import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import user_passes_test

from eproc.models import (
    StockCategory, StockSubCategory, StockItem, StockEntry, 
    UOM, Site, Location, Vehicle, PurchaseOrder, PurchaseEntry,
    InvoiceItem, MaterialIssueEntry, MaterialItem, InternalTransfer, 
    TransferItem, InternalGrn, InternalGrnItems, OutSaleEntry, 
    SalesItem, Notification, Goods, MaintainanceItem, DamageItem, 
    ReturnItem, InternalDamageItem, InternalDamageEntry, Supplier,
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

# ==================== STOCK ITEMS & INVENTORY ====================
@user_access
def stock(request):
    s_item = StockItem.objects.all().count()
    s_cat = StockCategory.objects.all().count()
    context = {'s_item': s_item, 's_cat': s_cat}    
    return render(request, 'stock_dash.html', context)

@user_access
def stock_entry(request):
    s_item = StockEntry.objects.all().count()
    s_cat = StockCategory.objects.all().count()
    stock_cat = StockCategory.objects.all()
    uom_dash = UOM.objects.all()
    site_dash = Site.objects.filter(active_status='yes')
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
        's_item': s_item, 'psupa': psupa, 'site_dash': site_dash, 
        's_cat': s_cat, 'stock_cat': stock_cat, 'uom_dash': uom_dash
    }    
    return render(request, 'stock_entry.html', context)

@user_access
def add_stock(request):
    if request.method == "POST":
        current_user = request.user.username
        name = request.POST.get('name')
        url = request.POST.get('url')
        alias = request.POST.get('alias')
        stock_cat = request.POST.get('stock_category')
        caturl = request.POST.get('categoryurl')
        stock_subcat = request.POST.get('subcategory')
        subcaturl = request.POST.get('subcategoryurl')
        mainurl = request.POST.get('mainurl')
        stock_type = request.POST.get('stock_type')
        uom = request.POST.get('uom')
        surl = request.POST.getlist('sites')
        u_site = user_site(request)

        if StockItem.objects.filter(url=url).exists():
            q = StockItem.objects.filter(url=url).first()
            item_id = q.id
        else:
            query = StockItem(
                item=name, url=url, alias=alias, stock_category=stock_cat, 
                stock_subcategory=stock_subcat, cat_url=caturl, 
                subcat_url=subcaturl, main_url=mainurl, uom=uom, 
                stock_type=stock_type, entry_by=current_user, user_site=u_site
            )
            query.save()
            item_id = query.id

        if surl:
            for s in surl:
                s_site = request.POST.get('site_name' + str(s))
                qty = request.POST.get('qty' + str(s))
                rate = request.POST.get('rate' + str(s))
                amt = request.POST.get('amt' + str(s))

                if not StockEntry.objects.filter(url=url, stock_site=s_site).exists():
                    query_se = StockEntry(
                        item=name, item_id=item_id, url=url, stock_site=s_site, 
                        alias=alias, stock_category=stock_cat, stock_subcategory=stock_subcat, 
                        cat_url=caturl, subcat_url=subcaturl, uom=uom, opening=qty, 
                        quantity=qty, rate=rate, amount=amt, stock_type=stock_type, 
                        entry_by=current_user, user_site=u_site
                    )
                    query_se.save()

        sites = Site.objects.filter(active_status='yes')
        for s in sites:
            s_site = s.name
            if not StockEntry.objects.filter(url=url, stock_site=s_site).exists():
                query_se = StockEntry(
                    item=name, item_id=item_id, url=url, stock_site=s_site, 
                    alias=alias, stock_category=stock_cat, stock_subcategory=stock_subcat, 
                    cat_url=caturl, subcat_url=subcaturl, uom=uom, opening=0, 
                    quantity=0, rate=0, amount=0, stock_type=stock_type, 
                    entry_by=current_user, user_site=u_site
                )
                query_se.save()

        messages.info(request, 'done')
        return redirect('stock_entry')
    return redirect('stock_entry')

@user_access
def stock_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = StockEntry.objects.all()
    else:
        s_it = StockEntry.objects.filter(stock_site=u_site)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(s_it, 200)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    n = len(product)
    s_item.append([product, range(1, n)])

    stock_cat = StockCategory.objects.all()
    uom_dash = UOM.objects.all()
    site_dash = Site.objects.filter(active_status='yes')
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
        's_item': s_item, 'psupa': psupa, 'site_dash': site_dash, 
        'stock_cat': stock_cat, 'uom_dash': uom_dash
    }    
    return render(request, 'display/stock_display.html', context)

@user_access
def stock_item_display(request):
    s_item = StockItem.objects.all()
    stock_cat = StockCategory.objects.all()
    uom_dash = UOM.objects.all()
    site_dash = Site.objects.filter(active_status='yes')
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
        's_item': s_item, 'psupa': psupa, 'site_dash': site_dash, 
        'stock_cat': stock_cat, 'uom_dash': uom_dash
    }    
    return render(request, 'display/stock_item_display.html', context)

@user_access
def search_stock_item(request):
    if request.method == "POST":
        search = request.POST.get('search')
        scat = request.POST.get('searchcat')
        sscat = request.POST.get('searchsubcat')
        ssite = request.POST.get('searchsite')
        s_item = StockEntry.objects.all()
        if scat:
            s_item = s_item.filter(stock_category=scat).order_by('-id')
        if sscat:
            s_item = s_item.filter(stock_subcategory=sscat).order_by('-id')
        if ssite:
            s_item = s_item.filter(stock_site=ssite).order_by('-id')
        if search:
            s_item = s_item.filter(item__icontains=search).order_by('-id')
        
        stock_cat = StockCategory.objects.all()
        uom_dash = UOM.objects.all()
        site_dash = Site.objects.filter(active_status='yes')
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
            's_item': s_item, 'psupa': psupa, 'site_dash': site_dash, 
            'search': search, 'scat': scat, 'sscat': sscat, 'ssite': ssite, 
            'stock_cat': stock_cat, 'uom_dash': uom_dash
        }
        return render(request, 'display/stock_search.html', context)
    return redirect('stock_display')

@user_access
def search_item(request):
    if request.method == "POST":
        search = request.POST.get('search')
        scat = request.POST.get('searchcat')
        sscat = request.POST.get('searchsubcat')
        s_item = StockItem.objects.all()
        if scat:
            s_item = s_item.filter(stock_category=scat).order_by('-id')
        if sscat:
            s_item = s_item.filter(stock_subcategory=sscat).order_by('-id')
        if search:
            s_item = s_item.filter(item__icontains=search).order_by('-id')
        
        stock_cat = StockCategory.objects.all()
        uom_dash = UOM.objects.all()
        site_dash = Site.objects.filter(active_status='yes')
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
            's_item': s_item, 'psupa': psupa, 'site_dash': site_dash, 
            'scat': scat, 'sscat': sscat, 'search': search, 
            'stock_cat': stock_cat, 'uom_dash': uom_dash
        }
        return render(request, 'display/stock_search_item.html', context)
    return redirect('stock_item_display')

