import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from eproc.models import (
    MaintainanceBill, MaintainanceItem, MaintainInvoice, ProblemCategory, 
    ProblemSubCategory, StockItem, StockEntry, StockCategory, StockSubCategory, 
    Supplier, VehicleType, VehicleList, PurchaseOrder, PurchaseItem, 
    PurchaseEntry, InvoiceItem, InternalGrn, InternalGrnItems, Fuel, VehicleTrack,
    CompanyLetterhead
)
from eproc.decorators import user_access
from procurement.utils import render_to_pdf
from .dashboard_views import user_site, user_role

def get_active_letterhead(site_name=None):
    """
    Helper to fetch site-specific active letterhead or fallback to the master corporate letterhead.
    """
    if site_name:
        lh = CompanyLetterhead.objects.filter(site=site_name, is_active=True).first()
        if lh:
            return lh
    return CompanyLetterhead.objects.filter(is_active=True).first()

# ==================== MAINTENANCE DASHBOARD ====================
def maintainance_dashboard(request):
    count1 = Fuel.objects.all().count()
    count2 = MaintainanceBill.objects.all().count()
    count3 = VehicleList.objects.all().count()
    count4 = VehicleTrack.objects.all().count()
    context = {'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4}
    return render(request, 'fuelmaintain/maintainance_dashboard.html', context)

# ==================== PROBLEM CATEGORIES & SUBCATEGORIES ====================
@user_access
def problem_category(request):
    problem_dash = ProblemCategory.objects.all().order_by('-id')
    context = {'problem_dash': problem_dash}
    return render(request, 'fuelmaintain/problem_category.html', context)

@user_access
def add_problem(request):
    if request.method == "POST":
        name = request.POST.get('problem')
        url = request.POST.get('url')

        if ProblemCategory.objects.filter(problem_url=url).exists():
            messages.info(request, 'error')
            return redirect('problem_category')
        else:
            query = ProblemCategory(name=name, problem_url=url)
            query.save()
            messages.info(request, 'done')
            return redirect('problem_category')
    return redirect('problem_category')

@user_access
def problem_display(request):
    problem = ProblemCategory.objects.all()
    context = {'party': problem}
    return render(request, 'fuelmaintain/display/problem_display.html', context)

@user_access
def update_problem(request):
    if request.method == "POST":
        fid = request.POST.get('lid')
        name = request.POST.get('name')
        url = request.POST.get('url')

        if ProblemCategory.objects.filter(problem_url=url).exclude(id=fid).exists():
            messages.info(request, 'error')
            return redirect('problem_category')
        else:
            ProblemCategory.objects.filter(id=fid).update(name=name, problem_url=url)
            messages.info(request, 'done')
            return redirect('problem_category')
    return redirect('problem_category')

@user_access
def delete_problem(request):
    if request.method == "POST":
        sid = request.POST.get('lid')
        ProblemCategory.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('problem_category')
    return redirect('problem_category')

@user_access
def problem_subcategory(request):
    all_cats = []
    length = 0
    seen = set()
    seen_add = seen.add
    ent = ProblemSubCategory.objects.values_list('problem_url', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for c in ent:
        subcategory = ProblemSubCategory.objects.filter(problem_url=c)
        n = len(subcategory)
        if n > 0:
            length = 1
        all_cats.append([subcategory, range(1, n)])
    problem_dash = ProblemCategory.objects.all()
    context = {'all_cats': all_cats, 'problem_dash': problem_dash, 'length': length}
    return render(request, 'fuelmaintain/problem_subcategory.html', context)

@user_access
def add_subproblem(request):
    if request.method == "POST":
        name = request.POST.get('subproblem')
        url = request.POST.get('url')
        problem_url = request.POST.get('problemval')
        problem_name = request.POST.get('problem_name')
        if ProblemSubCategory.objects.filter(problem_url=problem_url, problem_suburl=url).exists():
            messages.info(request, 'error')
            return redirect('problem_subcategory')
        else:
            query = ProblemSubCategory(name=name, problem_suburl=url, problem_url=problem_url, problem_name=problem_name)
            query.save()
            messages.info(request, 'done')
            return redirect('problem_subcategory')
    return redirect('problem_subcategory')

@user_access
def update_subproblem(request):
    if request.method == "POST":
        fid = request.POST.get('lid')
        name = request.POST.get('name')
        url = request.POST.get('url')
        problem_url = request.POST.get('purl')
        if ProblemSubCategory.objects.filter(problem_url=problem_url, problem_suburl=url).exclude(id=fid).exists():
            messages.info(request, 'error')
            return redirect('problem_subcategory')
        else:
            ProblemSubCategory.objects.filter(id=fid).update(name=name, problem_suburl=url)
            messages.info(request, 'done')
            return redirect('problem_subcategory')
    return redirect('problem_subcategory')

@user_access
def delete_subproblem(request):
    if request.method == "POST":
        sid = request.POST.get('lid')
        ProblemSubCategory.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('problem_subcategory')
    return redirect('problem_subcategory')

# ==================== MAINTENANCE WORK ORDERS ====================
@user_access
def manage_maintainance(request):
    problem = ProblemCategory.objects.all()
    supplier_dash = Supplier.objects.all()
    v_type = VehicleType.objects.all()
    item_real = StockItem.objects.all()
    u_site = user_site(request)
    porder = PurchaseOrder.objects.filter(status='approved', issuing_site=u_site, po_vehi="yes")
    
    sub_material = []
    seen = set()
    seen_add = seen.add
    ent = ProblemSubCategory.objects.values_list('problem_url', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for s in ent:
        submat = ProblemSubCategory.objects.filter(problem_url=s)
        n = len(submat)
        sub_material.append([submat, range(1, n)])

    ivoice = list(set(MaintainanceBill.objects.values_list('bill_number', flat=True)))
    newpei = (MaintainanceBill.objects.last().pei + 1) if MaintainanceBill.objects.last() else 1

    vehis = []
    seen = set()
    seen_add = seen.add
    ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for e in ent:
        vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
        n = len(vehi)
        vehis.append([vehi, range(1, n)])

    pitem = PurchaseItem.objects.all()

    psupa = []
    seen = set()
    seen_add = seen.add
    tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for r in ent:
        ps = PurchaseEntry.objects.filter(purchase_order_number=r)
        n = len(ps)
        psupa.append([ps, range(1, n)])

    igoods = []
    seen = set()
    seen_add = seen.add
    tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for s in ent:
        igood = InvoiceItem.objects.filter(purchaseid=s, issue_use="no", grn_status='yes').exclude(Q(damage='all') | Q(retur='all'))
        n = len(igood)
        igoods.append([igood, range(1, n)])

    ingg = [i.grn_number for i in InternalGrn.objects.filter(user_site=u_site)]

    itrans = []
    seen = set()
    seen_add = seen.add
    tran = InternalGrnItems.objects.values_list('goodsid', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for s in ent:
        itra = InternalGrnItems.objects.filter(goodsid=s, grn__in=ingg, invoice_status="no").exclude(damage='all')
        n = len(itra)
        itrans.append([itra, range(1, n)])

    purinvoice = PurchaseEntry.objects.filter(issue_use='no')

    itemsel = []
    seen = set()
    seen_add = seen.add
    ent = StockItem.objects.values_list('main_url', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for e in ent:
        isel = StockItem.objects.filter(main_url=e)
        n = len(isel)
        itemsel.append([isel, range(1, n)])

    stock_cat = StockCategory.objects.all()
    psupaa = []
    seen = set()
    seen_add = seen.add
    tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for r in ent:
        pss = StockSubCategory.objects.filter(cat_url=r)
        n = len(pss)
        psupaa.append([pss, range(1, n)])

    context = {
        'psupa': psupa, 'itemsel': itemsel, 'stock_cat': stock_cat, 
        'psupaa': psupaa, 'purinvoice': purinvoice, 'igoods': igoods, 
        'itrans': itrans, 'pitem': pitem, 'sub_material': sub_material, 
        'item_real': item_real, 'vehis': vehis, 'v_type': v_type, 
        'supplier_dash': supplier_dash, 'problem': problem, 'ivoice': ivoice, 
        'porder': porder, 'newpei': newpei
    }
    return render(request, 'fuelmaintain/maintainance.html', context)

@user_access
def add_maintainance(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        entry_date = request.POST.get('date')
        billdate = request.POST.get('invoice_date')
        billnum = request.POST.get('invoice')
        maintain_number = request.POST.get('maintain_number')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_type_id = request.POST.get('vehicle_type_id')
        num_type = request.POST.get('num_type')
        vehicle = request.POST.get('vehiclee')
        kilometer = request.POST.get('kilometer')
        problem = request.POST.get('problem')
        subproblem = request.POST.get('subproblem')
        narrat = request.POST.get('narrat')
        pei = request.POST.get('pvn_count')
        jorder = request.POST.get('jorder')
        gjorder = request.POST.get('gjorder')
        subtotal = request.POST.get('subtotal')
        labour = request.POST.get('labour')
        total = request.POST.get('total')
        hour = request.POST.get('hour')
        itemadd = request.POST.getlist('itemadd')
        gitemadd = request.POST.getlist('gitemadd')
        exitemadd = request.POST.getlist('exitemadd')
        
        if len(itemadd) == 0 and len(gitemadd) == 0:
            messages.info(request, 'error')
            return redirect('manage_maintainance')
        if MaintainanceBill.objects.filter(vehicle_number=vehicle, hour=hour).exists():
            messages.info(request, 'error')
            return redirect('manage_maintainance')

        jobnumber = ''
        status = ''
        jedate = ''
        japprove = ''
        if jorder == 'yes':
            jobnumber = request.POST.get('jobnumber', '').replace(" ", "").upper()
            p = PurchaseOrder.objects.filter(purchase_number=jobnumber).first()
            if p:
                status = p.status
                jedate = p.entry_date
                japprove = p.approved_by 

        # Stock validations
        if jorder == 'yes':
            for i in itemadd:
                iid = str(i)
                if request.POST.get('inameid' + iid):
                    item_id = request.POST.get('inameid' + iid)
                    quantity = request.POST.get('iqty' + iid)
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if not sq or float(sq.quantity or 0) < float(quantity or 0):
                        messages.info(request, 'error')
                        return redirect('manage_maintainance')

        if gjorder == 'yes':
            for i in gitemadd:
                iid = str(i)
                if request.POST.get('ginameid' + iid):
                    item_id = request.POST.get('ginameid' + iid)
                    quantity = request.POST.get('giqty' + iid)
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if not sq or float(sq.quantity or 0) < float(quantity or 0):
                        messages.info(request, 'error')
                        return redirect('manage_maintainance')

        if len(exitemadd) > 0:
            for i in itemadd:
                iid = str(i)
                if request.POST.get('iid' + iid):
                    item_id = request.POST.get('iid' + iid)
                    quantity = request.POST.get('iqty' + iid)
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if not sq or float(sq.quantity or 0) < float(quantity or 0):
                        messages.info(request, 'error')
                        return redirect('manage_maintainance')

        query = MaintainanceBill(
            entry_by=current_user, maintain_number=maintain_number, hour=hour, pei=pei, 
            bill_number=billnum, purchase_order_number=jobnumber, purchase_entry_date=jedate, 
            purchase_approve_by=japprove, number_type=num_type, vehicle_type_id=vehicle_type_id, 
            vehicle_type=vehicle_type, vehicle_number=vehicle, purchase_status=status, 
            kilometer=kilometer, problem_category=problem, problem_subcategory=subproblem, 
            supplier_id='', supplier_name='', supplier_address='', supplier_contact='', 
            narration=narrat, entry_date=entry_date, bill_date=billdate, sub_total=subtotal, 
            labour_charge=labour, total=total, jorder=jorder, gjorder=gjorder, user_site=u_site
        )
        query.save()
        mid = query.id

        if jorder == 'yes':
            pvnval = request.POST.getlist('pvnval')
            for p_str in pvnval:
                p_upper = p_str.upper()
                pe = PurchaseEntry.objects.filter(voucher_number=p_upper).first()
                if pe:
                    MaintainInvoice.objects.create(
                        maintainid=mid, maintain_number=maintain_number, purchase_order_number=jobnumber, 
                        voucher_number=p_upper, invoice_number=pe.invoice_number, 
                        invoice_type=pe.invoice_type, supplier=pe.supplier_name, 
                        sub_total=pe.sub_total, discount_amt=pe.discount_amt, 
                        discount_per=pe.discount_per, vat=pe.vat, total=pe.total
                    )
                    PurchaseEntry.objects.filter(voucher_number=p_upper).update(issue_use='yes')

            for i in itemadd:
                iid = str(i)
                if request.POST.get('ipvn' + iid):
                    pvn = request.POST.get('ipvn' + iid)
                    item_id = request.POST.get('inameid' + iid)
                    item_name = request.POST.get('iname' + iid)
                    alias = request.POST.get('ialias' + iid)
                    uom = request.POST.get('iuom' + iid)
                    quantity = request.POST.get('iqty' + iid)
                    rate = request.POST.get('irate' + iid)
                    amount = request.POST.get('iamt' + iid)
                    dper = request.POST.get('idisper' + iid)
                    damt = request.POST.get('idisamt' + iid)
                    
                    MaintainanceItem.objects.create(
                        bill_id=mid, purchase_id=jobnumber, pvn=pvn, item_id=item_id, 
                        item_name=item_name, alias=alias, uom=uom, quantity=quantity, 
                        rate=rate, amount=amount, discount_per=dper, discount_amt=damt
                    )
                    InvoiceItem.objects.filter(pvn=pvn).update(issue_use='yes')
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if sq:
                        newqty = float(sq.quantity or 0) - float(quantity or 0)
                        StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

        ginvc = []
        if gjorder == 'yes':
            for i in gitemadd:
                iid = str(i)
                if request.POST.get('gipvn' + iid):
                    pvn = request.POST.get('gipvn' + iid)
                    item_id = request.POST.get('ginameid' + iid)
                    item_name = request.POST.get('giname' + iid)
                    alias = request.POST.get('gialias' + iid)
                    uom = request.POST.get('giuom' + iid)
                    quantity = request.POST.get('giqty' + iid)
                    
                    MaintainanceItem.objects.create(
                        bill_id=mid, pvn=pvn, item_id=item_id, item_name=item_name, 
                        alias=alias, uom=uom, quantity=quantity, rate=0, amount=0, 
                        discount_per=0, discount_amt=0, itnn='yes'
                    )
                    ginvc.append(pvn)
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if sq:
                        newqty = float(sq.quantity or 0) - float(quantity or 0)
                        StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

            for g_num in set(ginvc):
                InternalGrn.objects.filter(grn_number=g_num).update(invoice_id=maintain_number, invoice_status='yes')
                InternalGrnItems.objects.filter(grn=g_num).update(invoice_id=maintain_number, invoice_status='yes')

        if len(exitemadd) > 0:
            for i in itemadd:
                iid = str(i)
                if request.POST.get('iid' + iid):
                    item_id = request.POST.get('iid' + iid)
                    item_name = request.POST.get('iname' + iid)
                    alias = request.POST.get('ialias' + iid)
                    uom = request.POST.get('iuom' + iid)
                    quantity = request.POST.get('iqty' + iid)
                    rate = request.POST.get('irate' + iid)
                    amount = request.POST.get('iamt' + iid)
                    dper = request.POST.get('idisper' + iid)
                    damt = request.POST.get('idisamt' + iid)
                    
                    MaintainanceItem.objects.create(
                        bill_id=mid, item_id=item_id, item_name=item_name, alias=alias, 
                        uom=uom, quantity=quantity, rate=rate, amount=amount, 
                        discount_per=dper, discount_amt=damt
                    )
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if sq:
                        newqty = float(sq.quantity or 0) - float(quantity or 0)
                        StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

        messages.info(request, 'done')
        return redirect('manage_maintainance')
    return redirect('manage_maintainance')

@user_access
def maintainance_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = MaintainanceBill.objects.all().order_by('-id')
    else:
        s_it = MaintainanceBill.objects.filter(user_site=u_site).order_by('-id')
    
    page = request.GET.get('page', 1)
    paginator = Paginator(s_it, 30)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    n = len(product)
    s_item.append([product, range(1, n)])
    context = {'s_item': s_item}
    return render(request, 'fuelmaintain/display/maintain_display.html', context)

@user_access
def maintainance_detail(request, mid):
    if MaintainanceBill.objects.filter(id=mid).exists():
        minvoice = MaintainInvoice.objects.filter(maintainid=mid)
        item = MaintainanceBill.objects.filter(id=mid).first()
        sgoods = MaintainanceItem.objects.filter(bill_id=mid)
        context = {'item': item, 'sgoods': sgoods, 'minvoice': minvoice}
        return render(request, 'fuelmaintain/display/maintain_detail.html', context)
    return redirect('maintainance_display')

@user_access
def search_maintainance(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(maintain_number=search) | Q(vehicle_number__icontains=search) | 
                Q(problem_category=search) | Q(problem_subcategory=search) | 
                Q(supplier_name__icontains=search) | Q(purchase_order_number=search) | 
                Q(vehicle_type__icontains=search) | Q(user_site__icontains=search) | 
                Q(maintain_number=sea) | Q(vehicle_number=sea) | Q(problem_category=sea) | 
                Q(problem_subcategory=sea) | Q(supplier_name=sea) | Q(purchase_order_number=sea) | 
                Q(vehicle_type=sea) | Q(user_site=sea) | Q(maintain_number=se) | 
                Q(vehicle_number=se) | Q(problem_category=se) | Q(problem_subcategory=se) | 
                Q(supplier_name=se) | Q(purchase_order_number=se) | Q(vehicle_type=se) | 
                Q(user_site=se) | Q(maintain_number=s) | Q(vehicle_number=s) | 
                Q(problem_category=s) | Q(problem_subcategory=s) | Q(supplier_name=s) | 
                Q(purchase_order_number=s) | Q(vehicle_type=s) | Q(user_site=s)
            )
        else:
            lookup = (
                Q(Q(maintain_number=search) | Q(vehicle_number__icontains=search) | 
                  Q(problem_category=search) | Q(problem_subcategory=search) | 
                  Q(supplier_name__icontains=search) | Q(purchase_order_number=search) | 
                  Q(vehicle_type__icontains=search) | Q(maintain_number=sea) | 
                  Q(vehicle_number=sea) | Q(problem_category=sea) | Q(problem_subcategory=sea) | 
                  Q(supplier_name=sea) | Q(purchase_order_number=sea) | Q(vehicle_type=sea) | 
                  Q(maintain_number=se) | Q(vehicle_number=se) | Q(problem_category=se) | 
                  Q(problem_subcategory=se) | Q(supplier_name=se) | Q(purchase_order_number=se) | 
                  Q(vehicle_type=se) | Q(maintain_number=s) | Q(vehicle_number=s) | 
                  Q(problem_category=s) | Q(problem_subcategory=s) | Q(supplier_name=s) | 
                  Q(purchase_order_number=s) | Q(vehicle_type=s)) & Q(user_site=u_site)
            )
        s_item = []
        s_it = MaintainanceBill.objects.filter(lookup).order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(s_it, 30)
        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)
        n = len(product)
        s_item.append([product, range(1, n)])
        context = {'s_item': s_item, 'search': search}
        return render(request, 'fuelmaintain/display/maintainance_search.html', context)
    return redirect('maintainance_display')

@user_access
def print_maintainance(request):
    if request.method == "POST":
        minvoice = []
        jid = request.POST.get('jid')
        job = MaintainanceBill.objects.filter(id=jid).first()
        igoods = MaintainanceItem.objects.filter(bill_id=jid)
        if MaintainInvoice.objects.filter(maintainid=jid).exists():
            minvoice = MaintainInvoice.objects.filter(maintainid=jid)

        letterhead = get_active_letterhead(job.user_site if job else None)

        context = {
            'a': job, 
            'igoods': igoods, 
            'minvoice': minvoice,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('fuelmaintain/printmaintain.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportmaintain_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('maintainance_display')

@user_access
def edit_maintainance(request, mid):
    item = MaintainanceBill.objects.filter(id=mid).first()
    if not item:
        return redirect('maintainance_display')

    iv = item.bill_number
    u_site = item.user_site
    bills = []
    gmitms = []
    bill = MaintainanceItem.objects.filter(bill_id=mid).exclude(itnn='yes')
    bill_count = list(range(1, len(bill) + 1))
    bills.append([bill, range(1, len(bill))])
    
    problem = ProblemCategory.objects.all()
    porder = PurchaseOrder.objects.filter(status='approved', issuing_site=u_site, po_vehi="yes")
    supplier_dash = Supplier.objects.all()
    v_type = VehicleType.objects.all()
    item_real = StockItem.objects.all()
    
    sub_material = []
    seen = set()
    seen_add = seen.add
    ent = ProblemSubCategory.objects.values_list('problem_url', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for s in ent:
        submat = ProblemSubCategory.objects.filter(problem_url=s)
        n = len(submat)
        sub_material.append([submat, range(1, n)])
    
    ivoice = [s for s in list(set(MaintainanceBill.objects.values_list('bill_number', flat=True))) if s != iv]

    vehis = []
    seen = set()
    seen_add = seen.add
    ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for e in ent:
        vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
        n = len(vehi)
        vehis.append([vehi, range(1, n)])

    pitem = PurchaseItem.objects.all()

    psupa = []
    seen = set()
    seen_add = seen.add
    tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for r in ent:
        ps = PurchaseEntry.objects.filter(purchase_order_number=r)
        n = len(ps)
        psupa.append([ps, range(1, n)])

    minv = MaintainInvoice.objects.filter(maintainid=mid)
    mis = [m.voucher_number for m in minv]

    igoods = []
    seen = set()
    seen_add = seen.add
    tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for s in ent:
        igood = InvoiceItem.objects.filter(purchaseid=s, issue_use='no', grn_status='yes').exclude(Q(damage='all') | Q(retur='all'))
        n = len(igood)
        igoods.append([igood, range(1, n)])

    ingg = [i.grn_number for i in InternalGrn.objects.filter(user_site=u_site)]

    itrans = []
    seen = set()
    seen_add = seen.add
    tran = InternalGrnItems.objects.values_list('goodsid', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for s in ent:
        itra = InternalGrnItems.objects.filter(goodsid=s, grn__in=ingg, invoice_status="no").exclude(damage='all')
        n = len(itra)
        itrans.append([itra, range(1, n)])

    purinvoice = PurchaseEntry.objects.filter(Q(issue_use='no') | Q(voucher_number__in=mis))
    mitm = MaintainanceItem.objects.filter(bill_id=mid).exclude(Q(pvn='') | Q(itnn='yes'))
    gmm = MaintainanceItem.objects.filter(bill_id=mid, itnn='yes')
    gmitm = MaintainanceItem.objects.filter(bill_id=mid, itnn='yes')
    gmitms.append([gmitm, range(1, len(gmitm))])

    itemsel = []
    seen = set()
    seen_add = seen.add
    ent = StockItem.objects.values_list('main_url', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for e in ent:
        isel = StockItem.objects.filter(main_url=e)
        n = len(isel)
        itemsel.append([isel, range(1, n)])

    stock_cat = StockCategory.objects.all()
    psupaa = []
    seen = set()
    seen_add = seen.add
    tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for r in ent:
        pss = StockSubCategory.objects.filter(cat_url=r)
        psupaa.append([pss, range(1, len(pss))])

    context = {
        'psupa': psupa, 'itemsel': itemsel, 'stock_cat': stock_cat, 
        'psupaa': psupaa, 'mitm': mitm, 'gmm': gmm, 'gmitms': gmitms, 
        'bill': bill, 'minv': minv, 'purinvoice': purinvoice, 'igoods': igoods, 
        'itrans': itrans, 'pitem': pitem, 'item': item, 'item_real': item_real, 
        'vehis': vehis, 'v_type': v_type, 'supplier_dash': supplier_dash, 
        'bills': bills, 'bill_count': bill_count, 'sub_material': sub_material, 
        'problem': problem, 'porder': porder
    }
    return render(request, 'fuelmaintain/maintain_edit.html', context)

@user_access
def edit_maintainance_entry(request):
    if request.method == "POST":
        entry_id = request.POST.get('entry_id')
        mb = MaintainanceBill.objects.filter(id=entry_id).first()
        if not mb:
            return redirect('maintainance_display')
        u_site = mb.user_site
        entry_date = request.POST.get('date')
        billdate = request.POST.get('invoice_date')
        billnum = request.POST.get('invoice')
        maintain_number = request.POST.get('maintain_number')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_type_id = request.POST.get('vehicle_type_id')
        num_type = request.POST.get('num_type')
        vehicle = request.POST.get('vehiclee')
        kilometer = request.POST.get('kilometer')
        problem = request.POST.get('problem')
        subproblem = request.POST.get('subproblem')
        narrat = request.POST.get('narrat')
        jorder = request.POST.get('jorder')
        gjorder = request.POST.get('gjorder')
        subtotal = request.POST.get('subtotal')
        labour = request.POST.get('labour')
        total = request.POST.get('total')
        hour = request.POST.get('hour')
        itemadd = request.POST.getlist('itemadd')
        gitemadd = request.POST.getlist('gitemadd')
        exitemadd = request.POST.getlist('exitemadd')

        if len(itemadd) == 0 and len(gitemadd) == 0:
            messages.info(request, 'error')
            return redirect('/edit-maintainance/' + entry_id + '/')
        if MaintainanceBill.objects.filter(vehicle_number=vehicle, hour=hour).exclude(id=entry_id).exists():
            messages.info(request, 'error')
            return redirect('/edit-maintainance/' + entry_id + '/')

        jobnumber = ''
        status = ''
        jedate = ''
        japprove = ''
        if jorder == 'yes':
            jobnumber = request.POST.get('jobnumber', '').replace(" ", "").upper()
            p = PurchaseOrder.objects.filter(purchase_number=jobnumber).first()
            if p:
                status = p.status
                jedate = p.entry_date
                japprove = p.approved_by

        # Validation
        if jorder == 'yes':
            for i in itemadd:
                iid = str(i)
                if request.POST.get('inameid' + iid):
                    item_id = request.POST.get('inameid' + iid)
                    quantity = request.POST.get('iqty' + iid)
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if not sq or float(sq.quantity or 0) < float(quantity or 0):
                        messages.info(request, 'error')
                        return redirect('/edit-maintainance/' + entry_id + '/')

        if gjorder == 'yes':
            for i in gitemadd:
                iid = str(i)
                if request.POST.get('ginameid' + iid):
                    item_id = request.POST.get('ginameid' + iid)
                    quantity = request.POST.get('giqty' + iid)
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if not sq or float(sq.quantity or 0) < float(quantity or 0):
                        messages.info(request, 'error')
                        return redirect('/edit-maintainance/' + entry_id + '/')

        if len(exitemadd) > 0:
            for i in itemadd:
                iid = str(i)
                if request.POST.get('iid' + iid):
                    item_id = request.POST.get('iid' + iid)
                    quantity = request.POST.get('iqty' + iid)
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if not sq or float(sq.quantity or 0) < float(quantity or 0):
                        messages.info(request, 'error')
                        return redirect('/edit-maintainance/' + entry_id + '/')

        MaintainanceBill.objects.filter(id=entry_id).update(
            bill_number=billnum, purchase_order_number=jobnumber, hour=hour, 
            purchase_entry_date=jedate, purchase_approve_by=japprove, number_type=num_type, 
            vehicle_type_id=vehicle_type_id, vehicle_type=vehicle_type, vehicle_number=vehicle, 
            purchase_status=status, kilometer=kilometer, problem_category=problem, 
            problem_subcategory=subproblem, narration=narrat, entry_date=entry_date, 
            bill_date=billdate, sub_total=subtotal, labour_charge=labour, total=total
        )

        # Rollback stock
        gq = MaintainanceItem.objects.filter(bill_id=entry_id)
        invt = []
        ginv = []
        for a in gq:
            itemid = a.item_id
            qty = a.quantity
            sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
            if sq:
                newqty = float(sq.quantity or 0) + float(qty or 0)
                StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
            if a.pvn:
                if InvoiceItem.objects.filter(pvn=a.pvn).exists():
                    invt.append(a.pvn)
                if InternalGrnItems.objects.filter(pvn=a.pvn).exists():
                    ginv.append(a.pvn)

        for i in set(invt):
            InvoiceItem.objects.filter(pvn=i).update(issue_use='no')
        for i in set(ginv):
            InternalGrnItems.objects.filter(grn=i).update(invoice_id='', invoice_status='no')
            InternalGrn.objects.filter(grn_number=i).update(invoice_id='', invoice_status='no')

        gm = MaintainInvoice.objects.filter(maintainid=entry_id)
        for m in gm:
            PurchaseEntry.objects.filter(voucher_number=m.voucher_number).update(issue_use='no')
        MaintainInvoice.objects.filter(maintainid=entry_id).delete()

        if jorder == 'yes':
            pvnval = request.POST.getlist('pvnval')
            for p_str in pvnval:
                p_upper = p_str.upper()
                pe = PurchaseEntry.objects.filter(voucher_number=p_upper).first()
                if pe:
                    MaintainInvoice.objects.create(
                        maintainid=entry_id, maintain_number=maintain_number, purchase_order_number=jobnumber, 
                        voucher_number=p_upper, invoice_number=pe.invoice_number, 
                        invoice_type=pe.invoice_type, supplier=pe.supplier_name, 
                        sub_total=pe.sub_total, discount_amt=pe.discount_amt, 
                        discount_per=pe.discount_per, vat=pe.vat, total=pe.total
                    )
                    PurchaseEntry.objects.filter(voucher_number=p_upper).update(issue_use='yes')

        MaintainanceItem.objects.filter(bill_id=entry_id).delete()
        if jorder == 'yes':
            for i in itemadd:
                iid = str(i)
                if request.POST.get('ipvn' + iid):
                    pvn = request.POST.get('ipvn' + iid)
                    item_id = request.POST.get('inameid' + iid)
                    item_name = request.POST.get('iname' + iid)
                    alias = request.POST.get('ialias' + iid)
                    uom = request.POST.get('iuom' + iid)
                    quantity = request.POST.get('iqty' + iid)
                    rate = request.POST.get('irate' + iid)
                    amount = request.POST.get('iamt' + iid)
                    dper = request.POST.get('idisper' + iid)
                    damt = request.POST.get('idisamt' + iid)
                    
                    MaintainanceItem.objects.create(
                        bill_id=entry_id, purchase_id=jobnumber, pvn=pvn, item_id=item_id, 
                        item_name=item_name, alias=alias, uom=uom, quantity=quantity, 
                        rate=rate, amount=amount, discount_per=dper, discount_amt=damt
                    )
                    InvoiceItem.objects.filter(pvn=pvn).update(issue_use='yes')
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if sq:
                        newqty = float(sq.quantity or 0) - float(quantity or 0)
                        StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

        ginvc_new = []
        if gjorder == 'yes':
            for i in gitemadd:
                iid = str(i)
                if request.POST.get('gipvn' + iid):
                    pvn = request.POST.get('gipvn' + iid)
                    item_id = request.POST.get('ginameid' + iid)
                    item_name = request.POST.get('giname' + iid)
                    alias = request.POST.get('gialias' + iid)
                    uom = request.POST.get('giuom' + iid)
                    quantity = request.POST.get('giqty' + iid)
                    
                    MaintainanceItem.objects.create(
                        bill_id=entry_id, pvn=pvn, item_id=item_id, item_name=item_name, 
                        alias=alias, uom=uom, quantity=quantity, rate=0, amount=0, 
                        discount_per=0, discount_amt=0, itnn='yes'
                    )
                    ginvc_new.append(pvn)
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if sq:
                        newqty = float(sq.quantity or 0) - float(quantity or 0)
                        StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

            for g_num in set(ginvc_new):
                InternalGrn.objects.filter(grn_number=g_num).update(invoice_id=maintain_number, invoice_status='yes')
                InternalGrnItems.objects.filter(grn=g_num).update(invoice_id=maintain_number, invoice_status='yes')

        if len(exitemadd) > 0:
            for i in itemadd:
                iid = str(i)
                if request.POST.get('iid' + iid):
                    item_id = request.POST.get('iid' + iid)
                    item_name = request.POST.get('iname' + iid)
                    alias = request.POST.get('ialias' + iid)
                    uom = request.POST.get('iuom' + iid)
                    quantity = request.POST.get('iqty' + iid)
                    rate = request.POST.get('irate' + iid)
                    amount = request.POST.get('iamt' + iid)
                    dper = request.POST.get('idisper' + iid)
                    damt = request.POST.get('idisamt' + iid)
                    
                    MaintainanceItem.objects.create(
                        bill_id=entry_id, item_id=item_id, item_name=item_name, alias=alias, 
                        uom=uom, quantity=quantity, rate=rate, amount=amount, 
                        discount_per=dper, discount_amt=damt
                    )
                    sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
                    if sq:
                        newqty = float(sq.quantity or 0) - float(quantity or 0)
                        StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

        messages.info(request, 'done')
        return redirect('/edit-maintainance/' + entry_id + '/')
    return redirect('maintainance_display')

@user_access
def maintainance_delete(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        gmm = MaintainanceBill.objects.filter(id=sid).first()
        if not gmm:
            return redirect('maintainance_display')
        u_site = gmm.user_site
        gq = MaintainanceItem.objects.filter(bill_id=sid)
        invt = []
        ginv = []
        for a in gq:
            itemid = a.item_id
            qty = a.quantity
            sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
            if sq:
                newqty = float(sq.quantity or 0) + float(qty or 0)
                StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
            if a.pvn:
                if InvoiceItem.objects.filter(pvn=a.pvn).exists():
                    invt.append(a.pvn)
                if InternalGrnItems.objects.filter(pvn=a.pvn).exists():
                    ginv.append(a.pvn)

        for i in set(invt):
            InvoiceItem.objects.filter(pvn=i).update(issue_use='no')
        for i in set(ginv):
            InternalGrnItems.objects.filter(pvn=i).update(invoice_id='', invoice_status='no')
            InternalGrn.objects.filter(pvn=i).update(invoice_id='', invoice_status='no')

        gm = MaintainInvoice.objects.filter(maintainid=sid)
        for m in gm:
            PurchaseEntry.objects.filter(voucher_number=m.voucher_number).update(issue_use='no')

        MaintainInvoice.objects.filter(maintainid=sid).delete()
        MaintainanceBill.objects.filter(id=sid).delete()
        MaintainanceItem.objects.filter(bill_id=sid).delete()

        messages.info(request, 'done')
        return redirect('maintainance_display')
    return redirect('maintainance_display')