import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import user_passes_test

from eproc.models import (
    Supplier, Location, Vehicle, UOM, Site, StockItem, StockEntry,
    StockCategory, StockSubCategory,
    PurchaseOrder, PurchaseItem, PurchaseEntry, InvoiceItem,
    GoodsEntry, Goods, GoodsExtra, QuotationEntry, QuotationItem,
    Notification, DamageEntry, ReturnEntry, VehicleType, VehicleList,
    CompanyLetterhead
)
from account.views import check_staff
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

@user_passes_test(check_staff, login_url='login_user')
def purchase(request):
    goo = GoodsEntry.objects.all().count()
    invoi = PurchaseEntry.objects.all().count()
    pur = PurchaseOrder.objects.all().count()
    dm = DamageEntry.objects.all().count()
    rm = ReturnEntry.objects.all().count()
    context = {'goo': goo, 'invoi': invoi, 'pur': pur, 'dm': dm, 'rm': rm}    
    return render(request, 'purchase.html', context)

# ==================== ASHISH GRN & INVOICE WORKFLOW ====================
@user_access
def ashish_goods_entry(request):
    supplier_dash = Supplier.objects.all()
    location_dash = Location.objects.all()
    vehicle_dash = Vehicle.objects.all()
    porder = PurchaseOrder.objects.filter(status='approved')
    uom_dash = UOM.objects.all()
    u_site = user_site(request)
    item_dash = StockItem.objects.all()
    grn = 0
    if GoodsEntry.objects.last():
        good = GoodsEntry.objects.last()
        ng = good.grn_count
        grn = int(ng) + 1
    else:
        grn = grn + 1

    gchallan = [item['challan_number'] for item in GoodsEntry.objects.values('challan_number')]
    gbill = [item['bill_number'] for item in GoodsEntry.objects.values('bill_number')]

    igoods = []
    seen = set()
    seen_add = seen.add
    tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for s in ent:
        igood = InvoiceItem.objects.filter(purchaseid=s, grn_status='no', issue_use='no').exclude(Q(damage='all') | Q(retur='all'))
        n = len(igood)
        igoods.append([igood, range(1, n)])

    purinvoice = []
    seen = set()
    seen_add = seen.add
    tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for s in ent:
        pur = PurchaseEntry.objects.filter(purchase_order_number=s)
        n = len(pur)
        purinvoice.append([pur, range(1, n)])

    context = {
        'porder': porder, 'purinvoice': purinvoice, 'supplier_dash': supplier_dash, 
        'igoods': igoods, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 
        'uom_dash': uom_dash, 'item_dash': item_dash, 'grn': grn, 
        'gchallan': gchallan, 'gbill': gbill
    }    
    return render(request, 'ashish_goods_entry.html', context)

@user_access
def ashish_goods_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = GoodsEntry.objects.all().order_by('-id')
    else:
        s_it = GoodsEntry.objects.filter(user_site=u_site).order_by('-id')
    
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
    return render(request, 'display/ashish_goods_display.html', context)

@user_access
def ashish_goods_detail(request, gid):
    if GoodsEntry.objects.filter(id=gid).exists():
        item = GoodsEntry.objects.filter(id=gid).first()
        s_goods = Goods.objects.filter(goodsid=gid)
        iextra = GoodsExtra.objects.filter(goodsid=gid)
        context = {'item': item, 's_goods': s_goods, 'iextra': iextra}    
        return render(request, 'display/ashish_goods_detail.html', context)
    return redirect('ashish_goods_display')

@user_access
def ashish_search_goods(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(grn_number=search) | Q(challan_number=search) | Q(bill_number=search) | 
                Q(supplier_name__icontains=search) | Q(vehicle_number__icontains=search) | 
                Q(user_site__icontains=search) | Q(grn_number=sea) | Q(challan_number=sea) | 
                Q(bill_number=sea) | Q(supplier_name=sea) | Q(vehicle_number=sea) | 
                Q(user_site=sea) | Q(grn_number=se) | Q(challan_number=se) | 
                Q(bill_number=se) | Q(supplier_name=se) | Q(vehicle_number=se) | 
                Q(user_site=se) | Q(grn_number=s) | Q(challan_number=s) | 
                Q(bill_number=s) | Q(supplier_name=s) | Q(vehicle_number=s) | Q(user_site=s)
            )
        else:
            lookup = (
                Q(Q(grn_number=search) | Q(challan_number=search) | Q(bill_number=search) | 
                  Q(supplier_name__icontains=search) | Q(vehicle_number__icontains=search) | 
                  Q(grn_number=sea) | Q(challan_number=sea) | Q(bill_number=sea) | 
                  Q(supplier_name=sea) | Q(vehicle_number=sea) | Q(grn_number=se) | 
                  Q(challan_number=se) | Q(bill_number=se) | Q(supplier_name=se) | 
                  Q(vehicle_number=se) | Q(grn_number=s) | Q(challan_number=s) | 
                  Q(bill_number=s) | Q(supplier_name=s) | Q(vehicle_number=s)) & Q(user_site=u_site)
            )
        s_goods = []
        s_goo = GoodsEntry.objects.filter(lookup).order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(s_goo, 30)
        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)
        n = len(product)
        s_goods.append([product, range(1, n)])
        context = {'s_goods': s_goods, 'search': search}
        return render(request, 'display/ashish_goods_search.html', context)
    return redirect('ashish_goods_display')

