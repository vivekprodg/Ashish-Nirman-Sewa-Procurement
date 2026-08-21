import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from eproc.models import (
    DamageEntry, DamageItem, DamageInvoice, ReturnEntry, 
    ReturnItem, ReturnInvoice, InternalDamageEntry, InternalDamageItem, 
    PurchaseOrder, PurchaseItem, PurchaseEntry, InvoiceItem, 
    InternalGrn, InternalGrnItems, StockItem, UOM, Notification,
    CompanyLetterhead
)
from eproc.decorators import user_access
from procurement.utils import render_to_pdf
from .dashboard_views import user_site, user_role

def get_active_letterhead(site_name=None):
    """
    Fetches the site-specific active letterhead or falls back to the corporate master letterhead.
    """
    if site_name:
        lh = CompanyLetterhead.objects.filter(site=site_name, is_active=True).first()
        if lh:
            return lh
    # Fallback to All Sites master letterhead or any active letterhead
    master_lh = CompanyLetterhead.objects.filter(Q(site='All Sites') | Q(site='') | Q(site__isnull=True), is_active=True).first()
    if master_lh:
        return master_lh
    return CompanyLetterhead.objects.filter(is_active=True).first()

# ==================== DAMAGE STOCK (PURCHASE INVOICE) ====================
@user_access
def damage_stock(request):
    porder = PurchaseOrder.objects.filter(status='approved')
    uom_dash = UOM.objects.all()
    item_real = StockItem.objects.all()
    pvn = 0
    if DamageEntry.objects.last():
        good = DamageEntry.objects.last()
        pvn = int(good.pvn_count or 0) + 1
    else:
        pvn = 1

    pitem = InvoiceItem.objects.filter(issue_use="no", grn_status='no').exclude(Q(damage='all') | Q(retur='all'))
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
    tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for s in ent:
        igood = InvoiceItem.objects.filter(purchaseid=s, issue_use="no", grn_status='no')
        n = len(igood)
        igoods.append([igood, range(1, n)])

    purinvoice = PurchaseEntry.objects.filter(issue_use='no', grn_status='no')

    context = {
        'porder': porder, 'pitem': pitem, 'pvn': pvn, 'item_real': item_real, 
        'uom_dash': uom_dash, 'psupa': psupa, 'purinvoice': purinvoice, 'igoods': igoods
    }    
    return render(request, 'damage_product.html', context)

@user_access
def damage_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_item = DamageEntry.objects.all().order_by('-id')[:30]
    else:
        s_item = DamageEntry.objects.filter(user_site=u_site).order_by('-id')[:30]
    context = {'s_item': s_item}    
    return render(request, 'display/damage_display.html', context)

@user_access
def damage_detail(request, pid):
    if DamageEntry.objects.filter(id=pid).exists():
        item = DamageEntry.objects.filter(id=pid).first()
        s_goods = DamageItem.objects.filter(damageid=pid)
        dinvoice = DamageInvoice.objects.filter(damageid=pid)
        context = {'item': item, 's_goods': s_goods, 'dinvoice': dinvoice}    
        return render(request, 'display/damage_detail.html', context)
    return redirect('damage_display')

@user_access
def search_damage(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(purchase_order_number=search) | Q(damage_number=search) | Q(user_site=search) | 
                Q(purchase_order_number=sea) | Q(damage_number=sea) | Q(user_site=sea) | 
                Q(purchase_order_number=se) | Q(damage_number=se) | Q(user_site=se) | 
                Q(purchase_order_number=s) | Q(damage_number=s) | Q(user_site=s)
            )
        else:
            lookup = (
                Q(Q(purchase_order_number=search) | Q(damage_number=search) | 
                  Q(purchase_order_number=sea) | Q(damage_number=sea) | 
                  Q(purchase_order_number=se) | Q(damage_number=se) | 
                  Q(purchase_order_number=s) | Q(damage_number=s)) & Q(user_site=u_site)
            )
        s_item = DamageEntry.objects.filter(lookup).order_by('-id')
        context = {'s_item': s_item, 'search': search}
        return render(request, 'display/damage_search.html', context)
    return redirect('damage_display')