@user_access
def update_stock(request):
    if request.method == "POST":
        sid = request.POST.get('suid')
        url = request.POST.get('url')
        opening = request.POST.get('opening')
        quantity = request.POST.get('quantity')
        rate = request.POST.get('rate')
        amount = request.POST.get('amount')
        s_site = request.POST.get('site')

        if StockEntry.objects.filter(url=url, stock_site=s_site).exclude(id=sid).exists():
            messages.info(request, 'error')
            return redirect('stock_display')
        else:
            StockEntry.objects.filter(id=sid).update(opening=opening, quantity=quantity, rate=rate, amount=amount)
            messages.info(request, 'done')
            return redirect('stock_display')
    return redirect('stock_display')

@user_access
def update_stock_item(request):
    if request.method == "POST":
        sid = request.POST.get('suid')
        name = request.POST.get('name')
        dname = request.POST.get('dname')
        dalias = request.POST.get('dalias')
        duom = request.POST.get('duom')
        url = request.POST.get('url')
        alias = request.POST.get('alias')
        stock_cat = request.POST.get('category')
        stock_subcat = request.POST.get('subcategory')
        stock_type = request.POST.get('type')
        uom = request.POST.get('uom')
        
        sc = StockCategory.objects.filter(name=stock_cat).first()
        scurl = sc.url if sc else ''
        scc = StockSubCategory.objects.filter(cat_name=stock_cat, name=stock_subcat).first()
        sscurl = scc.url if scc else ''
        murl = str(scurl) + '' + str(sscurl)

        if StockItem.objects.filter(url=url).exclude(id=sid).exists():
            messages.info(request, 'error')
            return redirect('stock_display')
        else:
            StockItem.objects.filter(id=sid).update(
                item=name, url=url, alias=alias, stock_category=stock_cat, 
                stock_subcategory=stock_subcat, cat_url=scurl, subcat_url=sscurl, 
                main_url=murl, uom=uom, stock_type=stock_type
            )
            StockEntry.objects.filter(item_id=sid).update(
                item=name, url=url, alias=alias, stock_category=stock_cat, 
                stock_subcategory=stock_subcat, cat_url=scurl, subcat_url=sscurl, 
                uom=uom, stock_type=stock_type
            )
            if name != dname:
                Goods.objects.filter(item_id=sid).update(item=name)
                InvoiceItem.objects.filter(item_id=sid).update(item=name)
                MaterialItem.objects.filter(item_id=sid).update(item=name)
                TransferItem.objects.filter(item_id=sid).update(item=name)
                InternalGrnItems.objects.filter(item_id=sid).update(item=name)
                MaintainanceItem.objects.filter(item_id=sid).update(item_name=name)
                DamageItem.objects.filter(item_id=sid).update(item=name)
                ReturnItem.objects.filter(item_id=sid).update(item=name)
                InternalDamageItem.objects.filter(item_id=sid).update(item=name)
            if alias != dalias:
                Goods.objects.filter(item_id=sid).update(alias=alias)
                InvoiceItem.objects.filter(item_id=sid).update(alias=alias)
                MaterialItem.objects.filter(item_id=sid).update(alias=alias)
                TransferItem.objects.filter(item_id=sid).update(alias=alias)
                InternalGrnItems.objects.filter(item_id=sid).update(alias=alias)
                MaintainanceItem.objects.filter(item_id=sid).update(alias=alias)
                DamageItem.objects.filter(item_id=sid).update(alias=alias)
                ReturnItem.objects.filter(item_id=sid).update(alias=alias)
                InternalDamageItem.objects.filter(item_id=sid).update(alias=alias)
            if uom != duom:
                Goods.objects.filter(item_id=sid).update(uom=uom)
                InvoiceItem.objects.filter(item_id=sid).update(uom=uom)
                MaterialItem.objects.filter(item_id=sid).update(uom=uom)
                TransferItem.objects.filter(item_id=sid).update(uom=uom)
                InternalGrnItems.objects.filter(item_id=sid).update(uom=uom)
                MaintainanceItem.objects.filter(item_id=sid).update(uom=uom)
                DamageItem.objects.filter(item_id=sid).update(uom=uom)
                ReturnItem.objects.filter(item_id=sid).update(uom=uom)
                InternalDamageItem.objects.filter(item_id=sid).update(uom=uom)

            messages.info(request, 'done')
            return redirect('stock_item_display')
    return redirect('stock_item_display')