@user_access
def ashish_print_goods(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = GoodsEntry.objects.filter(id=jid).first()
        igoods = Goods.objects.filter(goodsid=jid)
        iextra = GoodsExtra.objects.filter(goodsid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods, 
            'iextra': iextra,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('ashish_printgoods.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportgoods_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('login_user')

@user_access
def ashish_delete_goods(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        ge = GoodsEntry.objects.filter(id=sid).first()
        if ge:
            u_site = ge.user_site
            gq = Goods.objects.filter(goodsid=sid)
            for a in gq:
                itemid = a.item_id
                qty = a.quantity
                pvn = a.pvn
                sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                if sq:
                    qt = float(sq.quantity or 0)
                    newqty = max(0, qt - float(qty or 0))
                    StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
                PurchaseEntry.objects.filter(voucher_number=pvn).update(grn_id='', grn_status='no')
                InvoiceItem.objects.filter(pvn=pvn).update(grn_id='', grn_status='no')

            GoodsEntry.objects.filter(id=sid).delete()
            Goods.objects.filter(goodsid=sid).delete()
            GoodsExtra.objects.filter(goodsid=sid).delete()
            messages.info(request, 'done')
        return redirect('ashish_goods_display')
    return redirect('ashish_goods_display')

@user_access
def ashish_goods_edit(request, gid):
    if GoodsEntry.objects.filter(id=gid).exists():
        item = GoodsEntry.objects.filter(id=gid).first()
        cn = item.challan_number
        bn = item.bill_number

        seen = set()
        seen_add = seen.add
        tran = Goods.objects.values_list('pvn', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        inv_count = []
        for b in ent:
            que = Goods.objects.filter(pvn=b, goodsid=gid)
            for i in que:
                inv_count.append(i.pvn)

        supplier_dash = Supplier.objects.all()
        location_dash = Location.objects.all()
        vehicle_dash = Vehicle.objects.all()
        uom_dash = UOM.objects.all()
        item_dash = StockItem.objects.all()

        gchallan = [s['challan_number'] for s in GoodsEntry.objects.values('challan_number')]
        gbill = [s['bill_number'] for s in GoodsEntry.objects.values('bill_number')]
        gchallan = [x for x in gchallan if x != cn]
        gbill = [x for x in gbill if x != bn]

        igoods = []
        seen = set()
        seen_add = seen.add
        tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for s in ent:
            igood = InvoiceItem.objects.filter(purchaseid=s, grn_status='no', issue_use='no')
            n = len(igood)
            igoods.append([igood, range(1, n)])

        invitem = []
        seen = set()
        seen_add = seen.add
        tran = Goods.objects.values_list('pvn', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for s in ent:
            inv = Goods.objects.filter(pvn=s, goodsid=gid)
            n = len(inv)
            invitem.append([inv, range(1, n)])

        purinvoice = []
        seen = set()
        seen_add = seen.add
        tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for s in ent:
            pur = PurchaseEntry.objects.filter(purchase_order_number=s)
            n = len(pur)
            purinvoice.append([pur, range(1, n)])

        purextra = GoodsExtra.objects.filter(goodsid=gid)

        context = {
            'item': item, 'purextra': purextra, 'purinvoice': purinvoice, 
            'invitem': invitem, 'igoods': igoods, 'inv_count': inv_count, 
            'supplier_dash': supplier_dash, 'location_dash': location_dash, 
            'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 
            'item_dash': item_dash, 'gchallan': gchallan, 'gbill': gbill
        }    
        return render(request, 'ashish_goods_edit.html', context)
    return redirect('ashish_goods_display')

@user_access
def ashish_add_goods(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date = request.POST.get('date')
        grn = request.POST.get('grn')
        grn_count = request.POST.get('grn_count')
        challan = request.POST.get('challan')
        bill = request.POST.get('bill')
        location = request.POST.get('location')
        narrat = request.POST.get('narrat')
        porder = request.POST.get('porder', '').upper().replace(" ", "")
        itemadd = request.POST.getlist('itemadd')

        for a in itemadd:
            a = str(a)
            pvn = request.POST.get('ipvn' + a, '').upper()
            itemid = request.POST.get('inameid' + a)
            if not StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
                messages.info(request, 'error')
                return redirect('ashish_goods_entry')
            if PurchaseEntry.objects.filter(voucher_number=pvn, grn_status='yes').exists():
                messages.info(request, 'error')
                return redirect('ashish_goods_entry')

        if GoodsEntry.objects.filter(grn_number=grn).exists():
            messages.info(request, 'error')
            return redirect('ashish_goods_entry')
        else:
            query = GoodsEntry(
                entry_date=date, purchase_order_number=porder, narration=narrat, 
                grn_number=grn, grn_count=grn_count, challan_number=challan, 
                bill_number=bill, location=location, entry_by=current_user, user_site=u_site
            )
            query.save()

        gid = query.id
        for a in itemadd:
            a = str(a)
            pvn = request.POST.get('ipvn' + a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            alias = request.POST.get('ialias' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            que = Goods(goodsid=gid, pvn=pvn, grn=grn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
            que.save()

            sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
            if sq:
                qt = float(sq.quantity or 0)
                newqty = qt + float(qty or 0)
                StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

            if not GoodsExtra.objects.filter(goodsid=gid, voucher_number=pvn).exists():
                s = PurchaseEntry.objects.filter(voucher_number=pvn).first()
                if s:
                    supp = s.supplier_name
                    por = s.purchase_order_number
                    pv = pvn.upper()
                    g_extra = GoodsExtra(grn_number=grn, goodsid=gid, purchase_order_number=por, voucher_number=pv, supplier=supp)
                    g_extra.save()

            PurchaseEntry.objects.filter(voucher_number=pvn).update(grn_id=gid, grn_status='yes')
            InvoiceItem.objects.filter(pvn=pvn).update(grn_id=gid, grn_status='yes')

        po = PurchaseOrder.objects.filter(purchase_number=porder).first()
        issuing_site_name = po.issuing_site if po else ''

        q = Notification(
            notify_topic='grn', content_id=gid, content='grn_add', 
            from_site=u_site, from_user=current_user, content_val=grn, 
            content_val2=issuing_site_name
        )
        q.save()

        messages.info(request, 'done')
        return redirect('ashish_goods_entry')
    return redirect('ashish_goods_entry')

@user_access
def ashish_edit_goods(request):
    if request.method == "POST":
        gid = request.POST.get('gid')
        date = request.POST.get('date')
        grn = request.POST.get('grn')
        challan = request.POST.get('challan')
        bill = request.POST.get('bill')
        porder = request.POST.get('porder', '').replace(" ", "").upper()
        narrat = request.POST.get('narrat')
        itemadd = request.POST.getlist('itemadd')

        ge = GoodsEntry.objects.filter(id=gid).first()
        if not ge:
            return redirect('ashish_goods_display')
        u_site = ge.user_site

        gq = Goods.objects.filter(goodsid=gid)
        gpvn = [a.pvn.upper() for a in gq]

        for a in itemadd:
            a = str(a)
            pvn = request.POST.get('ipvn' + a, '').upper()
            itemid = request.POST.get('inameid' + a)
            if not StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
                messages.info(request, 'error')
                return redirect('/ashish-edit-goods/' + str(gid) + '/')
            if PurchaseEntry.objects.filter(voucher_number=pvn, grn_status='yes').exclude(voucher_number__in=gpvn).exists():
                messages.info(request, 'error')
                return redirect('/ashish-edit-goods/' + str(gid) + '/')

        GoodsEntry.objects.filter(id=gid).update(entry_date=date, narration=narrat, challan_number=challan, bill_number=bill)

        for a in gq:
            itemid = a.item_id
            qty = a.quantity
            pvn = a.pvn
            sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
            if sq:
                qt = float(sq.quantity or 0)
                newqty = max(0, qt - float(qty or 0))
                StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
            PurchaseEntry.objects.filter(voucher_number=pvn).update(grn_id='', grn_status='no')
            InvoiceItem.objects.filter(pvn=pvn).update(grn_id='', grn_status='no')

        GoodsExtra.objects.filter(goodsid=gid).delete()
        Goods.objects.filter(goodsid=gid).delete()

        for a in itemadd:
            a = str(a)
            pvn = request.POST.get('ipvn' + a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            alias = request.POST.get('ialias' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            que = Goods(goodsid=gid, pvn=pvn, grn=grn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
            que.save()
            sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
            if sq:
                qt = float(sq.quantity or 0)
                newqty = qt + float(qty or 0)
                StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

            if not GoodsExtra.objects.filter(goodsid=gid, voucher_number=pvn).exists():
                s = PurchaseEntry.objects.filter(voucher_number=pvn).first()
                if s:
                    supp = s.supplier_name
                    por = s.purchase_order_number
                    g_extra = GoodsExtra(grn_number=grn, goodsid=gid, purchase_order_number=por, voucher_number=pvn, supplier=supp)
                    g_extra.save()
            PurchaseEntry.objects.filter(voucher_number=pvn).update(grn_id=gid, grn_status='yes')
            InvoiceItem.objects.filter(pvn=pvn).update(grn_id=gid, grn_status='yes')

        messages.info(request, 'done')
        return redirect('/ashish-edit-goods/' + str(gid) + '/')
    return redirect('ashish_goods_display')

@user_access
def ashish_purchase_invoice(request):
    supplier_dash = Supplier.objects.all()
    location_dash = Location.objects.all()
    vehicle_dash = Vehicle.objects.all()
    porder = PurchaseOrder.objects.filter(status='approved')
    uom_dash = UOM.objects.all()
    item_dash = StockItem.objects.all()
    pvn = 0
    if PurchaseEntry.objects.last():
        good = PurchaseEntry.objects.last()
        ng = good.pvn_count
        pvn = int(ng) + 1
    else:
        pvn = pvn + 1

    ichallan = [item['challan_number'] for item in PurchaseEntry.objects.values('challan_number')]
    ivoice = [item['invoice_number'] for item in PurchaseEntry.objects.values('invoice_number')]
    pitem = PurchaseItem.objects.all()

    context = {
        'porder': porder, 'pitem': pitem, 'pvn': pvn, 'item_dash': item_dash, 
        'ichallan': ichallan, 'ivoice': ivoice, 'supplier_dash': supplier_dash, 
        'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash
    }    
    return render(request, 'ashish_purchase_invoice.html', context)

ashish_invoice_entry = ashish_purchase_invoice

@user_access
def ashish_invoice_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = PurchaseEntry.objects.all().order_by('-id')
    else:
        s_it = PurchaseEntry.objects.filter(user_site=u_site).order_by('-id')
    
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
    return render(request, 'display/ashish_invoice_display.html', context)

@user_access
def ashish_invoice_detail(request, pid):
    if PurchaseEntry.objects.filter(id=pid).exists():
        item = PurchaseEntry.objects.filter(id=pid).first()
        s_goods = InvoiceItem.objects.filter(purchaseid=pid)
        context = {'item': item, 's_goods': s_goods}    
        return render(request, 'display/ashish_invoice_detail.html', context)
    return redirect('ashish_invoice_display')

@user_access
def ashish_search_invoice(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(purchase_order_number=search) | Q(voucher_number=search) | Q(challan_number=search) | 
                Q(invoice_number=search) | Q(invoice_type__icontains=search) | Q(supplier_name__icontains=search) | 
                Q(vehicle_number__icontains=search) | Q(user_site__icontains=search) | Q(narration__icontains=search) | 
                Q(purchase_order_number=sea) | Q(voucher_number=sea) | Q(challan_number=sea) | 
                Q(invoice_number=sea) | Q(invoice_type__icontains=sea) | Q(supplier_name__icontains=sea) | 
                Q(vehicle_number__icontains=sea) | Q(user_site__icontains=sea) | Q(narration__icontains=sea) | 
                Q(purchase_order_number=se) | Q(voucher_number=se) | Q(challan_number=se) | 
                Q(invoice_number=se) | Q(invoice_type__icontains=se) | Q(supplier_name__icontains=se) | 
                Q(vehicle_number__icontains=se) | Q(user_site__icontains=se) | Q(narration__icontains=se) | 
                Q(purchase_order_number=s) | Q(voucher_number=s) | Q(challan_number=s) | 
                Q(invoice_number=s) | Q(invoice_type__icontains=s) | Q(supplier_name__icontains=s) | 
                Q(vehicle_number__icontains=s) | Q(user_site__icontains=s) | Q(narration__icontains=s)
            )
        else:
            lookup = (
                Q(Q(purchase_order_number=search) | Q(voucher_number=search) | Q(challan_number=search) | 
                  Q(invoice_number=search) | Q(invoice_type__icontains=search) | Q(supplier_name__icontains=search) | 
                  Q(vehicle_number__icontains=search) | Q(narration__icontains=search) | Q(purchase_order_number=sea) | 
                  Q(voucher_number=sea) | Q(challan_number=sea) | Q(invoice_number=sea) | 
                  Q(invoice_type__icontains=sea) | Q(supplier_name__icontains=sea) | Q(vehicle_number__icontains=sea) | 
                  Q(narration__icontains=sea) | Q(purchase_order_number=se) | Q(voucher_number=se) | 
                  Q(challan_number=se) | Q(invoice_number=se) | Q(invoice_type__icontains=se) | 
                  Q(supplier_name__icontains=se) | Q(vehicle_number__icontains=se) | Q(narration__icontains=se) | 
                  Q(purchase_order_number=s) | Q(voucher_number=s) | Q(challan_number=s) | 
                  Q(invoice_number=s) | Q(invoice_type__icontains=s) | Q(supplier_name__icontains=s) | 
                  Q(vehicle_number__icontains=s) | Q(narration__icontains=s)) & Q(user_site=u_site)
            )
        s_item = []
        s_it = PurchaseEntry.objects.filter(lookup).order_by('-id')
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
        return render(request, 'display/ashish_search_invoice.html', context)
    return redirect('ashish_invoice_display')

@user_access
def ashish_print_invoice(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = PurchaseEntry.objects.filter(id=jid).first()
        igoods = InvoiceItem.objects.filter(purchaseid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('ashish_printinvoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportinvoice_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('ashish_invoice_display')

@user_access
def ashish_delete_invoice(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        PurchaseEntry.objects.filter(id=sid).delete()
        InvoiceItem.objects.filter(purchaseid=sid).delete()
        messages.info(request, 'done')
        return redirect('ashish_invoice_display')
    return redirect('ashish_invoice_display')

@user_access
def ashish_invoice_edit(request, pid):
    if PurchaseEntry.objects.filter(id=pid).exists():
        supplier_dash = Supplier.objects.all()
        location_dash = Location.objects.all()
        vehicle_dash = Vehicle.objects.all()
        uom_dash = UOM.objects.all()
        item_dash = StockItem.objects.all()
        porder = PurchaseOrder.objects.filter(status='approved')
        item = PurchaseEntry.objects.filter(id=pid).first()
        cn = item.challan_number
        ni = item.invoice_number
        invitem = InvoiceItem.objects.filter(purchaseid=pid)

        ichallan = [s['challan_number'] for s in PurchaseEntry.objects.values('challan_number') if s['challan_number'] != cn]
        ivoice = [s['invoice_number'] for s in PurchaseEntry.objects.values('invoice_number') if s['invoice_number'] != ni]

        inv_count = list(range(1, len(invitem) + 1))
        pitem = PurchaseItem.objects.all()

        context = {
            'item': item, 'porder': porder, 'pitem': pitem, 'inv_count': inv_count, 
            'invitem': invitem, 'item_dash': item_dash, 'ichallan': ichallan, 
            'ivoice': ivoice, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 
            'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash
        }    
        return render(request, 'ashish_invoice_edit.html', context)
    return redirect('ashish_invoice_display')

@user_access
def ashish_add_invoice(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date = request.POST.get('date')
        invoice_date = request.POST.get('invoice_date')
        voucher_number = request.POST.get('voucher_number')
        pvn_count = request.POST.get('pvn_count')
        challan = request.POST.get('challan')
        invoice = request.POST.get('invoice')
        invoice_type = request.POST.get('invoice_type')
        location = request.POST.get('location')
        supplier = request.POST.get('supplier')
        vehicle = request.POST.get('vehicle')
        narrat = request.POST.get('narrat')
        sub_total = request.POST.get('subtotal')
        discount_per = request.POST.get('discount1')
        discount_amt = request.POST.get('discount2')
        porder = request.POST.get('porder', '').replace(" ", "").upper()
        vat = request.POST.get('vat')
        total = request.POST.get('total')
        trans = request.POST.get('trans')
        day = request.POST.get('day')
        itemadd = request.POST.getlist('itemadd')

        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''

        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            if InvoiceItem.objects.filter(item_id=itemid, po=porder).exists():
                messages.info(request, 'error')
                return redirect('ashish_purchase_invoice')

        if PurchaseEntry.objects.filter(voucher_number=voucher_number).exists():
            messages.info(request, 'error')
            return redirect('ashish_purchase_invoice')
        else:
            query = PurchaseEntry(
                entry_date=date, purchase_order_number=porder, day=day, 
                transaction_type=trans, narration=narrat, invoice_date=invoice_date, 
                invoice_type=invoice_type, voucher_number=voucher_number, 
                pvn_count=pvn_count, challan_number=challan, invoice_number=invoice, 
                location=location, supplier_id=supplier, supplier_name=sup_name, 
                supplier_address=sup_address, supplier_contact=sup_contact, 
                vehicle_number=vehicle, sub_total=sub_total, discount_per=discount_per, 
                discount_amt=discount_amt, vat=vat, total=total, 
                entry_by=current_user, user_site=u_site
            )
            query.save()
            pid = query.id

        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            alias = request.POST.get('ialias' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            rate = request.POST.get('irate' + a)
            amt = request.POST.get('iamt' + a)
            dis_amt = request.POST.get('idisamt' + a)
            dis_per = request.POST.get('idisper' + a)
            que = InvoiceItem(
                purchaseid=pid, po=porder, pvn=voucher_number, discount_amt=dis_amt, 
                discount_per=dis_per, item_id=itemid, item=item, alias=alias, 
                uom=uom, quantity=qty, orig_quantity=qty, useable_quantity=qty, 
                rate=rate, amount=amt
            )
            que.save()

        po = PurchaseOrder.objects.filter(purchase_number=porder).first()
        issuing_site_name = po.issuing_site if po else ''

        q1 = Notification(
            notify_topic='purchase_invoice_entry', content_id=pid, content='invoice_add', 
            from_site=u_site, from_user=current_user, content_val=voucher_number, 
            content_val2=issuing_site_name
        )
        q1.save()

        q2 = Notification(
            notify_topic='purchase_invoice_entry', content_id=pid, content='invoice_arrival', 
            from_site=u_site, from_user=current_user, content_val=voucher_number, 
            content_val1=porder, content_val2=issuing_site_name
        )
        q2.save()

        messages.info(request, 'done')
        return redirect('ashish_purchase_invoice')
    return redirect('ashish_purchase_invoice')

@user_access
def ashish_edit_invoice(request):
    if request.method == "POST":
        pid = request.POST.get('pid')
        date = request.POST.get('date')
        invoice_date = request.POST.get('invoice_date')
        voucher_number = request.POST.get('voucher_number')
        challan = request.POST.get('challan')
        invoice = request.POST.get('invoice')
        invoice_type = request.POST.get('invoice_type')
        location = request.POST.get('location')
        supplier = request.POST.get('supplier')
        vehicle = request.POST.get('vehicle')
        narrat = request.POST.get('narrat')
        sub_total = request.POST.get('subtotal')
        discount_per = request.POST.get('discount1')
        discount_amt = request.POST.get('discount2')
        vat = request.POST.get('vat')
        total = request.POST.get('total')
        trans = request.POST.get('trans')
        porder = request.POST.get('porder', '').replace(" ", "").upper()
        day = request.POST.get('day')
        itemadd = request.POST.getlist('itemadd')

        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''

        inviid = [a.id for a in InvoiceItem.objects.filter(purchaseid=pid)]

        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            if InvoiceItem.objects.filter(item_id=itemid, po=porder).exclude(id__in=inviid).exists():
                messages.info(request, 'error')
                return redirect('ashish_purchase_invoice')

        PurchaseEntry.objects.filter(id=pid).update(
            entry_date=date, narration=narrat, day=day, transaction_type=trans, 
            invoice_date=invoice_date, invoice_type=invoice_type, challan_number=challan, 
            invoice_number=invoice, location=location, supplier_id=supplier, 
            supplier_name=sup_name, supplier_address=sup_address, 
            supplier_contact=sup_contact, vehicle_number=vehicle, 
            sub_total=sub_total, discount_per=discount_per, discount_amt=discount_amt, 
            vat=vat, total=total
        )

        InvoiceItem.objects.filter(purchaseid=pid).delete()
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            alias = request.POST.get('ialias' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            rate = request.POST.get('irate' + a)
            amt = request.POST.get('iamt' + a)
            dis_amt = request.POST.get('idisamt' + a)
            dis_per = request.POST.get('idisper' + a)
            que = InvoiceItem(
                purchaseid=pid, po=porder, pvn=voucher_number, discount_amt=dis_amt, 
                discount_per=dis_per, item_id=itemid, item=item, alias=alias, 
                uom=uom, quantity=qty, orig_quantity=qty, useable_quantity=qty, 
                rate=rate, amount=amt
            )
            que.save()

        messages.info(request, 'done')
        return redirect('/ashish-invoice-edit/' + str(pid) + '/')
    return redirect('ashish_invoice_display')

# ==================== LEGACY GRN & INVOICES ====================
@user_access
def goods_entry(request):
    supplier_dash = Supplier.objects.all()
    location_dash = Location.objects.all()
    vehicle_dash = Vehicle.objects.all()
    porder = PurchaseOrder.objects.filter(status='approved')
    uom_dash = UOM.objects.all()
    item_dash = StockItem.objects.all()
    grn = 0
    if GoodsEntry.objects.last():
        good = GoodsEntry.objects.last()
        ng = good.grn_count
        grn = int(ng) + 1
    else:
        grn = grn + 1

    gchallan = [item['challan_number'] for item in GoodsEntry.objects.values('challan_number')]
    gbill = [item['bill_number'] for item in GoodsEntry.objects.values('bill_number')]
    
    context = {
        'porder': porder, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 
        'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 
        'grn': grn, 'gchallan': gchallan, 'gbill': gbill
    }    
    return render(request, 'goods_entry.html', context)

@user_access
def goods_display(request):
    s_item = GoodsEntry.objects.all().order_by('-id')[:30]
    context = {'s_item': s_item}    
    return render(request, 'display/goods_display.html', context)

@user_access
def goods_detail(request, gid):
    if GoodsEntry.objects.filter(id=gid).exists():
        item = GoodsEntry.objects.filter(id=gid).first()
        s_goods = Goods.objects.filter(goodsid=gid)
        context = {'item': item, 's_goods': s_goods}    
        return render(request, 'display/goods_detail.html', context)
    return redirect('goods_display')

@user_access
def search_goods(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        lookup = (
            Q(grn_number=search) | Q(challan_number=search) | Q(bill_number=search) | 
            Q(location=search) | Q(supplier_name=search) | Q(vehicle_number=search) | 
            Q(user_site=search) | Q(grn_number=sea) | Q(challan_number=sea) | 
            Q(bill_number=sea) | Q(location=sea) | Q(supplier_name=sea) | 
            Q(vehicle_number=sea) | Q(user_site=sea) | Q(grn_number=se) | 
            Q(challan_number=se) | Q(bill_number=se) | Q(location=se) | 
            Q(supplier_name=se) | Q(vehicle_number=se) | Q(user_site=se) | 
            Q(grn_number=s) | Q(challan_number=s) | Q(bill_number=s) | 
            Q(location=s) | Q(supplier_name=s) | Q(vehicle_number=s) | Q(user_site=s)
        )
        s_goods = GoodsEntry.objects.filter(lookup).order_by('-id')
        context = {'s_goods': s_goods, 'search': search}
        return render(request, 'display/goods_search.html', context)
    return redirect('goods_display')

@user_access
def print_goods(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = GoodsEntry.objects.filter(id=jid).first()
        igoods = Goods.objects.filter(goodsid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('printgoods.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportgoods_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('goods_display')

@user_access
def delete_goods(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        GoodsEntry.objects.filter(id=sid).delete()
        Goods.objects.filter(goodsid=sid).delete()
        messages.info(request, 'done')
        return redirect('goods_display')
    return redirect('goods_display')

@user_access
def goods_edit(request, gid):
    if GoodsEntry.objects.filter(id=gid).exists():
        item = GoodsEntry.objects.filter(id=gid).first()
        igoods = Goods.objects.filter(goodsid=gid)
        goods_count = list(range(1, len(igoods) + 1))

        supplier_dash = Supplier.objects.all()
        location_dash = Location.objects.all()
        vehicle_dash = Vehicle.objects.all()
        uom_dash = UOM.objects.all()
        item_dash = StockItem.objects.all()

        gchallan = [s['challan_number'] for s in GoodsEntry.objects.values('challan_number')]
        gbill = [s['bill_number'] for s in GoodsEntry.objects.values('bill_number')]
        
        context = {
            'item': item, 'igoods': igoods, 'goods_count': goods_count, 
            'supplier_dash': supplier_dash, 'location_dash': location_dash, 
            'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 
            'item_dash': item_dash, 'gchallan': gchallan, 'gbill': gbill
        }    
        return render(request, 'goods_edit.html', context)
    return redirect('goods_display')

@user_access
def add_goods(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date = request.POST.get('date')
        grn = request.POST.get('grn')
        grn_count = request.POST.get('grn_count')
        challan = request.POST.get('challan')
        bill = request.POST.get('bill')
        supplier = request.POST.get('supplier')
        vehicle = request.POST.get('vehicle')
        itemadd = request.POST.getlist('itemadd')

        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''

        if GoodsEntry.objects.filter(grn_number=grn).exists():
            messages.info(request, 'error')
            return redirect('goods_entry')
        else:
            query = GoodsEntry(
                entry_date=date, grn_number=grn, grn_count=grn_count, 
                challan_number=challan, bill_number=bill, supplier_id=supplier, 
                supplier_name=sup_name, supplier_address=sup_address, 
                supplier_contact=sup_contact, vehicle_number=vehicle, 
                entry_by=current_user, user_site=u_site
            )
            query.save()

        gid = query.id
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            remark = request.POST.get('iremark' + a)
            que = Goods(goodsid=gid, grn=grn, item_id=itemid, item=item, uom=uom, quantity=qty, remark=remark)
            que.save()

        q = Notification(
            notify_topic='grn', content_id=gid, content='grn_add', 
            from_site=u_site, from_user=current_user, content_val=grn
        )
        q.save()

        messages.info(request, 'done')
        return redirect('goods_entry')
    return redirect('goods_entry')

@user_access
def edit_goods(request):
    if request.method == "POST":
        gid = request.POST.get('gid')
        date = request.POST.get('date')
        grn = request.POST.get('grn')
        challan = request.POST.get('challan')
        bill = request.POST.get('bill')
        supplier = request.POST.get('supplier')
        vehicle = request.POST.get('vehicle')
        itemadd = request.POST.getlist('itemadd')

        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''

        GoodsEntry.objects.filter(id=gid).update(
            entry_date=date, challan_number=challan, bill_number=bill, 
            supplier_id=supplier, supplier_name=sup_name, 
            supplier_address=sup_address, supplier_contact=sup_contact, 
            vehicle_number=vehicle
        )

        Goods.objects.filter(goodsid=gid).delete()
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            remark = request.POST.get('iremark' + a)
            que = Goods(goodsid=gid, grn=grn, item_id=itemid, item=item, uom=uom, quantity=qty, remark=remark)
            que.save()
        messages.info(request, 'done')
        return redirect('/edit-goods/' + str(gid) + '/')
    return redirect('goods_display')

@user_access
def invoice_entry(request):
    supplier_dash = Supplier.objects.all()
    location_dash = Location.objects.all()
    vehicle_dash = Vehicle.objects.all()
    porder = PurchaseOrder.objects.filter(status='approved', invoice_status='no')
    uom_dash = UOM.objects.all()
    stock_item = StockEntry.objects.all()
    pvn = 0
    if PurchaseEntry.objects.last():
        good = PurchaseEntry.objects.last()
        ng = good.pvn_count
        pvn = int(ng) + 1
    else:
        pvn = pvn + 1

    ichallan = [item['challan_number'] for item in PurchaseEntry.objects.values('challan_number')]
    ivoice = [item['invoice_number'] for item in PurchaseEntry.objects.values('invoice_number')]

    igoods = []
    seen = set()
    seen_add = seen.add
    tran = Goods.objects.values('goodsid')
    trans = {item['goodsid'] for item in tran}
    for s in trans:
        igood = Goods.objects.filter(goodsid=s)
        n = len(igood)
        igoods.append([igood, range(1, n)])

    context = {
        'porder': porder, 'pvn': pvn, 'stock_item': stock_item, 
        'ichallan': ichallan, 'ivoice': ivoice, 'supplier_dash': supplier_dash, 
        'igoods': igoods, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 
        'uom_dash': uom_dash
    }    
    return render(request, 'purchase_invoice.html', context)

@user_access
def invoice_display(request):
    s_item = PurchaseEntry.objects.all().order_by('-id')[:30]
    context = {'s_item': s_item}    
    return render(request, 'display/invoice_display.html', context)

def invoice_detail(request, pid):
    if PurchaseEntry.objects.filter(id=pid).exists():
        item = PurchaseEntry.objects.filter(id=pid).first()
        s_goods = InvoiceItem.objects.filter(purchaseid=pid)
        context = {'item': item, 's_goods': s_goods}    
        return render(request, 'display/invoice_detail.html', context)
    return redirect('invoice_display')

@user_access
def search_invoice(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        lookup = (
            Q(voucher_number=search) | Q(challan_number=search) | Q(invoice_number=search) | 
            Q(invoice_type=search) | Q(location=search) | Q(supplier_name=search) | 
            Q(vehicle_number=search) | Q(user_site=search) | Q(voucher_number=sea) | 
            Q(challan_number=sea) | Q(invoice_number=sea) | Q(invoice_type=sea) | 
            Q(location=sea) | Q(supplier_name=sea) | Q(vehicle_number=sea) | 
            Q(user_site=sea) | Q(voucher_number=se) | Q(challan_number=se) | 
            Q(invoice_number=se) | Q(invoice_type=se) | Q(location=se) | 
            Q(supplier_name=se) | Q(vehicle_number=se) | Q(user_site=se) | 
            Q(voucher_number=s) | Q(challan_number=s) | Q(invoice_number=s) | 
            Q(invoice_type=s) | Q(location=s) | Q(supplier_name=s) | 
            Q(vehicle_number=s) | Q(user_site=s)
        )
        s_item = PurchaseEntry.objects.filter(lookup).order_by('-id')
        context = {'s_item': s_item, 'search': search}
        return render(request, 'display/search_invoice.html', context)
    return redirect('invoice_display')

@user_access
def print_invoice(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = PurchaseEntry.objects.filter(id=jid).first()
        igoods = InvoiceItem.objects.filter(purchaseid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('printinvoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportinvoice_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('invoice_display')

@user_access
def delete_invoice(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        PurchaseEntry.objects.filter(id=sid).delete()
        InvoiceItem.objects.filter(purchaseid=sid).delete()
        messages.info(request, 'done')
        return redirect('invoice_display')
    return redirect('invoice_display')

@user_access
def invoice_edit(request, pid):
    if PurchaseEntry.objects.filter(id=pid).exists():
        supplier_dash = Supplier.objects.all()
        location_dash = Location.objects.all()
        vehicle_dash = Vehicle.objects.all()
        uom_dash = UOM.objects.all()
        stock_item = StockEntry.objects.all()
        item = PurchaseEntry.objects.filter(id=pid).first()
        initem = InvoiceItem.objects.filter(purchaseid=pid)

        ichallan = [s['challan_number'] for s in PurchaseEntry.objects.values('challan_number')]
        ivoice = [s['invoice_number'] for s in PurchaseEntry.objects.values('invoice_number')]

        igoods = []
        tran = Goods.objects.values('goodsid')
        trans = {s['goodsid'] for s in tran}
        for s in trans:
            igood = Goods.objects.filter(goodsid=s)
            n = len(igood)
            igoods.append([igood, range(1, n)])

        invitem = []
        tran = InvoiceItem.objects.values('grn')
        trans = {s['grn'] for s in tran}
        for s in trans:
            inv = InvoiceItem.objects.filter(grn=s, purchaseid=pid)
            n = len(inv)
            invitem.append([inv, range(1, n)])

        seen = set()
        seen_add = seen.add
        tran = InvoiceItem.objects.values_list('grn', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        inv_count = []
        for b in ent:
            que = InvoiceItem.objects.filter(grn=b, purchaseid=pid)
            for i in que:
                inv_count.append(i.grn)

        context = {
            'item': item, 'inv_count': inv_count, 'invitem': invitem, 
            'initem': initem, 'stock_item': stock_item, 'ichallan': ichallan, 
            'ivoice': ivoice, 'supplier_dash': supplier_dash, 'igoods': igoods, 
            'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 
            'uom_dash': uom_dash
        }    
        return render(request, 'invoice_edit.html', context)
    return redirect('invoice_display')

@user_access
def add_invoice(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date = request.POST.get('date')
        invoice_date = request.POST.get('invoice_date')
        voucher_number = request.POST.get('voucher_number')
        pvn_count = request.POST.get('pvn_count')
        challan = request.POST.get('challan')
        invoice = request.POST.get('invoice')
        invoice_type = request.POST.get('invoice_type')
        location = request.POST.get('location')
        supplier = request.POST.get('supplier')
        vehicle = request.POST.get('vehicle')
        sub_total = request.POST.get('subtotal')
        discount_per = request.POST.get('discount1')
        discount_amt = request.POST.get('discount2')
        vat = request.POST.get('vat')
        total = request.POST.get('total')
        itemadd = request.POST.getlist('itemadd')

        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''

        if PurchaseEntry.objects.filter(voucher_number=voucher_number).exists():
            messages.info(request, 'error')
            return redirect('purchase_invoice')
        else:
            query = PurchaseEntry(
                entry_date=date, invoice_date=invoice_date, invoice_type=invoice_type, 
                voucher_number=voucher_number, pvn_count=pvn_count, challan_number=challan, 
                invoice_number=invoice, location=location, supplier_id=supplier, 
                supplier_name=sup_name, supplier_address=sup_address, 
                supplier_contact=sup_contact, vehicle_number=vehicle, 
                sub_total=sub_total, discount_per=discount_per, discount_amt=discount_amt, 
                vat=vat, total=total, entry_by=current_user, user_site=u_site
            )
            query.save()

        pid = query.id
        for a in itemadd:
            a = str(a)
            grn = request.POST.get('igrn' + a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            rate = request.POST.get('irate' + a)
            amt = request.POST.get('iamt' + a)
            que = InvoiceItem(purchaseid=pid, pvn=voucher_number, grn=grn, item_id=itemid, item=item, uom=uom, quantity=qty, rate=rate, amount=amt)
            que.save()
            GoodsEntry.objects.filter(grn_number=grn).update(invoice_id=pid, invoice_status="yes")

        q = Notification(
            notify_topic='purchase_invoice_entry', content_id=pid, content='invoice_add', 
            from_site=u_site, from_user=current_user, content_val=voucher_number
        )
        q.save()

        messages.info(request, 'done')
        return redirect('purchase_invoice')
    return redirect('purchase_invoice')

@user_access
def edit_invoice(request):
    if request.method == "POST":
        pid = request.POST.get('pid')
        date = request.POST.get('date')
        invoice_date = request.POST.get('invoice_date')
        voucher_number = request.POST.get('voucher_number')
        challan = request.POST.get('challan')
        invoice = request.POST.get('invoice')
        invoice_type = request.POST.get('invoice_type')
        location = request.POST.get('location')
        supplier = request.POST.get('supplier')
        vehicle = request.POST.get('vehicle')
        sub_total = request.POST.get('subtotal')
        discount_per = request.POST.get('discount1')
        discount_amt = request.POST.get('discount2')
        vat = request.POST.get('vat')
        total = request.POST.get('total')
        itemadd = request.POST.getlist('itemadd')

        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''

        PurchaseEntry.objects.filter(id=pid).update(
            entry_date=date, invoice_date=invoice_date, invoice_type=invoice_type, 
            challan_number=challan, invoice_number=invoice, location=location, 
            supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, 
            supplier_contact=sup_contact, vehicle_number=vehicle, sub_total=sub_total, 
            discount_per=discount_per, discount_amt=discount_amt, vat=vat, total=total
        )

        InvoiceItem.objects.filter(purchaseid=pid).delete()
        for a in itemadd:
            a = str(a)
            grn = request.POST.get('igrn' + a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            rate = request.POST.get('irate' + a)
            amt = request.POST.get('iamt' + a)
            que = InvoiceItem(purchaseid=pid, pvn=voucher_number, grn=grn, item_id=itemid, item=item, uom=uom, quantity=qty, rate=rate, amount=amt)
            que.save()

        messages.info(request, 'done')
        return redirect('/invoice-edit/' + str(pid) + '/')
    return redirect('invoice_display')

# ==================== PURCHASE ORDERS ====================
@user_access
def purchase_order(request):
    supplier_dash = Supplier.objects.all()
    location_dash = Location.objects.all()
    v_type = VehicleType.objects.all()
    uom_dash = UOM.objects.all()
    u_site = user_site(request)
    item_dash = StockItem.objects.all()
    pon = 0
    if PurchaseOrder.objects.exists():
        po_counts = PurchaseOrder.objects.values_list('pon_count', flat=True)
        numbers = [int(num) for num in list(po_counts) if str(num).isdigit()]
        pon = max(numbers) + 1 if numbers else 1
    else:
        pon = 1

    vehis = []
    seen = set()
    seen_add = seen.add
    ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for e in ent:
        vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
        n = len(vehi)
        vehis.append([vehi, range(1, n)])

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
    psupa = []
    seen = set()
    seen_add = seen.add
    tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for r in ent:
        ps = StockSubCategory.objects.filter(cat_url=r)
        n = len(ps)
        psupa.append([ps, range(1, n)])

    context = {
        'vehis': vehis, 'stock_cat': stock_cat, 'psupa': psupa, 
        'itemsel': itemsel, 'v_type': v_type, 'supplier_dash': supplier_dash, 
        'location_dash': location_dash, 'uom_dash': uom_dash, 
        'item_dash': item_dash, 'pon': pon, 'u_site': u_site
    }    
    return render(request, 'purchase_order.html', context)

@user_access
def purchase_order_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = PurchaseOrder.objects.all().order_by('-id')
    else:
        s_it = PurchaseOrder.objects.filter(user_site=u_site).order_by('-id')
    
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
    return render(request, 'display/purchase_order_display.html', context)

@user_access
def purchase_order_detail(request, gid):
    if PurchaseOrder.objects.filter(id=gid).exists():
        site_dash = Site.objects.filter(active_status='yes')
        item = PurchaseOrder.objects.filter(id=gid).first()
        s_goods = PurchaseItem.objects.filter(purchase_order_id=gid)
        context = {'item': item, 's_goods': s_goods, 'site_dash': site_dash}    
        return render(request, 'display/purchase_order_detail.html', context)
    return redirect('purchase_order_display')

@user_access
def search_purchase_order(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(purchase_number=search) | Q(issuing_site__icontains=search) | 
                Q(narration__icontains=search) | Q(purchase_number=sea) | 
                Q(issuing_site=sea) | Q(purchase_number=se) | 
                Q(issuing_site=se) | Q(purchase_number=s) | Q(issuing_site=s)
            )
        else:
            lookup = (
                Q(Q(purchase_number=search) | Q(purchase_number=sea) | 
                  Q(purchase_number=se) | Q(purchase_number=s) | 
                  Q(narration__icontains=search)) & Q(user_site=u_site)
            )
        s_goods = []
        s_goo = PurchaseOrder.objects.filter(lookup).order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(s_goo, 30)
        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)
        n = len(product)
        s_goods.append([product, range(1, n)])
        context = {'s_goods': s_goods, 'search': search}
        return render(request, 'display/purchase_order_search.html', context)
    return redirect('purchase_order_display')

@user_access
def print_purchase_order(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = PurchaseOrder.objects.filter(id=jid).first()
        igoods = PurchaseItem.objects.filter(purchase_order_id=jid)
        letterhead = get_active_letterhead(s_good.issuing_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('print_purchase_order.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportgoods_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('purchase_order_display')

@user_access
def delete_purchase_order(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        PurchaseOrder.objects.filter(id=sid).delete()
        PurchaseItem.objects.filter(purchase_order_id=sid).delete()
        messages.info(request, 'done')
        return redirect('purchase_order_display')
    return redirect('purchase_order_display')

@user_access
def cancel_purchase_order(request, pid):
    if PurchaseOrder.objects.filter(id=pid).exists():
        current_user = request.user.username
        u_site = user_site(request)
        p = PurchaseOrder.objects.filter(id=pid).first()
        pon = p.purchase_number
        if GoodsEntry.objects.filter(purchase_order_number=pon).exists() or PurchaseEntry.objects.filter(purchase_order_number=pon).exists():
            messages.info(request, 'error')
            return redirect('/purchase-order-detail/' + str(pid) + '/')

        us_site = p.user_site
        PurchaseOrder.objects.filter(id=pid).update(cancelled_by=current_user, status="cancelled")

        q = Notification(
            notify_topic='purchase_order', content_id=pid, content='purchase_order_cancel', 
            from_site=u_site, from_user=current_user, content_val=pon, content_val3=us_site
        )
        q.save()

        messages.info(request, 'done')
        return redirect('/purchase-order-detail/' + str(pid) + '/')
    return redirect('purchase_order_display')

@user_access
def approve_purchase_order(request):
    if request.method == "POST":
        pid = request.POST.get('pid')
        current_user = request.user.username
        u_site = user_site(request)

        p = PurchaseOrder.objects.filter(id=pid).first()
        pon = p.purchase_number
        us_site = p.user_site
        items = PurchaseItem.objects.filter(purchase_order_id=pid)
        for i in items:
            iid = i.id
            iname = i.item
            plocate = request.POST.get('plocate' + str(iid))
            PurchaseItem.objects.filter(id=iid).update(purchase_location=plocate)

            q_loc = Notification(
                notify_topic='purchase_order', content_id=pid, 
                content='purchase_order_approve_location', from_site=u_site, 
                from_user=current_user, content_val=pon, content_val1=iname, 
                content_val2=plocate
            )
            q_loc.save()

        PurchaseOrder.objects.filter(id=pid).update(approved_by=current_user, status="approved")

        q_appr = Notification(
            notify_topic='purchase_order', content_id=pid, 
            content='purchase_order_approve', from_site=u_site, 
            from_user=current_user, content_val=pon, content_val3=us_site
        )
        q_appr.save()

        messages.info(request, 'done')
        return redirect('/purchase-order-detail/' + str(pid) + '/')
    return redirect('purchase_order_display')

@user_access
def purchase_order_edit(request, gid):
    if PurchaseOrder.objects.filter(id=gid).exists():
        item = PurchaseOrder.objects.filter(id=gid).first()
        igoods = PurchaseItem.objects.filter(purchase_order_id=gid)
        goods_count = list(range(1, len(igoods) + 1))

        supplier_dash = Supplier.objects.all()
        location_dash = Location.objects.all()
        vehicle_dash = Vehicle.objects.all()
        uom_dash = UOM.objects.all()
        item_dash = StockItem.objects.all()
        v_type = VehicleType.objects.all()

        vehis = []
        seen = set()
        seen_add = seen.add
        ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
        ent = [x for x in ent if not (x in seen or seen_add(x))]
        for e in ent:
            vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
            n = len(vehi)
            vehis.append([vehi, range(1, n)])

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
        psupa = []
        seen = set()
        seen_add = seen.add
        tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for r in ent:
            ps = StockSubCategory.objects.filter(cat_url=r)
            n = len(ps)
            psupa.append([ps, range(1, n)])

        context = {
            'item': item, 'stock_cat': stock_cat, 'psupa': psupa, 
            'itemsel': itemsel, 'igoods': igoods, 'v_type': v_type, 
            'vehis': vehis, 'goods_count': goods_count, 'supplier_dash': supplier_dash, 
            'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 
            'uom_dash': uom_dash, 'item_dash': item_dash
        }    
        return render(request, 'edit_purchase_order.html', context)
    return redirect('purchase_order_display')

@user_access
def add_purchase_order(request):
    if request.method == "POST":
        current_user = request.user.username
        date = request.POST.get('date')
        pon = request.POST.get('pon')
        pon_count = request.POST.get('pon_count')
        issue_site = request.POST.get('issue_site')
        po = request.POST.get('po')
        narrat = request.POST.get('narrat')
        itemadd = request.POST.getlist('itemadd')
        u_site = user_site(request)
        vehi_type = ''
        vehi_type_id = ''
        vehi_num = ''
        num_type = ''

        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            if not StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
                messages.info(request, 'error')
                return redirect('purchase_order')

        if po == 'yes':
            vehi_type = request.POST.get('vehicle_type')
            vehi_type_id = request.POST.get('vehicle_type_id')
            vehi_num = request.POST.get('vehicle')
            num_type = request.POST.get('num_type')

        if PurchaseOrder.objects.filter(purchase_number=pon).exists():
            messages.info(request, 'error')
            return redirect('purchase_order')
        else:
            query = PurchaseOrder(
                entry_date=date, purchase_number=pon, po_vehi=po, 
                vehicle_type=vehi_type, vehicle_type_id=vehi_type_id, 
                vehicle_number=vehi_num, number_type=num_type, narration=narrat, 
                pon_count=pon_count, issuing_site=issue_site, entry_by=current_user, 
                user_site=u_site
            )
            query.save()

        gid = query.id
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            alias = request.POST.get('ialias' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            desc = request.POST.get('idesc' + a)
            que = PurchaseItem(
                purchase_order_id=gid, pon=pon, description=desc, 
                item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty
            )
            que.save()

        pr = Site.objects.filter(role='admin', active_status='yes').first()
        content_val2_site = pr.name if pr else ''

        q = Notification(
            notify_topic='purchase_order', content_id=gid, content='purchase_order_add', 
            from_site=u_site, from_user=current_user, content_val=pon, content_val2=content_val2_site
        )
        q.save()

        messages.info(request, 'done')
        return redirect('purchase_order')
    return redirect('purchase_order')

@user_access
def edit_purchase_order(request):
    if request.method == "POST":
        gid = request.POST.get('gid')
        date = request.POST.get('date')
        pon = request.POST.get('pon')
        po = request.POST.get('po')
        narrat = request.POST.get('narrat')
        issue_site = request.POST.get('issue_site')
        itemadd = request.POST.getlist('itemadd')
        vehi_type = ''
        vehi_type_id = ''
        vehi_num = ''
        num_type = ''

        ge = PurchaseOrder.objects.filter(id=gid).first()
        if not ge:
            return redirect('purchase_order_display')
        u_site = ge.issuing_site

        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            if not StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
                messages.info(request, 'error')
                return redirect('/purchase-order-edit/' + str(gid) + '/')

        if po == 'yes':
            vehi_type = request.POST.get('vehicle_type')
            vehi_type_id = request.POST.get('vehicle_type_id')
            vehi_num = request.POST.get('vehicle')
            num_type = request.POST.get('num_type')
        
        PurchaseOrder.objects.filter(id=gid).update(
            entry_date=date, narration=narrat, po_vehi=po, 
            vehicle_type=vehi_type, vehicle_type_id=vehi_type_id, 
            vehicle_number=vehi_num, number_type=num_type, issuing_site=issue_site
        )

        PurchaseItem.objects.filter(purchase_order_id=gid).delete()
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            uom = request.POST.get('iuom' + a)
            alias = request.POST.get('ialias' + a)
            qty = request.POST.get('iqty' + a)
            desc = request.POST.get('idesc' + a)
            que = PurchaseItem(
                purchase_order_id=gid, description=desc, pon=pon, 
                item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty
            )
            que.save()

        messages.info(request, 'done')
        return redirect('/purchase-order-edit/' + str(gid) + '/')
    return redirect('purchase_order_display')

# ==================== QUOTATIONS ====================
@user_access
def quotation_entry(request):
    supplier_dash = Supplier.objects.all()
    uom_dash = UOM.objects.all()
    item_dash = StockItem.objects.all()
    qsupplier = [item['supplier'] for item in QuotationEntry.objects.values('supplier')]

    context = {
        'supplier_dash': supplier_dash, 'uom_dash': uom_dash, 
        'item_dash': item_dash, 'qsupplier': qsupplier
    }    
    return render(request, 'quotation_entry.html', context)

@user_access
def quotation_display(request):
    s_item = QuotationEntry.objects.all().order_by('-id')[:30]
    context = {'s_item': s_item}    
    return render(request, 'display/quotation_display.html', context)

@user_access
def quotation_detail(request, gid):
    if QuotationEntry.objects.filter(id=gid).exists():
        item = QuotationEntry.objects.filter(id=gid).first()
        s_goods = QuotationItem.objects.filter(quotationid=gid)
        context = {'item': item, 's_goods': s_goods}    
        return render(request, 'display/quotation_detail.html', context)
    return redirect('quotation_display')

@user_access
def search_quotation(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        lookup = Q(supplier_name=search) | Q(supplier_name=sea) | Q(supplier_name=se) | Q(supplier_name=s)
        s_goods = QuotationEntry.objects.filter(lookup).order_by('-id')
        context = {'s_goods': s_goods, 'search': search}
        return render(request, 'display/quotation_search.html', context)
    return redirect('quotation_display')

@user_access
def print_quotation(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = QuotationEntry.objects.filter(id=jid).first()
        igoods = QuotationItem.objects.filter(quotationid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('printquotation.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportquotation_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('quotation_display')

@user_access
def delete_quotation(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        QuotationEntry.objects.filter(id=sid).delete()
        QuotationItem.objects.filter(quotationid=sid).delete()
        messages.info(request, 'done')
        return redirect('quotation_display')
    return redirect('quotation_display')

@user_access
def quotation_edit(request, gid):
    if QuotationEntry.objects.filter(id=gid).exists():
        item = QuotationEntry.objects.filter(id=gid).first()
        igoods = QuotationItem.objects.filter(quotationid=gid)
        goods_count = list(range(1, len(igoods) + 1))
        supplier_dash = Supplier.objects.all()
        uom_dash = UOM.objects.all()
        item_dash = StockItem.objects.all()
        qsupplier = [s['supplier'] for s in QuotationEntry.objects.values('supplier')]

        context = {
            'item': item, 'igoods': igoods, 'goods_count': goods_count, 
            'supplier_dash': supplier_dash, 'uom_dash': uom_dash, 
            'item_dash': item_dash, 'qsupplier': qsupplier
        }    
        return render(request, 'quotation_edit.html', context)
    return redirect('quotation_display')

@user_access
def add_quotation(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date = request.POST.get('date')
        valid_date = request.POST.get('valid_date')
        supplier = request.POST.get('supplier')
        itemadd = request.POST.getlist('itemadd')
        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''

        if QuotationEntry.objects.filter(supplier=supplier).exists():
            messages.info(request, 'error')
            return redirect('quotation_entry')
        else:
            query = QuotationEntry(
                entry_date=date, valid_date=valid_date, supplier=supplier, 
                supplier_name=sup_name, supplier_address=sup_address, 
                supplier_contact=sup_contact, entry_by=current_user, user_site=u_site
            )
            query.save()

        gid = query.id
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            uom = request.POST.get('iuom' + a)
            rate = request.POST.get('irate' + a)
            que = QuotationItem(quotationid=gid, item_id=itemid, item=item, uom=uom, rate=rate)
            que.save()
        messages.info(request, 'done')
        return redirect('quotation_entry')
    return redirect('quotation_entry')

@user_access
def edit_quotation(request):
    if request.method == "POST":
        gid = request.POST.get('gid')
        date = request.POST.get('date')
        valid_date = request.POST.get('valid_date')
        supplier = request.POST.get('supplier')
        itemadd = request.POST.getlist('itemadd')
        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''

        QuotationEntry.objects.filter(id=gid).update(
            entry_date=date, valid_date=valid_date, supplier_id=supplier, 
            supplier_name=sup_name, supplier_address=sup_address, 
            supplier_contact=sup_contact, entry_by=request.user.username
        )

        QuotationItem.objects.filter(quotationid=gid).delete()
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            uom = request.POST.get('iuom' + a)
            rate = request.POST.get('irate' + a)
            que = QuotationItem(quotationid=gid, item_id=itemid, item=item, uom=uom, rate=rate)
            que.save()
        messages.info(request, 'done')
        return redirect('/quotation-edit/' + str(gid) + '/')
    return redirect('quotation_display')