@user_access
def print_damage(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = DamageEntry.objects.filter(id=jid).first()
        igoods = DamageItem.objects.filter(damageid=jid)
        minvoice = DamageInvoice.objects.filter(damageid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods, 
            'minvoice': minvoice,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('printdamage.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportdamage_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('damage_display')

@user_access
def delete_damage(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        ge = DamageItem.objects.filter(damageid=sid)
        for a in ge:
            itemid = a.item_id
            qty = a.quantity
            pvn = a.pvn
            if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                quantity = itm.quantity
                dqty = float(quantity or 0) + float(qty or 0)
                InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='no', damage_qty='0')
                PurchaseEntry.objects.filter(voucher_number=pvn).update(damage='no')

        DamageEntry.objects.filter(id=sid).delete()
        DamageItem.objects.filter(damageid=sid).delete()
        DamageInvoice.objects.filter(damageid=sid).delete()
        messages.info(request, 'done')
        return redirect('damage_display')
    return redirect('damage_display')

@user_access
def damage_edit(request, pid):
    if DamageEntry.objects.filter(id=pid).exists():
        porder = PurchaseOrder.objects.filter(status='approved')
        uom_dash = UOM.objects.all()
        item_real = StockItem.objects.all()
        item = DamageEntry.objects.filter(id=pid).first()
        bills = []
        pp = DamageItem.objects.filter(damageid=pid)
        bill_count = list(range(1, len(pp) + 1))

        seen = set()
        seen_add = seen.add
        tran = DamageItem.objects.values_list('pvn', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for r in ent:
            bill = DamageItem.objects.filter(pvn=r, damageid=pid)
            n = len(bill)
            bills.append([bill, range(1, n)])

        pitem = InvoiceItem.objects.filter(issue_use="no", grn_status='no').exclude(Q(damage='all') | Q(retur='all'))
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
            igood = InvoiceItem.objects.filter(purchaseid=s, issue_use="no", grn_status='no')
            n = len(igood)
            igoods.append([igood, range(1, n)])

        purinvoice = PurchaseEntry.objects.filter(issue_use='no', grn_status='no')
        minv = DamageInvoice.objects.filter(damageid=pid)
        mitm = DamageItem.objects.filter(damageid=pid)

        context = {
            'item': item, 'pp': pp, 'porder': porder, 'pitem': pitem, 
            'bill_count': bill_count, 'bills': bills, 'item_real': item_real, 
            'uom_dash': uom_dash, 'psupa': psupa, 'purinvoice': purinvoice, 
            'minv': minv, 'mitm': mitm
        }    
        return render(request, 'damage_edit.html', context)
    return redirect('damage_display')

@user_access
def add_damage(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date = request.POST.get('date')
        damage_number = request.POST.get('damage_number')
        pvn_count = request.POST.get('pvn_count')
        narrat = request.POST.get('narrat')
        porder = request.POST.get('jobnumber', '').replace(" ", "").upper()
        itemadd = request.POST.getlist('itemadd')
        pvnlist = request.POST.getlist('pvnval')
        if len(pvnlist) == 0:
            messages.info(request, 'error')
            return redirect('damage_product')

        pvnl = list(set([p.upper() for p in pvnlist]))

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    if DamageItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                        messages.info(request, 'error')
                        return redirect('damage_product')
                    quantity = request.POST.get('iqty' + rstr)
                    if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                        itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                        if float(quantity or 0) > float(itm.quantity or 0):
                            messages.info(request, 'error')
                            return redirect('damage_product')

        if DamageEntry.objects.filter(damage_number=damage_number).exists():
            messages.info(request, 'error')
            return redirect('damage_product')
        else:
            query = DamageEntry(
                entry_date=date, purchase_order_number=porder, narration=narrat, 
                damage_number=damage_number, pvn_count=pvn_count, 
                entry_by=current_user, user_site=u_site
            )
            query.save()

        pid = query.id
        for p in pvnl:
            pe = PurchaseEntry.objects.filter(voucher_number=p).first()
            if pe:
                DamageInvoice.objects.create(
                    damageid=pid, damage_number=damage_number, purchase_order_number=porder, 
                    voucher_number=p, invoice_number=pe.invoice_number, 
                    invoice_type=pe.invoice_type, supplier=pe.supplier_name, 
                    sub_total=pe.sub_total, discount_amt=pe.discount_amt, 
                    discount_per=pe.discount_per, vat=pe.vat, total=pe.total
                )

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    item = request.POST.get('iname' + rstr)
                    alias = request.POST.get('ialias' + rstr)
                    uom = request.POST.get('iuom' + rstr)
                    qty = request.POST.get('iqty' + rstr)
                    if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                        itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                        DamageItem.objects.create(
                            damageid=pid, po=porder, dn=damage_number, pvn=pvn, 
                            item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty
                        )
                        dqty = float(itm.quantity or 0) - float(qty or 0)
                        damage_tag = 'all' if int(dqty) == 0 else 'partial'
                        InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(
                            quantity=dqty, useable_quantity=dqty, damage=damage_tag, damage_qty=qty
                        )
                        PurchaseEntry.objects.filter(voucher_number=pvn).update(damage='yes')

        po = PurchaseOrder.objects.filter(purchase_number=porder).first()
        issuing_site_name = po.issuing_site if po else ''

        q = Notification(
            notify_topic='damage_entry', content_id=pid, content='damage_add', 
            from_site=u_site, from_user=current_user, content_val=damage_number, 
            content_val2=issuing_site_name
        )
        q.save()

        messages.info(request, 'done')
        return redirect('damage_product')
    return redirect('damage_product')

@user_access
def edit_damage(request):
    if request.method == "POST":
        pid = request.POST.get('pid')
        date = request.POST.get('date')
        damage_number = request.POST.get('damage_number')
        narrat = request.POST.get('narrat')
        porder = request.POST.get('jobnumber', '').replace(" ", "").upper()
        itemadd = request.POST.getlist('itemadd')
        pvnlist = request.POST.getlist('pvnval')
        if len(pvnlist) == 0:
            messages.info(request, 'error')
            return redirect('/damage-edit/' + str(pid) + '/')

        pvnl = list(set([p.upper() for p in pvnlist]))

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    if DamageItem.objects.filter(item_id=itemid, pvn=pvn).exclude(damageid=pid).exists():
                        messages.info(request, 'error')
                        return redirect('/damage-edit/' + str(pid) + '/')

        # Rollback prior state
        ge = DamageItem.objects.filter(damageid=pid)
        for a in ge:
            itemid = a.item_id
            qty = a.quantity
            pvn = a.pvn
            if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                dqty = float(itm.quantity or 0) + float(qty or 0)
                InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='no', damage_qty='0')
                PurchaseEntry.objects.filter(voucher_number=pvn).update(damage='no')

        DamageEntry.objects.filter(id=pid).update(entry_date=date, purchase_order_number=porder, narration=narrat)
        DamageInvoice.objects.filter(damageid=pid).delete()
        DamageItem.objects.filter(damageid=pid).delete()

        for p in pvnl:
            pe = PurchaseEntry.objects.filter(voucher_number=p).first()
            if pe:
                DamageInvoice.objects.create(
                    damageid=pid, damage_number=damage_number, purchase_order_number=porder, 
                    voucher_number=p, invoice_number=pe.invoice_number, 
                    invoice_type=pe.invoice_type, supplier=pe.supplier_name, 
                    sub_total=pe.sub_total, discount_amt=pe.discount_amt, 
                    discount_per=pe.discount_per, vat=pe.vat, total=pe.total
                )

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    item = request.POST.get('iname' + rstr)
                    alias = request.POST.get('ialias' + rstr)
                    uom = request.POST.get('iuom' + rstr)
                    qty = request.POST.get('iqty' + rstr)
                    if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                        itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                        DamageItem.objects.create(
                            damageid=pid, po=porder, dn=damage_number, pvn=pvn, 
                            item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty
                        )
                        dqty = float(itm.quantity or 0) - float(qty or 0)
                        damage_tag = 'all' if int(dqty) == 0 else 'partial'
                        InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(
                            quantity=dqty, useable_quantity=dqty, damage=damage_tag, damage_qty=qty
                        )
                        PurchaseEntry.objects.filter(voucher_number=pvn).update(damage='yes')

        messages.info(request, 'done')
        return redirect('/damage-edit/' + str(pid) + '/')
    return redirect('damage_display')

# ==================== RETURN STOCK (TO VENDORS) ====================
@user_access
def return_stock(request):
    porder = PurchaseOrder.objects.filter(status='approved')
    uom_dash = UOM.objects.all()
    item_real = StockItem.objects.all()
    pvn = 0
    if ReturnEntry.objects.last():
        good = ReturnEntry.objects.last()
        pvn = int(good.pvn_count or 0) + 1
    else:
        pvn = 1

    pitem = InvoiceItem.objects.filter(issue_use="no", grn_status='no').exclude(Q(damage='all') | Q(retur='all'))
    psupa = []
    seen = set()
    seen_add = seen.add
    tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for r in ent:
        ps = PurchaseEntry.objects.filter(purchase_order_number=r)
        n = len(ps)
        psupa.append([ps, range(1, n)])

    purinvoice = PurchaseEntry.objects.filter(issue_use='no', grn_status='no')

    context = {
        'porder': porder, 'pitem': pitem, 'pvn': pvn, 'item_real': item_real, 
        'uom_dash': uom_dash, 'psupa': psupa, 'purinvoice': purinvoice
    }    
    return render(request, 'return.html', context)

@user_access
def return_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_item = ReturnEntry.objects.all().order_by('-id')[:30]
    else:
        s_item = ReturnEntry.objects.filter(user_site=u_site).order_by('-id')[:30]
    context = {'s_item': s_item}    
    return render(request, 'display/return_display.html', context)

@user_access
def return_detail(request, pid):
    if ReturnEntry.objects.filter(id=pid).exists():
        item = ReturnEntry.objects.filter(id=pid).first()
        s_goods = ReturnItem.objects.filter(damageid=pid)
        dinvoice = ReturnInvoice.objects.filter(damageid=pid)
        context = {'item': item, 's_goods': s_goods, 'dinvoice': dinvoice}    
        return render(request, 'display/return_detail.html', context)
    return redirect('return_display')

@user_access
def search_return(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(purchase_order_number=search) | Q(damage_number=search) | Q(user_site=search) | 
                Q(purchase_order_number=sea) | Q(damage_number=sea) | Q(user_site=sea) | 
                Q(purchase_order_number=se) | Q(damage_number=se) | Q(user_site=se) | 
                Q(purchase_order_number=s) | Q(damage_number=s) | Q(user_site=s)
            )
        else:
            lookup = (
                Q(Q(purchase_order_number=search) | Q(damage_number=search) | 
                  Q(purchase_order_number=sea) | Q(damage_number=sea) | 
                  Q(purchase_order_number=se) | Q(damage_number=se) | 
                  Q(purchase_order_number=s) | Q(damage_number=s)) & Q(user_site=u_site)
            )
        s_item = ReturnEntry.objects.filter(lookup).order_by('-id')
        context = {'s_item': s_item, 'search': search}
        return render(request, 'display/return_search.html', context)
    return redirect('return_display')

@user_access
def print_return(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = ReturnEntry.objects.filter(id=jid).first()
        igoods = ReturnItem.objects.filter(damageid=jid)
        minvoice = ReturnInvoice.objects.filter(damageid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods, 
            'minvoice': minvoice,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('printreturn.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportreturn_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('return_display')

@user_access
def delete_return(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        ge = ReturnItem.objects.filter(damageid=sid)
        for a in ge:
            itemid = a.item_id
            qty = a.quantity
            amt = a.amount
            dism = a.discount_amt
            pvn = a.pvn
            if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                amount = float(itm.amount or 0) + float(amt or 0)
                dqty = float(itm.quantity or 0) + float(qty or 0)
                dim = float(itm.discount_amt or 0) + float(dism or 0)
                InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(
                    quantity=dqty, discount_amt=round(dim, 2), amount=round(amount, 2), 
                    useable_quantity=dqty, retur='no', retur_qty='0'
                )
                pv = PurchaseEntry.objects.filter(voucher_number=pvn).first()
                if pv:
                    subt = float(pv.sub_total or 0) + float(amt or 0)
                    dip = float(pv.discount_per or 0)
                    va = float(pv.vat or 0) if pv.vat else 0
                    p_dim = subt * (dip / 100) if dip > 0 else 0
                    tot = subt - p_dim + va
                    PurchaseEntry.objects.filter(voucher_number=pvn).update(
                        sub_total=round(subt, 2), total=round(tot, 2), 
                        discount_amt=round(p_dim, 2), retur='no'
                    )

        ReturnEntry.objects.filter(id=sid).delete()
        ReturnInvoice.objects.filter(damageid=sid).delete()
        ReturnItem.objects.filter(damageid=sid).delete()
        messages.info(request, 'done')
        return redirect('return_display')
    return redirect('return_display')

@user_access
def return_edit(request, pid):
    if ReturnEntry.objects.filter(id=pid).exists():
        porder = PurchaseOrder.objects.filter(status='approved')
        uom_dash = UOM.objects.all()
        item_real = StockItem.objects.all()
        item = ReturnEntry.objects.filter(id=pid).first()
        bills = []
        pp = ReturnItem.objects.filter(damageid=pid)
        bill_count = list(range(1, len(pp) + 1))

        seen = set()
        seen_add = seen.add
        tran = ReturnItem.objects.values_list('pvn', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for r in ent:
            bill = ReturnItem.objects.filter(pvn=r, damageid=pid)
            n = len(bill)
            bills.append([bill, range(1, n)])

        pitem = InvoiceItem.objects.filter(issue_use="no", grn_status='no').exclude(Q(damage='all') | Q(retur='all'))
        psupa = []
        seen = set()
        seen_add = seen.add
        tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for r in ent:
            ps = PurchaseEntry.objects.filter(purchase_order_number=r)
            n = len(ps)
            psupa.append([ps, range(1, n)])

        purinvoice = PurchaseEntry.objects.filter(issue_use='no', grn_status='no')
        minv = ReturnInvoice.objects.filter(damageid=pid)
        mitm = ReturnItem.objects.filter(damageid=pid)

        context = {
            'item': item, 'pp': pp, 'porder': porder, 'pitem': pitem, 
            'bill_count': bill_count, 'bills': bills, 'item_real': item_real, 
            'uom_dash': uom_dash, 'psupa': psupa, 'purinvoice': purinvoice, 
            'minv': minv, 'mitm': mitm
        }    
        return render(request, 'return_edit.html', context)
    return redirect('return_display')

@user_access
def add_return(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date = request.POST.get('date')
        damage_number = request.POST.get('damage_number')
        pvn_count = request.POST.get('pvn_count')
        narrat = request.POST.get('narrat')
        porder = request.POST.get('jobnumber', '').replace(" ", "").upper()
        itemadd = request.POST.getlist('itemadd')
        pvnlist = request.POST.getlist('pvnval')
        if len(pvnlist) == 0:
            messages.info(request, 'error')
            return redirect('return_product')

        pvnl = list(set([p.upper() for p in pvnlist]))

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    if ReturnItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                        messages.info(request, 'error')
                        return redirect('return_product')
                    quantity = request.POST.get('iqty' + rstr)
                    if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                        itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                        if float(quantity or 0) > float(itm.quantity or 0):
                            messages.info(request, 'error')
                            return redirect('return_product')

        if ReturnEntry.objects.filter(damage_number=damage_number).exists():
            messages.info(request, 'error')
            return redirect('return_product')
        else:
            query = ReturnEntry(
                entry_date=date, purchase_order_number=porder, narration=narrat, 
                damage_number=damage_number, pvn_count=pvn_count, 
                entry_by=current_user, user_site=u_site
            )
            query.save()

        pid = query.id
        for p in pvnl:
            pe = PurchaseEntry.objects.filter(voucher_number=p).first()
            if pe:
                ReturnInvoice.objects.create(
                    damageid=pid, damage_number=damage_number, purchase_order_number=porder, 
                    voucher_number=p, invoice_number=pe.invoice_number, 
                    invoice_type=pe.invoice_type, supplier=pe.supplier_name, 
                    sub_total=pe.sub_total, discount_amt=pe.discount_amt, 
                    discount_per=pe.discount_per, vat=pe.vat, total=pe.total
                )

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    item = request.POST.get('iname' + rstr)
                    alias = request.POST.get('ialias' + rstr)
                    uom = request.POST.get('iuom' + rstr)
                    qty = request.POST.get('iqty' + rstr)
                    if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                        itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                        rate = float(itm.rate or 0)
                        disp = float(itm.discount_per or 0)
                        amt = float(qty or 0) * rate
                        dm = amt * (disp / 100) if disp > 0 else 0
                        amt_net = amt - dm

                        ReturnItem.objects.create(
                            damageid=pid, po=porder, dn=damage_number, pvn=pvn, 
                            item_id=itemid, item=item, alias=alias, uom=uom, 
                            quantity=qty, rate=rate, amount=round(amt_net, 2), 
                            discount_per=disp, discount_amt=round(dm, 2)
                        )
                        dqty = float(itm.quantity or 0) - float(qty or 0)
                        if int(dqty) == 0:
                            InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(
                                quantity=0, amount=0, discount_per=0, discount_amt=0, 
                                useable_quantity=0, retur='all', retur_qty=qty
                            )
                        else:
                            amtt = dqty * rate
                            dm_rem = amtt * (disp / 100) if disp > 0 else 0
                            InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(
                                quantity=dqty, amount=round(amtt - dm_rem, 2), 
                                discount_amt=round(dm_rem, 2), useable_quantity=dqty, 
                                retur='partial', retur_qty=qty
                            )

                        pv = PurchaseEntry.objects.filter(voucher_number=pvn).first()
                        if pv:
                            subt = float(pv.sub_total or 0) - amt_net
                            dip = float(pv.discount_per or 0)
                            va = float(pv.vat or 0) if pv.vat else 0
                            p_dim = subt * (dip / 100) if dip > 0 else 0
                            tot = subt - p_dim + va
                            PurchaseEntry.objects.filter(voucher_number=pvn).update(
                                sub_total=round(subt, 2), total=round(tot, 2), 
                                discount_amt=round(p_dim, 2), retur='yes'
                            )

        po = PurchaseOrder.objects.filter(purchase_number=porder).first()
        issuing_site_name = po.issuing_site if po else ''

        q = Notification(
            notify_topic='return_entry', content_id=pid, content='return_add', 
            from_site=u_site, from_user=current_user, content_val=damage_number, 
            content_val2=issuing_site_name
        )
        q.save()

        messages.info(request, 'done')
        return redirect('return_product')
    return redirect('return_product')

@user_access
def edit_return(request):
    if request.method == "POST":
        pid = request.POST.get('pid')
        date = request.POST.get('date')
        damage_number = request.POST.get('damage_number')
        narrat = request.POST.get('narrat')
        porder = request.POST.get('jobnumber', '').replace(" ", "").upper()
        itemadd = request.POST.getlist('itemadd')
        pvnlist = request.POST.getlist('pvnval')
        if len(pvnlist) == 0:
            messages.info(request, 'error')
            return redirect('/return-edit/' + str(pid) + '/')

        pvnl = list(set([p.upper() for p in pvnlist]))

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    if ReturnItem.objects.filter(item_id=itemid, pvn=pvn).exclude(damageid=pid).exists():
                        messages.info(request, 'error')
                        return redirect('/return-edit/' + str(pid) + '/')

        # Rollback prior return state
        ge = ReturnItem.objects.filter(damageid=pid)
        for a in ge:
            itemid = a.item_id
            qty = a.quantity
            amt = a.amount
            dism = a.discount_amt
            pvn = a.pvn
            if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                amount = float(itm.amount or 0) + float(amt or 0)
                dqty = float(itm.quantity or 0) + float(qty or 0)
                dim = float(itm.discount_amt or 0) + float(dism or 0)
                InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(
                    quantity=dqty, discount_amt=round(dim, 2), amount=round(amount, 2), 
                    useable_quantity=dqty, retur='no', retur_qty='0'
                )
                pv = PurchaseEntry.objects.filter(voucher_number=pvn).first()
                if pv:
                    subt = float(pv.sub_total or 0) + float(amt or 0)
                    dip = float(pv.discount_per or 0)
                    va = float(pv.vat or 0) if pv.vat else 0
                    p_dim = subt * (dip / 100) if dip > 0 else 0
                    tot = subt - p_dim + va
                    PurchaseEntry.objects.filter(voucher_number=pvn).update(
                        sub_total=round(subt, 2), total=round(tot, 2), 
                        discount_amt=round(p_dim, 2), retur='no'
                    )

        ReturnEntry.objects.filter(id=pid).update(entry_date=date, purchase_order_number=porder, narration=narrat)
        ReturnInvoice.objects.filter(damageid=pid).delete()
        ReturnItem.objects.filter(damageid=pid).delete()

        for p in pvnl:
            pe = PurchaseEntry.objects.filter(voucher_number=p).first()
            if pe:
                ReturnInvoice.objects.create(
                    damageid=pid, damage_number=damage_number, purchase_order_number=porder, 
                    voucher_number=p, invoice_number=pe.invoice_number, 
                    invoice_type=pe.invoice_type, supplier=pe.supplier_name, 
                    sub_total=pe.sub_total, discount_amt=pe.discount_amt, 
                    discount_per=pe.discount_per, vat=pe.vat, total=pe.total
                )

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    item = request.POST.get('iname' + rstr)
                    alias = request.POST.get('ialias' + rstr)
                    uom = request.POST.get('iuom' + rstr)
                    qty = request.POST.get('iqty' + rstr)
                    if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                        itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
                        rate = float(itm.rate or 0)
                        disp = float(itm.discount_per or 0)
                        amt = float(qty or 0) * rate
                        dm = amt * (disp / 100) if disp > 0 else 0
                        amt_net = amt - dm

                        ReturnItem.objects.create(
                            damageid=pid, po=porder, dn=damage_number, pvn=pvn, 
                            item_id=itemid, item=item, alias=alias, uom=uom, 
                            quantity=qty, rate=rate, amount=round(amt_net, 2), 
                            discount_per=disp, discount_amt=round(dm, 2)
                        )
                        dqty = float(itm.quantity or 0) - float(qty or 0)
                        if int(dqty) == 0:
                            InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(
                                quantity=0, amount=0, discount_per=0, discount_amt=0, 
                                useable_quantity=0, retur='all', retur_qty=qty
                            )
                        else:
                            amtt = dqty * rate
                            dm_rem = amtt * (disp / 100) if disp > 0 else 0
                            InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(
                                quantity=dqty, amount=round(amtt - dm_rem, 2), 
                                discount_amt=round(dm_rem, 2), useable_quantity=dqty, 
                                retur='partial', retur_qty=qty
                            )

                        pv = PurchaseEntry.objects.filter(voucher_number=pvn).first()
                        if pv:
                            subt = float(pv.sub_total or 0) - amt_net
                            dip = float(pv.discount_per or 0)
                            va = float(pv.vat or 0) if pv.vat else 0
                            p_dim = subt * (dip / 100) if dip > 0 else 0
                            tot = subt - p_dim + va
                            PurchaseEntry.objects.filter(voucher_number=pvn).update(
                                sub_total=round(subt, 2), total=round(tot, 2), 
                                discount_amt=round(p_dim, 2), retur='yes'
                            )

        messages.info(request, 'done')
        return redirect('/return-edit/' + str(pid) + '/')
    return redirect('return_display')

# ==================== TRANSFER DAMAGE ENTRIES ====================
@user_access
def internal_damage_stock(request):
    porder = InternalGrn.objects.filter(invoice_status='no')
    uom_dash = UOM.objects.all()
    item_real = StockItem.objects.all()
    pvn = 0
    if InternalDamageEntry.objects.last():
        good = InternalDamageEntry.objects.last()
        pvn = int(good.pvn_count or 0) + 1
    else:
        pvn = 1

    pitem = InternalGrnItems.objects.filter(invoice_status="no").exclude(damage='all')
    igoods = []
    seen = set()
    seen_add = seen.add
    tran = InternalGrnItems.objects.values_list('goodsid', flat=True).distinct()
    ent = [x for x in tran if not (x in seen or seen_add(x))]
    for s in ent:
        igood = InternalGrnItems.objects.filter(goodsid=s, invoice_status='no').exclude(damage='all')
        n = len(igood)
        igoods.append([igood, range(1, n)])

    context = {
        'porder': porder, 'pitem': pitem, 'pvn': pvn, 
        'item_real': item_real, 'uom_dash': uom_dash, 'igoods': igoods
    }    
    return render(request, 'internal_damage.html', context)

@user_access
def internal_damage_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_item = InternalDamageEntry.objects.all().order_by('-id')[:30]
    else:
        s_item = InternalDamageEntry.objects.filter(user_site=u_site).order_by('-id')[:30]
    context = {'s_item': s_item}    
    return render(request, 'display/internal_damage_display.html', context)

@user_access
def internal_damage_detail(request, pid):
    if InternalDamageEntry.objects.filter(id=pid).exists():
        item = InternalDamageEntry.objects.filter(id=pid).first()
        s_goods = InternalDamageItem.objects.filter(damageid=pid)
        context = {'item': item, 's_goods': s_goods}    
        return render(request, 'display/internal_damage_detail.html', context)
    return redirect('internal_damage_display')

@user_access
def search_internal_damage(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(damage_number=search) | Q(user_site__icontains=search) | 
                Q(damage_number=sea) | Q(user_site=sea) | Q(damage_number=se) | 
                Q(user_site=se) | Q(damage_number=s) | Q(user_site=s)
            )
        else:
            lookup = (
                Q(Q(narration__icontains=search) | Q(damage_number=search) | 
                  Q(narration__icontains=sea) | Q(damage_number=sea) | 
                  Q(damage_number=se) | Q(damage_number=s)) & Q(user_site=u_site)
            )
        s_item = InternalDamageEntry.objects.filter(lookup).order_by('-id')
        context = {'s_item': s_item, 'search': search}
        return render(request, 'display/internal_damage_search.html', context)
    return redirect('internal_damage_display')

@user_access
def print_internal_damage(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        s_good = InternalDamageEntry.objects.filter(id=jid).first()
        igoods = InternalDamageItem.objects.filter(damageid=jid)
        letterhead = get_active_letterhead(s_good.user_site if s_good else None)

        context = {
            'a': s_good, 
            'igoods': igoods,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('printinternaldamage.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reporttransferdamage_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('internal_damage_display')

@user_access
def delete_internal_damage(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        ge = InternalDamageItem.objects.filter(damageid=sid)
        for a in ge:
            itemid = a.item_id
            qty = a.quantity
            pvn = a.pvn
            if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
                itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
                dqty = float(itm.quantity or 0) + float(qty or 0)
                InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='no', damage_qty='0')
                InternalGrn.objects.filter(grn_number=pvn).update(damage='no')

        InternalDamageEntry.objects.filter(id=sid).delete()
        InternalDamageItem.objects.filter(damageid=sid).delete()
        messages.info(request, 'done')
        return redirect('internal_damage_display')
    return redirect('internal_damage_display')

@user_access
def internal_damage_edit(request, pid):
    if InternalDamageEntry.objects.filter(id=pid).exists():
        porder = InternalGrn.objects.filter(invoice_status='no')
        uom_dash = UOM.objects.all()
        item_real = StockItem.objects.all()
        item = InternalDamageEntry.objects.filter(id=pid).first()
        bills = []
        pp = InternalDamageItem.objects.filter(damageid=pid)
        bill_count = list(range(1, len(pp) + 1))

        seen = set()
        seen_add = seen.add
        tran = InternalDamageItem.objects.values_list('pvn', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for r in ent:
            bill = InternalDamageItem.objects.filter(pvn=r, damageid=pid)
            n = len(bill)
            bills.append([bill, range(1, n)])

        pitem = InternalGrnItems.objects.filter(invoice_status='no').exclude(damage='all')
        igoods = []
        seen = set()
        seen_add = seen.add
        tran = InternalGrnItems.objects.values_list('goodsid', flat=True).distinct()
        ent = [x for x in tran if not (x in seen or seen_add(x))]
        for s in ent:
            igood = InternalGrnItems.objects.filter(goodsid=s, invoice_status='no').exclude(damage='all')
            n = len(igood)
            igoods.append([igood, range(1, n)])

        mitm = InternalDamageItem.objects.filter(damageid=pid)

        context = {
            'item': item, 'pp': pp, 'porder': porder, 'pitem': pitem, 
            'bill_count': bill_count, 'bills': bills, 'item_real': item_real, 
            'uom_dash': uom_dash, 'mitm': mitm
        }    
        return render(request, 'internal_damage_edit.html', context)
    return redirect('internal_damage_display')

@user_access
def add_internal_damage(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date = request.POST.get('date')
        damage_number = request.POST.get('damage_number')
        pvn_count = request.POST.get('pvn_count')
        narrat = request.POST.get('narrat')
        itemadd = request.POST.getlist('itemadd')
        pvnlist = request.POST.getlist('pvnval')
        if len(pvnlist) == 0:
            messages.info(request, 'error')
            return redirect('internal_damage_stock')

        pvnl = list(set([p.upper() for p in pvnlist]))

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    if InternalDamageItem.objects.filter(item_id=itemid, pvn=pvn).exists():
                        messages.info(request, 'error')
                        return redirect('internal_damage_stock')
                    quantity = request.POST.get('iqty' + rstr)
                    if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
                        itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
                        if float(quantity or 0) > float(itm.quantity or 0):
                            messages.info(request, 'error')
                            return redirect('internal_damage_stock')

        if InternalDamageEntry.objects.filter(damage_number=damage_number).exists():
            messages.info(request, 'error')
            return redirect('internal_damage_stock')
        else:
            query = InternalDamageEntry(
                entry_date=date, narration=narrat, damage_number=damage_number, 
                pvn_count=pvn_count, entry_by=current_user, user_site=u_site
            )
            query.save()

        pid = query.id
        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    item = request.POST.get('iname' + rstr)
                    alias = request.POST.get('ialias' + rstr)
                    uom = request.POST.get('iuom' + rstr)
                    qty = request.POST.get('iqty' + rstr)
                    if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
                        itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
                        InternalDamageItem.objects.create(
                            damageid=pid, dn=damage_number, pvn=pvn, 
                            item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty
                        )
                        dqty = float(itm.quantity or 0) - float(qty or 0)
                        damage_tag = 'all' if int(dqty) == 0 else 'partial'
                        InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(
                            quantity=dqty, damage=damage_tag, damage_qty=qty
                        )
                        InternalGrn.objects.filter(grn_number=pvn).update(damage='yes')

        q = Notification(
            notify_topic='internal_damage_entry', content_id=pid, 
            content='internal_damage_add', from_site=u_site, 
            from_user=current_user, content_val=damage_number
        )
        q.save()

        messages.info(request, 'done')
        return redirect('internal_damage_stock')
    return redirect('internal_damage_stock')

@user_access
def edit_internal_damage(request):
    if request.method == "POST":
        pid = request.POST.get('pid')
        date = request.POST.get('date')
        damage_number = request.POST.get('damage_number')
        narrat = request.POST.get('narrat')
        itemadd = request.POST.getlist('itemadd')
        pvnlist = request.POST.getlist('pvnval')
        if len(pvnlist) == 0:
            messages.info(request, 'error')
            return redirect('/internal-damage-edit/' + str(pid) + '/')

        pvnl = list(set([p.upper() for p in pvnlist]))

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    if InternalDamageItem.objects.filter(item_id=itemid, pvn=pvn).exclude(damageid=pid).exists():
                        messages.info(request, 'error')
                        return redirect('/internal-damage-edit/' + str(pid) + '/')

        # Rollback state
        ge = InternalDamageItem.objects.filter(damageid=pid)
        for a in ge:
            itemid = a.item_id
            qty = a.quantity
            pvn = a.pvn
            if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
                itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
                dqty = float(itm.quantity or 0) + float(qty or 0)
                InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='no', damage_qty='0')
                InternalGrn.objects.filter(grn_number=pvn).update(damage='no')

        InternalDamageEntry.objects.filter(id=pid).update(entry_date=date, narration=narrat)
        InternalDamageItem.objects.filter(damageid=pid).delete()

        for a in itemadd:
            a = str(a)
            for pvn in pvnl:
                rstr = str(pvn) + a
                if request.POST.get('inameid' + rstr):
                    itemid = request.POST.get('inameid' + rstr)
                    item = request.POST.get('iname' + rstr)
                    alias = request.POST.get('ialias' + rstr)
                    uom = request.POST.get('iuom' + rstr)
                    qty = request.POST.get('iqty' + rstr)
                    if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
                        itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
                        InternalDamageItem.objects.create(
                            damageid=pid, dn=damage_number, pvn=pvn, 
                            item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty
                        )
                        dqty = float(itm.quantity or 0) - float(qty or 0)
                        damage_tag = 'all' if int(dqty) == 0 else 'partial'
                        InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(
                            quantity=dqty, damage=damage_tag, damage_qty=qty
                        )
                        InternalGrn.objects.filter(grn_number=pvn).update(damage='yes')

        messages.info(request, 'done')
        return redirect('/internal-damage-edit/' + str(pid) + '/')
    return redirect('internal_damage_display')