@user_access
def delete_stock(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        StockEntry.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('stock_display')
    return redirect('stock_display')

@user_access
def delete_stock_item(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        StockItem.objects.filter(id=sid).delete()
        StockEntry.objects.filter(item_id=sid).delete()
        messages.info(request, 'done')
        return redirect('stock_item_display')
    return redirect('stock_item_display')

@user_access
def stock_category(request):
    category_dash = StockCategory.objects.all()
    subcategory_dash = StockSubCategory.objects.all()
    context = {'category_dash': category_dash, 'psupa': [], 'subcategory_dash': subcategory_dash}    
    return render(request, 'stock_category.html', context)

@user_access
def add_stock_category(request):
    if request.method == "POST":
        name = request.POST.get('name')
        url = request.POST.get('url')
        current_user = request.user.username
        u_site = user_site(request)

        if StockCategory.objects.filter(url=url).exists():
            messages.info(request, 'error')
            return redirect('manage_stock_category')
        else:
            query = StockCategory(name=name, url=url, entry_by=current_user, user_site=u_site)
            query.save()
            messages.info(request, 'done')
            return redirect('manage_stock_category')
    return redirect('manage_stock_category')

@user_access
def edit_stock_category(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        default = request.POST.get('default')
        name = request.POST.get('name')
        url = request.POST.get('url')
        urlcol = []
        stc = StockCategory.objects.get(id=lid)
        stc_url = stc.url
        stcs = StockSubCategory.objects.filter(cat_url=stc_url)
        for s in stcs:
            stcs_url = s.url
            murl = str(stc_url) + '' + str(stcs_url)
            nmurl = str(url) + '' + str(stcs_url)
            urlcol.append([murl, nmurl])

        if StockCategory.objects.filter(url=url).exclude(id=lid).exists():
            messages.info(request, 'error')
            return redirect('manage_stock_category')
        else:
            StockCategory.objects.filter(id=lid).update(name=name, url=url)
            if StockItem.objects.filter(stock_category=default).exists():
                StockItem.objects.filter(stock_category=default).update(stock_category=name, cat_url=url)
                for key, value in urlcol:
                    if StockItem.objects.filter(main_url=key).exists():
                        StockItem.objects.filter(main_url=key).update(main_url=value)
            if StockEntry.objects.filter(stock_category=default).exists():
                StockEntry.objects.filter(stock_category=default).update(stock_category=name, cat_url=url)
            if StockSubCategory.objects.filter(cat_name=default).exists():
                StockSubCategory.objects.filter(cat_name=default).update(cat_name=name, cat_url=url)
            messages.info(request, 'done')
            return redirect('manage_stock_category')
    return redirect('manage_stock_category')

@user_access
def delete_stock_category(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        stk = StockCategory.objects.filter(id=lid).first()
        if stk:
            urll = stk.url
            StockCategory.objects.filter(id=lid).delete()
            if StockSubCategory.objects.filter(cat_url=urll).exists():
                StockSubCategory.objects.filter(cat_url=urll).delete()
            messages.info(request, 'done')
        return redirect('manage_stock_category')
    return redirect('manage_stock_category')

@user_access
def add_stock_subcategory(request):
    if request.method == "POST":
        name = request.POST.get('name')
        cat = request.POST.get('stock_category')
        url = request.POST.get('url')
        caturl = request.POST.get('caturl')
        current_user = request.user.username
        u_site = user_site(request)

        if StockSubCategory.objects.filter(cat_url=caturl, url=url).exists():
            messages.info(request, 'error')
            return redirect('manage_stock_category')
        else:
            query = StockSubCategory(name=name, url=url, cat_name=cat, cat_url=caturl, entry_by=current_user, user_site=u_site)
            query.save()
            messages.info(request, 'done')
            return redirect('manage_stock_category')
    return redirect('manage_stock_category')

@user_access
def edit_stock_subcategory(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        name = request.POST.get('name')
        cat = request.POST.get('stock_category')
        url = request.POST.get('url')
        caturl = request.POST.get('caturl')
        default = request.POST.get('default')
        stcs = StockSubCategory.objects.get(id=lid)
        stcs_url = stcs.url
        stc_url = stcs.cat_url
        murl = str(stc_url) + '' + str(stcs.url)
        nmurl = str(caturl if caturl != stc_url else stc_url) + '' + str(url)

        if StockSubCategory.objects.filter(cat_url=caturl, url=url).exclude(id=lid).exists():
            messages.info(request, 'error')
            return redirect('manage_stock_category')
        else:
            StockSubCategory.objects.filter(id=lid).update(cat_name=cat, cat_url=caturl, name=name, url=url)
            if StockItem.objects.filter(stock_subcategory=default).exists():
                StockItem.objects.filter(stock_subcategory=default).update(stock_subcategory=name, subcat_url=url)
                if StockItem.objects.filter(main_url=murl).exists():
                    StockItem.objects.filter(main_url=murl).update(main_url=nmurl)
            if StockEntry.objects.filter(stock_subcategory=default).exists():
                StockEntry.objects.filter(stock_subcategory=default).update(stock_subcategory=name, subcat_url=url)
            messages.info(request, 'done')
            return redirect('manage_stock_category')
    return redirect('manage_stock_category')

@user_access
def delete_stock_subcategory(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        StockSubCategory.objects.filter(id=lid).delete()
        messages.info(request, 'done')
        return redirect('manage_stock_category')
    return redirect('manage_stock_category')

# ==================== MATERIAL ISSUE ====================
@user_access
def material_issue(request):
    vehicle_dash = Vehicle.objects.all()
    u_site = user_site(request)
    porder = PurchaseOrder.objects.all().exclude(po_vehi='yes')
    item_real = StockItem.objects.all()
    item_dash = StockEntry.objects.filter(stock_site=u_site)
    mat = MaterialIssueEntry.objects.all().count()
    site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
    mie = 0
    if MaterialIssueEntry.objects.last():
        good = MaterialIssueEntry.objects.last()
        ng = good.mie_count
        mie = int(ng) + 1
    else:
        mie = mie + 1

    ppsupa = []
    seen = set()
    seen_add = seen.add
    tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for r in ent:
        pss = PurchaseEntry.objects.filter(purchase_order_number=r)
        pn = len(pss)
        ppsupa.append([pss, range(1, pn)])

    igoods = []
    seen = set()
    seen_add = seen.add
    tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for s in ent:
        igood = InvoiceItem.objects.filter(purchaseid=s, grn_status='yes', issue_use="no").exclude(Q(damage='all') | Q(retur='all'))
        n = len(igood)
        igoods.append([igood, range(1, n)])

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
        'psupa': psupa, 'ppsupa': ppsupa, 'itemsel': itemsel, 'stock_cat': stock_cat, 
        'igoods': igoods, 'porder': porder, 'item_real': item_real, 'mie': mie, 
        'site_dash': site_dash, 'u_site': u_site, 'mat': mat, 
        'vehicle_dash': vehicle_dash, 'item_dash': item_dash
    }    
    return render(request, 'material_issue.html', context)

@user_access
def material_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = MaterialIssueEntry.objects.all().order_by('-id')
    else:
        s_it = MaterialIssueEntry.objects.filter(user_site=u_site).order_by('-id')
    
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
    return render(request, 'display/material_display.html', context)

@user_access
def material_detail(request, mid):
    if MaterialIssueEntry.objects.filter(id=mid).exists():
        item = MaterialIssueEntry.objects.filter(id=mid).first()
        s_goods = MaterialItem.objects.filter(materialid=mid)
        context = {'item': item, 's_goods': s_goods}    
        return render(request, 'display/material_detail.html', context)
    return redirect('material_display')

@user_access
def search_material(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(issuing_location__icontains=search) | Q(mie_number=search) | 
                Q(vehicle_number__icontains=search) | Q(user_site__icontains=search) | 
                Q(issuing_location=sea) | Q(mie_number=sea) | Q(vehicle_number=sea) | 
                Q(user_site=sea) | Q(issuing_location=se) | Q(mie_number=se) | 
                Q(vehicle_number=se) | Q(user_site=se) | Q(issuing_location=s) | 
                Q(mie_number=s) | Q(vehicle_number=s) | Q(user_site=s)
            )
        else:
            lookup = (
                Q(Q(mie_number=search) | Q(vehicle_number__icontains=search) | 
                  Q(mie_number=sea) | Q(vehicle_number=sea) | Q(mie_number=se) | 
                  Q(vehicle_number=se) | Q(mie_number=s) | Q(vehicle_number=s)) & Q(user_site=u_site)
            )
        s_goods = []
        s_goo = MaterialIssueEntry.objects.filter(lookup).order_by('-id')
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
        return render(request, 'display/material_search.html', context)
    return redirect('material_display')

@user_access
def print_material(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = MaterialIssueEntry.objects.filter(id=jid).first()
        igoods = MaterialItem.objects.filter(materialid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('printmaterial.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportmaterial_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('material_display')

@user_access
def delete_material(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        ge = MaterialIssueEntry.objects.filter(id=sid).first()
        if ge:
            u_site = ge.user_site
            gq = MaterialItem.objects.filter(materialid=sid)
            for a in gq:
                itemid = a.item_id
                qty = a.quantity
                if a.pvn:
                    pvn = a.pvn
                    sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                    if sq:
                        qt = float(sq.quantity or 0)
                        newqty = qt + float(qty or 0)
                        StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
                    InvoiceItem.objects.filter(pvn=pvn).update(issue_use='no')
                else:
                    sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                    if sq:
                        qt = float(sq.quantity or 0)
                        newqty = qt + float(qty or 0)
                        StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

            MaterialIssueEntry.objects.filter(id=sid).delete()
            MaterialItem.objects.filter(materialid=sid).delete()
            messages.info(request, 'done')
        return redirect('material_display')
    return redirect('material_display')

@user_access
def material_edit(request, mid):
    if MaterialIssueEntry.objects.filter(id=mid).exists():
        item = MaterialIssueEntry.objects.filter(id=mid).first()
        porder = PurchaseOrder.objects.all().exclude(po_vehi='yes')
        bills = []
        bill = MaterialItem.objects.filter(materialid=mid)
        bill_len = len(bill)
        goods_count = list(range(1, bill_len + 1))
        bills.append([bill, range(1, bill_len)])
        location_dash = Location.objects.all()
        vehicle_dash = Vehicle.objects.all()
        u_site = user_site(request)
        item_dash = StockEntry.objects.filter(stock_site=u_site)
        item_real = StockItem.objects.all()
        site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)

        ppsupa = []
        seen = set()
        seen_add = seen.add
        tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for r in ent:
            pss = PurchaseEntry.objects.filter(purchase_order_number=r)
            n = len(pss)
            ppsupa.append([pss, range(1, n)])

        igoods = []
        seen = set()
        seen_add = seen.add
        tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for s in ent:
            igood = InvoiceItem.objects.filter(purchaseid=s, grn_status='yes', issue_use="no").exclude(Q(damage='all') | Q(retur='all'))
            n = len(igood)
            igoods.append([igood, range(1, n)])

        mitm = MaterialItem.objects.filter(materialid=mid).exclude(pvn='')

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
            'psupa': psupa, 'ppsupa': ppsupa, 'itemsel': itemsel, 'stock_cat': stock_cat, 
            'porder': porder, 'bills': bills, 'bill': bill, 'igoods': igoods, 
            'mitm': mitm, 'item': item, 'item_real': item_real, 'site_dash': site_dash, 
            'u_site': u_site, 'goods_count': goods_count, 'location_dash': location_dash, 
            'vehicle_dash': vehicle_dash, 'item_dash': item_dash
        }    
        return render(request, 'material_edit.html', context)
    return redirect('material_display')

@user_access
def add_material(request):
    if request.method == "POST":
        date = request.POST.get('date')
        issue_locate = request.POST.get('issue_locate')
        mie_number = request.POST.get('mie')
        mie_count = request.POST.get('mie_count')
        issue_for = request.POST.get('issue_for')
        narrat = request.POST.get('narrat')
        porder = request.POST.get('jobnumber', '').replace(" ", "")
        itemadd = request.POST.getlist('itemadd')
        exitemadd = request.POST.getlist('exitemadd')
        current_user = request.user.username
        u_site = user_site(request)

        for a in itemadd:
            a = str(a)
            if request.POST.get('inameid' + a):
                itemid = request.POST.get('inameid' + a)
                qty = request.POST.get('iqty' + a)
                sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                if not sq or float(sq.quantity or 0) < float(qty or 0):
                    messages.info(request, 'error')
                    return redirect('material_issue')

        if len(exitemadd) > 0:
            for a in itemadd:
                a = str(a)
                if request.POST.get('iid' + a):
                    itemid = request.POST.get('iid' + a)
                    qty = request.POST.get('iqty' + a)
                    sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                    if not sq or float(sq.quantity or 0) < float(qty or 0):
                        messages.info(request, 'error')
                        return redirect('material_issue')

        query = MaterialIssueEntry(
            issue_date=date, mie_number=mie_number, purchase_order_number=porder, 
            mie_count=mie_count, narration=narrat, issuing_location=issue_locate, 
            issue_for=issue_for, entry_by=current_user, user_site=u_site
        )
        query.save()

        mid = query.id
        for a in itemadd:
            a = str(a)
            if request.POST.get('ipvn' + a):
                pvn = request.POST.get('ipvn' + a)
                itemid = request.POST.get('inameid' + a)
                item = request.POST.get('iname' + a)
                alias = request.POST.get('ialias' + a)
                uom = request.POST.get('iuom' + a)
                qty = request.POST.get('iqty' + a)
                que = MaterialItem(materialid=mid, po=porder, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
                que.save()
                InvoiceItem.objects.filter(pvn=pvn).update(issue_use='yes')
                sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                if sq:
                    qt = float(sq.quantity or 0)
                    newqty = qt - float(qty or 0)
                    StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

        if len(exitemadd) > 0:
            for a in itemadd:
                a = str(a)
                if request.POST.get('iid' + a):
                    itemid = request.POST.get('iid' + a)
                    item = request.POST.get('iname' + a)
                    alias = request.POST.get('ialias' + a)
                    uom = request.POST.get('iuom' + a)
                    qty = request.POST.get('iqty' + a)
                    que = MaterialItem(materialid=mid, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
                    que.save()
                    sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                    if sq:
                        qt = float(sq.quantity or 0)
                        newqty = qt - float(qty or 0)
                        StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

        po = PurchaseOrder.objects.filter(purchase_number=porder.upper()).first()
        issuing_site_name = po.issuing_site if po else ''

        q = Notification(
            notify_topic='material_issue', content_id=mid, content='material_add', 
            from_site=u_site, from_user=current_user, content_val=issue_locate, 
            content_val2=issuing_site_name
        )
        q.save()

        messages.info(request, 'done')
        return redirect('material_issue')
    return redirect('material_issue')

@user_access
def edit_material(request):
    if request.method == "POST":
        mid = request.POST.get('mid')
        date = request.POST.get('date')
        issue_locate = request.POST.get('issue_locate')
        mie_number = request.POST.get('mie')
        issue_for = request.POST.get('issue_for')
        porder = request.POST.get('jobnumber', '').replace(" ", "")
        narrat = request.POST.get('narrat')
        exitemadd = request.POST.getlist('exitemadd')
        itemadd = request.POST.getlist('itemadd')

        ge = MaterialIssueEntry.objects.filter(id=mid).first()
        if not ge:
            return redirect('material_display')
        u_site = ge.user_site

        for a in itemadd:
            a = str(a)
            if request.POST.get('inameid' + a):
                itemid = request.POST.get('inameid' + a)
                qty = request.POST.get('iqty' + a)
                sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                if not sq or float(sq.quantity or 0) < float(qty or 0):
                    messages.info(request, 'error')
                    return redirect('/material-issue-edit/' + str(mid) + '/')

        if len(exitemadd) > 0:
            for a in itemadd:
                a = str(a)
                if request.POST.get('iid' + a):
                    itemid = request.POST.get('iid' + a)
                    qty = request.POST.get('iqty' + a)
                    sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                    if not sq or float(sq.quantity or 0) < float(qty or 0):
                        messages.info(request, 'error')
                        return redirect('/material-issue-edit/' + str(mid) + '/')

        MaterialIssueEntry.objects.filter(id=mid).update(
            issue_date=date, issuing_location=issue_locate, 
            purchase_order_number=porder, issue_for=issue_for, narration=narrat
        )

        gq = MaterialItem.objects.filter(materialid=mid)
        for a in gq:
            itemid = a.item_id
            qty = a.quantity
            if a.pvn:
                pvn = a.pvn
                sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                if sq:
                    qt = float(sq.quantity or 0)
                    newqty = qt + float(qty or 0)
                    StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
                InvoiceItem.objects.filter(pvn=pvn).update(issue_use='no')
            else:
                sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                if sq:
                    qt = float(sq.quantity or 0)
                    newqty = qt + float(qty or 0)
                    StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

        MaterialItem.objects.filter(materialid=mid).delete()
        for a in itemadd:
            a = str(a)
            if request.POST.get('ipvn' + a):
                pvn = request.POST.get('ipvn' + a)
                itemid = request.POST.get('inameid' + a)
                item = request.POST.get('iname' + a)
                alias = request.POST.get('ialias' + a)
                uom = request.POST.get('iuom' + a)
                qty = request.POST.get('iqty' + a)
                que = MaterialItem(materialid=mid, po=porder, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
                que.save()
                InvoiceItem.objects.filter(pvn=pvn).update(issue_use='yes')
                sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                if sq:
                    qt = float(sq.quantity or 0)
                    newqty = qt - float(qty or 0)
                    StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

        if len(exitemadd) > 0:
            for a in itemadd:
                a = str(a)
                if request.POST.get('iid' + a):
                    itemid = request.POST.get('iid' + a)
                    item = request.POST.get('iname' + a)
                    alias = request.POST.get('ialias' + a)
                    uom = request.POST.get('iuom' + a)
                    qty = request.POST.get('iqty' + a)
                    que = MaterialItem(materialid=mid, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
                    que.save()
                    sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
                    if sq:
                        qt = float(sq.quantity or 0)
                        newqty = qt - float(qty or 0)
                        StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

        messages.info(request, 'done')
        return redirect('/material-issue-edit/' + str(mid) + '/')
    return redirect('material_display')

# ==================== INTERNAL TRANSFERS ====================
@user_access
def internal_dash(request):
    s_item = InternalTransfer.objects.all().count()
    s_cat = InternalGrn.objects.all().count()
    d_cat = InternalDamageEntry.objects.all().count()
    context = {'s_item': s_item, 's_cat': s_cat, 'd_cat': d_cat}    
    return render(request, 'internal_dash.html', context)

@user_access
def internal_transfer(request):
    location_dash = Location.objects.all()
    vehicle_dash = Vehicle.objects.all()
    u_site = user_site(request)
    item_dash = StockEntry.objects.filter(stock_site=u_site)
    item_real = StockItem.objects.all()
    mat = InternalTransfer.objects.all().count()
    site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
    itn = 0
    if InternalTransfer.objects.last():
        good = InternalTransfer.objects.last()
        ng = good.itn_count
        itn = int(ng) + 1
    else:
        itn = itn + 1

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
        'location_dash': location_dash, 'itemsel': itemsel, 'stock_cat': stock_cat, 
        'psupa': psupa, 'item_real': item_real, 'itn': itn, 'site_dash': site_dash, 
        'u_site': u_site, 'mat': mat, 'vehicle_dash': vehicle_dash, 'item_dash': item_dash
    }    
    return render(request, 'internal_transfer.html', context)

@user_access
def internal_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = InternalTransfer.objects.all().order_by('-id')
    else:
        s_it = InternalTransfer.objects.filter(user_site=u_site).order_by('-id')
    
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
    return render(request, 'display/internal_display.html', context)

@user_access
def internal_detail(request, mid):
    if InternalTransfer.objects.filter(id=mid).exists():
        item = InternalTransfer.objects.filter(id=mid).first()
        s_goods = TransferItem.objects.filter(transferid=mid)
        context = {'item': item, 's_goods': s_goods}    
        return render(request, 'display/internal_detail.html', context)
    return redirect('internal_display')

@user_access
def search_internal(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(issuing_location__icontains=search) | Q(itn_number=search) | 
                Q(receiving_location__icontains=search) | Q(user_site__icontains=search) | 
                Q(issuing_location=sea) | Q(itn_number=sea) | Q(receiving_location=sea) | 
                Q(user_site=sea) | Q(issuing_location=se) | Q(itn_number=se) | 
                Q(receiving_location=se) | Q(user_site=se) | Q(issuing_location=s) | 
                Q(itn_number=s) | Q(receiving_location=s) | Q(user_site=s)
            )
        else:
            lookup = (
                Q(Q(itn_number=search) | Q(receiving_location__icontains=search) | 
                  Q(itn_number=sea) | Q(receiving_location=sea) | Q(itn_number=se) | 
                  Q(receiving_location=se) | Q(itn_number=s) | Q(receiving_location=s)) & Q(user_site=u_site)
            )
        s_goods = []
        s_goo = InternalTransfer.objects.filter(lookup).order_by('-id')
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
        return render(request, 'display/internal_search.html', context)
    return redirect('internal_display')

@user_access
def print_internal(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = InternalTransfer.objects.filter(id=jid).first()
        igoods = TransferItem.objects.filter(transferid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('printinternal.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportinternal_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('internal_display')

@user_access
def delete_internal(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        InternalTransfer.objects.filter(id=sid).delete()
        TransferItem.objects.filter(transferid=sid).delete()
        messages.info(request, 'done')
        return redirect('internal_display')
    return redirect('internal_display')

@user_access
def internal_edit(request, mid):
    if InternalTransfer.objects.filter(id=mid).exists():
        item = InternalTransfer.objects.filter(id=mid).first()
        igoods = TransferItem.objects.filter(transferid=mid)
        goods_count = list(range(1, len(igoods) + 1))

        location_dash = Location.objects.all()
        vehicle_dash = Vehicle.objects.all()
        u_site = user_site(request)
        item_dash = StockEntry.objects.filter(stock_site=u_site)
        item_real = StockItem.objects.all()
        site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)

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
            'item': item, 'itemsel': itemsel, 'stock_cat': stock_cat, 
            'psupa': psupa, 'item_real': item_real, 'site_dash': site_dash, 
            'u_site': u_site, 'igoods': igoods, 'goods_count': goods_count, 
            'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 
            'item_dash': item_dash
        }    
        return render(request, 'internal_edit.html', context)
    return redirect('material_display')

@user_access
def add_internal(request):
    if request.method == "POST":
        current_user = request.user.username
        date = request.POST.get('date')
        issue_locate = request.POST.get('issue_locate')
        receive_locate = request.POST.get('receive_locate')
        itn_number = request.POST.get('itn')
        itn_count = request.POST.get('itn_count')
        narrat = request.POST.get('narrat')
        itemadd = request.POST.getlist('itemadd')
        u_site = user_site(request)

        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            qty = request.POST.get('iqty' + a)
            sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
            if not sq or float(sq.quantity or 0) < float(qty or 0):
                messages.info(request, 'error')
                return redirect('internal_transfer')

        query = InternalTransfer(
            issue_date=date, narration=narrat, itn_number=itn_number, 
            itn_count=itn_count, issuing_location=issue_locate, 
            receiving_location=receive_locate, entry_by=current_user, user_site=u_site
        )
        query.save()

        mid = query.id
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            alias = request.POST.get('ialias' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            que = TransferItem(transferid=mid, pvn=itn_number, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
            que.save()

        q = Notification(
            notify_topic='internal_transfer', content_id=mid, content='transfer_add', 
            from_site=u_site, from_user=current_user, content_val=issue_locate, 
            content_val1=receive_locate, content_val2=receive_locate
        )
        q.save()

        messages.info(request, 'done')
        return redirect('internal_transfer')
    return redirect('internal_transfer')

add_internal_transfer = add_internal

@user_access
def edit_internal(request):
    if request.method == "POST":
        mid = request.POST.get('mid')
        date = request.POST.get('date')
        itn_number = request.POST.get('itn')
        issue_locate = request.POST.get('issue_locate')
        receive_locate = request.POST.get('receive_locate')
        narrat = request.POST.get('narrat')
        itemadd = request.POST.getlist('itemadd')

        ge = InternalTransfer.objects.filter(id=mid).first()
        if not ge:
            return redirect('internal_display')
        u_site = ge.user_site

        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            qty = request.POST.get('iqty' + a)
            sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
            if not sq or float(sq.quantity or 0) < float(qty or 0):
                messages.info(request, 'error')
                return redirect('/internal-transfer-edit/' + str(mid) + '/')

        InternalTransfer.objects.filter(id=mid).update(
            issue_date=date, narration=narrat, issuing_location=issue_locate, 
            receiving_location=receive_locate
        )

        TransferItem.objects.filter(transferid=mid).delete()
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            alias = request.POST.get('ialias' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            que = TransferItem(transferid=mid, pvn=itn_number, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
            que.save()

        messages.info(request, 'done')
        return redirect('/internal-transfer-edit/' + str(mid) + '/')
    return redirect('internal_display')

# ==================== TRANSFER GRN ====================
@user_access
def transfer_goods_entry(request):
    supplier_dash = Supplier.objects.all()
    location_dash = Location.objects.all()
    vehicle_dash = Vehicle.objects.all()
    uom_dash = UOM.objects.all()
    u_site = user_site(request)
    item_dash = StockItem.objects.all()
    grn = 0
    if InternalGrn.objects.last():
        good = InternalGrn.objects.last()
        ng = good.grn_count
        grn = int(ng) + 1
    else:
        grn = grn + 1

    ingg = [i.itn_number for i in InternalTransfer.objects.filter(receiving_location=u_site)]

    igoods = []
    tran = TransferItem.objects.values('transferid')
    trans = {item['transferid'] for item in tran}
    for s in trans:
        igood = TransferItem.objects.filter(transferid=s, pvn__in=ingg, grn_status='no')
        n = len(igood)
        igoods.append([igood, range(1, n)])
    context = {
        'supplier_dash': supplier_dash, 'igoods': igoods, 'location_dash': location_dash, 
        'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 'grn': grn
    }    
    return render(request, 'transfer_grn.html', context)

@user_access
def transfer_goods_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = InternalGrn.objects.all().order_by('-id')
    else:
        s_it = InternalGrn.objects.filter(user_site=u_site).order_by('-id')
    
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
    return render(request, 'display/transfer_grn_display.html', context)

@user_access
def transfer_goods_detail(request, gid):
    if InternalGrn.objects.filter(id=gid).exists():
        item = InternalGrn.objects.filter(id=gid).first()
        s_goods = InternalGrnItems.objects.filter(goodsid=gid)
        context = {'item': item, 's_goods': s_goods}    
        return render(request, 'display/transfer_gen_detail.html', context)
    return redirect('transfer_goods_display')

@user_access
def transfer_search_goods(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = Q(grn_number=search) | Q(user_site__icontains=search) | Q(grn_number=sea) | Q(user_site=sea) | Q(grn_number=se) | Q(user_site=se) | Q(grn_number=s) | Q(user_site=s)
        else:
            lookup = Q(Q(grn_number=search) | Q(grn_number=sea) | Q(grn_number=se) | Q(grn_number=s)) & Q(user_site=u_site)
        s_goods = []
        s_goo = InternalGrn.objects.filter(lookup).order_by('-id')
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
        return render(request, 'display/transfer_grn_search.html', context)
    return redirect('transfer_goods_display')

@user_access
def transfer_print_goods(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = InternalGrn.objects.filter(id=jid).first()
        igoods = InternalGrnItems.objects.filter(goodsid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('print_transfer_grn.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Report_transfer_grn_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('login_user')

@user_access
def transfer_delete_goods(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        it = InternalGrnItems.objects.filter(goodsid=sid)
        for i in it:
            itemid = i.item_id
            qty = i.quantity
            pvn = i.pvn
            itn = InternalTransfer.objects.filter(itn_number=pvn).first()
            if itn:
                source = itn.issuing_location
                dest = itn.receiving_location
                sq_source = StockEntry.objects.filter(item_id=itemid, stock_site=source).first()
                if sq_source:
                    newqty = float(sq_source.quantity or 0) + float(qty or 0)
                    StockEntry.objects.filter(item_id=itemid, stock_site=source).update(quantity=newqty)

                sq_dest = StockEntry.objects.filter(item_id=itemid, stock_site=dest).first()
                if sq_dest:
                    newqty = max(0, float(sq_dest.quantity or 0) - float(qty or 0))
                    StockEntry.objects.filter(item_id=itemid, stock_site=dest).update(quantity=newqty)

                InternalTransfer.objects.filter(itn_number=pvn).update(grn_id='', grn_status='no')
                TransferItem.objects.filter(pvn=pvn).update(grn_id='', grn_status='no')

        InternalGrn.objects.filter(id=sid).delete()
        InternalGrnItems.objects.filter(goodsid=sid).delete()
        messages.info(request, 'done')
        return redirect('transfer_goods_display')
    return redirect('transfer_goods_display')

@user_access
def transfer_goods_edit(request, gid):
    if InternalGrn.objects.filter(id=gid).exists():
        item = InternalGrn.objects.filter(id=gid).first()
        u_site = item.user_site
        seen = set()
        seen_add = seen.add
        tran = InternalGrnItems.objects.values_list('pvn', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        inv_count = []
        for b in ent:
            que = InternalGrnItems.objects.filter(pvn=b, goodsid=gid)
            for i in que:
                inv_count.append(i.pvn)

        supplier_dash = Supplier.objects.all()
        location_dash = Location.objects.all()
        vehicle_dash = Vehicle.objects.all()
        uom_dash = UOM.objects.all()
        item_dash = StockItem.objects.all()

        ingg = [i.itn_number for i in InternalTransfer.objects.filter(receiving_location=u_site)]

        igoods = []
        tran = TransferItem.objects.values('transferid')
        trans = {item['transferid'] for item in tran}
        for s in trans:
            igood = TransferItem.objects.filter(transferid=s, pvn__in=ingg, grn_status='no')
            n = len(igood)
            igoods.append([igood, range(1, n)])

        mitm = InternalGrnItems.objects.filter(goodsid=gid)

        invitem = []
        tran = InternalGrnItems.objects.values('pvn')
        trans = {item['pvn'] for item in tran}
        for s in trans:
            inv = InternalGrnItems.objects.filter(pvn=s, goodsid=gid)
            n = len(inv)
            invitem.append([inv, range(1, n)])
        context = {
            'item': item, 'invitem': invitem, 'igoods': igoods, 'mitm': mitm, 
            'inv_count': inv_count, 'supplier_dash': supplier_dash, 
            'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 
            'uom_dash': uom_dash, 'item_dash': item_dash
        }    
        return render(request, 'edit_transfer_grn.html', context)
    return redirect('transfer_goods_display')

@user_access
def transfer_add_goods(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date = request.POST.get('date')
        grn = request.POST.get('grn')
        grn_count = request.POST.get('grn_count')
        narrat = request.POST.get('narrat')
        itemadd = request.POST.getlist('itemadd')

        for a in itemadd:
            a = str(a)
            pvn = request.POST.get('ipvn' + a)
            itemid = request.POST.get('inameid' + a)
            if not StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
                messages.info(request, 'error')
                return redirect('transfer_goods_entry')
            if InternalGrnItems.objects.filter(pvn=pvn, item_id=itemid).exists():
                messages.info(request, 'error')
                return redirect('transfer_goods_entry')

        if InternalGrn.objects.filter(grn_number=grn).exists():
            messages.info(request, 'error')
            return redirect('transfer_goods_entry')
        else:
            query = InternalGrn(entry_date=date, narration=narrat, grn_number=grn, grn_count=grn_count, entry_by=current_user, user_site=u_site)
            query.save()

        gid = query.id
        sdis = []
        for a in itemadd:
            a = str(a)
            pvn = request.POST.get('ipvn' + a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            alias = request.POST.get('ialias' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            que = InternalGrnItems(goodsid=gid, pvn=pvn, grn=grn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty, orig_quantity=qty)
            que.save()
            itn = InternalTransfer.objects.filter(itn_number=pvn).first()
            if itn:
                source = itn.issuing_location
                dest = itn.receiving_location
                sdis.append([source, dest])

                sq_source = StockEntry.objects.filter(item_id=itemid, stock_site=source).first()
                if sq_source:
                    newqty = max(0, float(sq_source.quantity or 0) - float(qty or 0))
                    StockEntry.objects.filter(item_id=itemid, stock_site=source).update(quantity=newqty)

                sq_dest = StockEntry.objects.filter(item_id=itemid, stock_site=dest).first()
                if sq_dest:
                    newqty = float(sq_dest.quantity or 0) + float(qty or 0)
                    StockEntry.objects.filter(item_id=itemid, stock_site=dest).update(quantity=newqty)

                InternalTransfer.objects.filter(itn_number=pvn).update(grn_id=grn, grn_status='yes')
                TransferItem.objects.filter(pvn=pvn).update(grn_id=grn, grn_status='yes')

        dd = {}
        for s, d in sdis:
            dd[s] = d

        for s, d in dd.items():
            q = Notification(
                notify_topic='internal_transfer', content_id=gid, content='transfer_grn', 
                from_site=u_site, from_user=current_user, content_val=grn, 
                content_val2=s, content_val3=d
            )
            q.save()

        messages.info(request, 'done')
        return redirect('transfer_goods_entry')
    return redirect('transfer_goods_entry')

@user_access
def transfer_edit_goods(request):
    if request.method == "POST":
        gid = request.POST.get('gid')
        date = request.POST.get('date')
        grn = request.POST.get('grn')
        narrat = request.POST.get('narrat')
        itemadd = request.POST.getlist('itemadd')

        ge = InternalGrn.objects.filter(id=gid).first()
        if not ge:
            return redirect('transfer_goods_display')
        u_site = ge.user_site

        it = InternalGrnItems.objects.filter(goodsid=gid)
        itiid = [i.id for i in it]

        for a in itemadd:
            a = str(a)
            pvn = request.POST.get('ipvn' + a)
            itemid = request.POST.get('inameid' + a)
            if not StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
                messages.info(request, 'error')
                return redirect('/transfer-edit-goods/' + str(gid) + '/')
            if InternalGrnItems.objects.filter(pvn=pvn, item_id=itemid).exclude(id__in=itiid).exists():
                messages.info(request, 'error')
                return redirect('/transfer-edit-goods/' + str(gid) + '/')

        InternalGrn.objects.filter(id=gid).update(entry_date=date, narration=narrat)

        for i in it:
            itemid = i.item_id
            qty = i.quantity
            pvn = i.pvn
            itn = InternalTransfer.objects.filter(itn_number=pvn).first()
            if itn:
                source = itn.issuing_location
                dest = itn.receiving_location
                sq_source = StockEntry.objects.filter(item_id=itemid, stock_site=source).first()
                if sq_source:
                    newqty = float(sq_source.quantity or 0) + float(qty or 0)
                    StockEntry.objects.filter(item_id=itemid, stock_site=source).update(quantity=newqty)

                sq_dest = StockEntry.objects.filter(item_id=itemid, stock_site=dest).first()
                if sq_dest:
                    newqty = max(0, float(sq_dest.quantity or 0) - float(qty or 0))
                    StockEntry.objects.filter(item_id=itemid, stock_site=dest).update(quantity=newqty)

                InternalTransfer.objects.filter(itn_number=pvn).update(grn_id='', grn_status='no')
                TransferItem.objects.filter(pvn=pvn).update(grn_id='', grn_status='no')

        InternalGrnItems.objects.filter(goodsid=gid).delete()
        for a in itemadd:
            a = str(a)
            pvn = request.POST.get('ipvn' + a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            alias = request.POST.get('ialias' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            que = InternalGrnItems(goodsid=gid, pvn=pvn, grn=grn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty, orig_quantity=qty)
            que.save()
            itn = InternalTransfer.objects.filter(itn_number=pvn).first()
            if itn:
                source = itn.issuing_location
                dest = itn.receiving_location
                sq_source = StockEntry.objects.filter(item_id=itemid, stock_site=source).first()
                if sq_source:
                    newqty = max(0, float(sq_source.quantity or 0) - float(qty or 0))
                    StockEntry.objects.filter(item_id=itemid, stock_site=source).update(quantity=newqty)

                sq_dest = StockEntry.objects.filter(item_id=itemid, stock_site=dest).first()
                if sq_dest:
                    newqty = float(sq_dest.quantity or 0) + float(qty or 0)
                    StockEntry.objects.filter(item_id=itemid, stock_site=dest).update(quantity=newqty)

                InternalTransfer.objects.filter(itn_number=pvn).update(grn_id=grn, grn_status='yes')
                TransferItem.objects.filter(pvn=pvn).update(grn_id=grn, grn_status='yes')

        messages.info(request, 'done')
        return redirect('/transfer-edit-goods/' + str(gid) + '/')
    return redirect('transfer_goods_display')

# ==================== SALES & BUDGET ====================
@user_passes_test(check_staff, login_url='login_user')
def sale_dash(request):
    s_item = OutSaleEntry.objects.all().count()
    s_cat = StockCategory.objects.all().count()
    context = {'s_item': s_item, 's_cat': s_cat}    
    return render(request, 'saledash.html', context)

@user_access
def out_sales(request):
    location_dash = Location.objects.all()
    vehicle_dash = Vehicle.objects.all()
    u_site = user_site(request)
    item_dash = StockItem.objects.all()
    sid = 0
    if OutSaleEntry.objects.last():
        good = OutSaleEntry.objects.last()
        ng = good.sid_count
        sid = int(ng) + 1
    else:
        sid = sid + 1

    context = {
        'sid': sid, 'u_site': u_site, 'item_dash': item_dash, 
        'location_dash': location_dash, 'vehicle_dash': vehicle_dash
    }    
    return render(request, 'sales.html', context)

@user_access
def sale_display(request):
    s_item = OutSaleEntry.objects.all().order_by('-id')[:30]
    context = {'s_item': s_item}    
    return render(request, 'display/sale_display.html', context)

@user_access
def sale_detail(request, sid):
    if OutSaleEntry.objects.filter(id=sid).exists():
        item = OutSaleEntry.objects.filter(id=sid).first()
        s_goods = SalesItem.objects.filter(saleid=sid)
        context = {'item': item, 's_goods': s_goods}    
        return render(request, 'display/sale_detail.html', context)
    return redirect('sale_display')

@user_access
def search_sales(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        lookup = (
            Q(issuing_location=search) | Q(sales_id=search) | Q(buyer=search) | 
            Q(invoice_type=search) | Q(user_site=search) | Q(issuing_location=sea) | 
            Q(sales_id=sea) | Q(buyer=sea) | Q(invoice_type=sea) | Q(user_site=sea) | 
            Q(issuing_location=se) | Q(sales_id=se) | Q(buyer=se) | Q(invoice_type=se) | 
            Q(user_site=se) | Q(issuing_location=s) | Q(sales_id=s) | Q(buyer=s) | 
            Q(invoice_type=s) | Q(user_site=s)
        )
        s_item = OutSaleEntry.objects.filter(lookup).order_by('-id')
        context = {'s_item': s_item, 'search': search}
        return render(request, 'display/search_sale.html', context)
    return redirect('sale_display')

@user_access
def print_sale(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = OutSaleEntry.objects.filter(id=jid).first()
        igoods = SalesItem.objects.filter(saleid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('printsale.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportsale_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('sale_display')

@user_access
def delete_sale(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        OutSaleEntry.objects.filter(id=sid).delete()
        SalesItem.objects.filter(saleid=sid).delete()
        messages.info(request, 'done')
        return redirect('sale_display')
    return redirect('sale_display')

@user_access
def sale_edit(request, sid):
    if OutSaleEntry.objects.filter(id=sid).exists():
        location_dash = Location.objects.all()
        vehicle_dash = Vehicle.objects.all()
        item_dash = StockItem.objects.all()
        item = OutSaleEntry.objects.filter(id=sid).first()
        invitem = SalesItem.objects.filter(saleid=sid)
        inv_count = list(range(1, len(invitem) + 1))

        context = {
            'item': item, 'inv_count': inv_count, 'invitem': invitem, 
            'item_dash': item_dash, 'location_dash': location_dash, 
            'vehicle_dash': vehicle_dash
        }    
        return render(request, 'sale_edit.html', context)
    return redirect('sale_display')

@user_access
def add_sale(request):
    if request.method == "POST":
        current_user = request.user.username
        date = request.POST.get('date')
        saleid = request.POST.get('saleid')
        sid_count = request.POST.get('sid_count')
        issuing = request.POST.get('issue_locate')
        invoice_type = request.POST.get('invoice_type')
        buyer = request.POST.get('buyer')
        sub_total = request.POST.get('subtotal')
        discount_per = request.POST.get('discount1')
        discount_amt = request.POST.get('discount2')
        vat = request.POST.get('vat')
        total = request.POST.get('total')
        itemadd = request.POST.getlist('itemadd')
        u_site = user_site(request)

        if OutSaleEntry.objects.filter(sales_id=saleid).exists():
            messages.info(request, 'error')
            return redirect('out_sales')
        else:
            query = OutSaleEntry(
                sales_date=date, sales_id=saleid, invoice_type=invoice_type, 
                sid_count=sid_count, issuing_location=issuing, buyer=buyer, 
                sub_total=sub_total, discount_amt=discount_amt, 
                discount_per=discount_per, vat=vat, total=total, 
                entry_by=current_user, user_site=u_site
            )
            query.save()

        pid = query.id
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            rate = request.POST.get('irate' + a)
            amt = request.POST.get('iamt' + a)
            que = SalesItem(saleid=pid, item_id=itemid, item=item, uom=uom, quantity=qty, rate=rate, amount=amt)
            que.save()

        q = Notification(
            notify_topic='out_sales_entry', content_id=pid, content='sales_add', 
            from_site=u_site, from_user=current_user, content_val=issuing, content_val1=buyer
        )
        q.save()

        messages.info(request, 'done')
        return redirect('out_sales')
    return redirect('out_sales')

@user_access
def edit_sale(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        date = request.POST.get('date')
        issuing = request.POST.get('issue_locate')
        invoice_type = request.POST.get('invoice_type')
        buyer = request.POST.get('buyer')
        sub_total = request.POST.get('subtotal')
        discount_per = request.POST.get('discount1')
        discount_amt = request.POST.get('discount2')
        vat = request.POST.get('vat')
        total = request.POST.get('total')
        itemadd = request.POST.getlist('itemadd')

        OutSaleEntry.objects.filter(id=sid).update(
            sales_date=date, invoice_type=invoice_type, issuing_location=issuing, 
            buyer=buyer, sub_total=sub_total, discount_amt=discount_amt, 
            discount_per=discount_per, vat=vat, total=total, entry_by=request.user.username
        )
        
        SalesItem.objects.filter(saleid=sid).delete()
        for a in itemadd:
            a = str(a)
            itemid = request.POST.get('inameid' + a)
            item = request.POST.get('iname' + a)
            uom = request.POST.get('iuom' + a)
            qty = request.POST.get('iqty' + a)
            rate = request.POST.get('irate' + a)
            amt = request.POST.get('iamt' + a)
            que = SalesItem(saleid=sid, item_id=itemid, item=item, uom=uom, quantity=qty, rate=rate, amount=amt)
            que.save()

        messages.info(request, 'done')
        return redirect('/sales-edit/' + str(sid) + '/')
    return redirect('sale_display')