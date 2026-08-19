import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

from eproc.models import (
    Supplier, SupplierCategory, CreditPay, Location, 
    Vehicle, UOM, Site, PurchaseEntry, FuelBill, StockItem, StockEntry,
    StockCategory, StockSubCategory,
    Goods, InvoiceItem, MaterialItem, TransferItem, InternalGrnItems,
    MaintainanceItem, DamageItem, ReturnItem, InternalDamageItem,
    GoodsEntry, MaterialIssueEntry, InternalTransfer, InternalGrn,
    PurchaseOrder, PurchaseItem, MaintainanceBill, Fuel, Reserviour,
    FuelPurchase, VehicleTrack, FuelLeakage, VehicleList,
    DamageEntry, ReturnEntry, InternalDamageEntry, CompanyLetterhead
)
from account.models import UserDetail
from account.views import check_staff
from eproc.decorators import user_access
from procurement.utils import render_to_pdf
from .dashboard_views import user_site


# ==================== SUPER ADMIN LETTERHEAD SETTINGS ====================

@user_passes_test(lambda u: u.is_superuser, login_url='login_user')
def manage_letterhead(request):
    letterheads = CompanyLetterhead.objects.all().order_by('-id')
    active_letterhead = CompanyLetterhead.objects.filter(is_active=True).first()
    sites = Site.objects.filter(active_status='yes')
    context = {
        'letterheads': letterheads,
        'active_letterhead': active_letterhead,
        'sites': sites
    }
    return render(request, 'letterhead_setting.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='login_user')
def upload_letterhead(request):
    if request.method == "POST":
        title = request.POST.get('title', 'Corporate Master Letterhead')
        site_name = request.POST.get('site', 'All Sites')
        header_height = float(request.POST.get('header_height_cm') or 3.5)
        top_margin = float(request.POST.get('top_margin_cm') or 3.8)
        bottom_margin = float(request.POST.get('bottom_margin_cm') or 1.5)
        left_margin = float(request.POST.get('left_margin_cm') or 1.2)
        right_margin = float(request.POST.get('right_margin_cm') or 1.2)
        set_active = request.POST.get('is_active') == 'on'

        letterhead_file = request.FILES.get('letterhead_image')
        footer_file = request.FILES.get('footer_image')

        if not letterhead_file:
            messages.info(request, 'error')
            return redirect('manage_letterhead')

        if set_active:
            if site_name == 'All Sites' or not site_name:
                CompanyLetterhead.objects.all().update(is_active=False)
            else:
                CompanyLetterhead.objects.filter(site=site_name).update(is_active=False)

        new_letterhead = CompanyLetterhead(
            title=title,
            letterhead_image=letterhead_file,
            footer_image=footer_file,
            site=site_name,
            header_height_cm=header_height,
            top_margin_cm=top_margin,
            bottom_margin_cm=bottom_margin,
            left_margin_cm=left_margin,
            right_margin_cm=right_margin,
            is_active=set_active,
            uploaded_by=request.user.username
        )
        new_letterhead.save()

        messages.info(request, 'done')
        return redirect('manage_letterhead')
    return redirect('manage_letterhead')


@user_passes_test(lambda u: u.is_superuser, login_url='login_user')
def toggle_letterhead(request, lid):
    letterhead = get_object_or_404(CompanyLetterhead, id=lid)
    if not letterhead.is_active:
        if letterhead.site == 'All Sites' or not letterhead.site:
            CompanyLetterhead.objects.all().update(is_active=False)
        else:
            CompanyLetterhead.objects.filter(site=letterhead.site).update(is_active=False)
        letterhead.is_active = True
        letterhead.save()
    else:
        letterhead.is_active = False
        letterhead.save()
    messages.info(request, 'done')
    return redirect('manage_letterhead')


@user_passes_test(lambda u: u.is_superuser, login_url='login_user')
def delete_letterhead(request, lid):
    letterhead = get_object_or_404(CompanyLetterhead, id=lid)
    letterhead.delete()
    messages.info(request, 'done')
    return redirect('manage_letterhead')


# ==================== GENERAL INITIAL SETUP ====================

@user_passes_test(check_staff, login_url='login_user')
def predefined(request):
    scount = Supplier.objects.all().count()
    lcount = Location.objects.all().count()
    vcount = UOM.objects.all().count()
    sitecount = Site.objects.all().count()
    context = {'scount': scount, 'sitecount': sitecount, 'lcount': lcount, 'vcount': vcount}    
    return render(request, 'predefine.html', context)

@user_access
def manage_supplier(request):
    category_dash = SupplierCategory.objects.all()
    scount = Supplier.objects.all().count()
    lcount = Location.objects.all().count()
    vcount = UOM.objects.all().count()
    sitecount = Site.objects.all().count()
    context = {'category_dash': category_dash, 'sitecount': sitecount, 'scount': scount, 'lcount': lcount, 'vcount': vcount}    
    return render(request, 'supplier.html', context)

@user_access
def display_supplier(request):
    supplier_dash = Supplier.objects.all().order_by('-id')
    category_dash = SupplierCategory.objects.all()
    context = {'supplier_dash': supplier_dash, 'category_dash': category_dash}    
    return render(request, 'display/supplier_detail.html', context)

@user_access
def add_supplier(request):
    if request.method == "POST":
        current_user = request.user.username
        name = request.POST.get('name')
        address = request.POST.get('address')
        pan = request.POST.get('pan')
        landline = request.POST.get('landline')
        category = request.POST.get('category')
        person1 = request.POST.get('person1')
        person1email = request.POST.get('person1email')
        person1contact = request.POST.get('person1contact')
        person2 = request.POST.get('person2')
        person2email = request.POST.get('person2email')
        person2contact = request.POST.get('person2contact')
        opening = request.POST.get('opening')
        u_site = user_site(request)

        if Supplier.objects.filter(name=name, address=address, pan_number=pan, landline=landline, suppliers_category=category).exists():
            messages.info(request, 'error')
            return redirect('manage_supplier')
        else:
            query = Supplier(
                name=name, address=address, pan_number=pan, landline=landline, 
                opening=opening, suppliers_category=category, person_one=person1, 
                person_one_mobile=person1contact, person_one_email=person1email, 
                person_two=person2, person_two_mobile=person2contact, 
                person_two_email=person2email, user_site=u_site, entry_by=current_user
            )
            query.save()
            messages.info(request, 'done')
            return redirect('manage_supplier')
    return redirect('manage_supplier')

@user_access
def edit_supplier(request):
    if request.method == "POST":
        sid = request.POST.get('suid')
        name = request.POST.get('name')
        address = request.POST.get('address')
        pan = request.POST.get('pan')
        landline = request.POST.get('landline')
        category = request.POST.get('category')
        person1 = request.POST.get('person1')
        person1email = request.POST.get('person1email')
        person1contact = request.POST.get('person1contact')
        person2 = request.POST.get('person2')
        person2email = request.POST.get('person2email')
        person2contact = request.POST.get('person2contact')
        opening = request.POST.get('opening')

        if Supplier.objects.filter(name=name, address=address, pan_number=pan, landline=landline, suppliers_category=category).exclude(id=sid).exists():
            messages.info(request, 'error')
            return redirect('display_supplier')
        else:
            Supplier.objects.filter(id=sid).update(
                name=name, address=address, pan_number=pan, landline=landline, 
                opening=opening, suppliers_category=category, person_one=person1, 
                person_one_mobile=person1contact, person_one_email=person1email, 
                person_two=person2, person_two_mobile=person2contact, 
                person_two_email=person2email
            )
            messages.info(request, 'done')
            return redirect('display_supplier')
    return redirect('display_supplier')

@user_access
def delete_supplier(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        Supplier.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('display_supplier')
    return redirect('display_supplier')

@user_access
def view_credit(request, sid):
    if Supplier.objects.filter(id=sid).exists():
        record = []
        rec = 0
        sup = Supplier.objects.filter(id=sid).first()
        opening = sup.opening or 0
        name = sup.name
        total_credit = float(opening)
        remain = float(opening)

        if PurchaseEntry.objects.filter(supplier_id=sid, transaction_type='credit').exists():
            cre = PurchaseEntry.objects.filter(supplier_id=sid, transaction_type='credit').aggregate(Sum('total'))
            credit = cre['total__sum'] or 0
            total_credit = float(credit) + float(opening)
            remain = total_credit

            if FuelBill.objects.filter(supplier_id=sid, transaction_type='credit').exists():
                f_cre = FuelBill.objects.filter(supplier_id=sid, transaction_type='credit').aggregate(Sum('amount'))
                fuel_credit = f_cre['amount__sum'] or 0
                total_credit += float(fuel_credit)
                remain = total_credit

            if CreditPay.objects.filter(supplier_id=sid).exists():
                recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
                rec = recc['amount__sum'] or 0
                remain = float(total_credit) - float(rec)
                record = CreditPay.objects.filter(supplier_id=sid)

        elif FuelBill.objects.filter(supplier_id=sid, transaction_type='credit').exists():
            cre = FuelBill.objects.filter(supplier_id=sid, transaction_type='credit').aggregate(Sum('amount'))
            credit = cre['amount__sum'] or 0
            total_credit = float(credit) + float(opening)
            remain = total_credit

            if CreditPay.objects.filter(supplier_id=sid).exists():
                recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
                rec = recc['amount__sum'] or 0
                remain = float(total_credit) - float(rec)
                record = CreditPay.objects.filter(supplier_id=sid)
        else:
            if CreditPay.objects.filter(supplier_id=sid).exists():
                recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
                rec = recc['amount__sum'] or 0
                remain = float(total_credit) - float(rec)
                record = CreditPay.objects.filter(supplier_id=sid)

        context = {
            'sid': sid, 'rec': rec, 'name': name, 'record': record, 
            'opening': opening, 'total_credit': total_credit, 'remain': remain
        }    
        return render(request, 'display/credit_pay.html', context)
    return redirect('display_supplier')

@user_access
def pay_credit(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        sid = request.POST.get('supid')
        premain = request.POST.get('remain')
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        trans = request.POST.get('trans')
        bank = request.POST.get('bank') if trans == 'cheque' else ''

        sup = Supplier.objects.filter(id=sid).first()
        sup_name = sup.name
        sup_address = sup.address
        sup_contact = sup.landline

        if float(premain or 0) == 0 or float(amount or 0) > float(premain or 0):
            messages.info(request, 'error')
            return redirect('/credit-detail/' + str(sid) + '/')
        else:
            remain = float(premain) - float(amount)
            query = CreditPay(
                entry_date=date, supplier_id=sid, supplier_name=sup_name, 
                supplier_contact=sup_contact, supplier_address=sup_address, 
                amount=amount, remaining=remain, pay_method=trans, 
                bank=bank, entry_by=current_user, user_site=u_site
            )
            query.save()
            messages.info(request, 'done')
            return redirect('/credit-detail/' + str(sid) + '/')
    return redirect('display_supplier')

@user_access
def print_credit(request):
    if request.method == "POST":
        sid = request.POST.get('jid')
        s_good = Supplier.objects.filter(id=sid).first()
        record = []
        rec = 0
        sup = Supplier.objects.filter(id=sid).first()
        opening = sup.opening or 0
        total_credit = float(opening)
        remain = float(opening)

        if PurchaseEntry.objects.filter(supplier_id=sid, transaction_type='credit').exists():
            cre = PurchaseEntry.objects.filter(supplier_id=sid, transaction_type='credit').aggregate(Sum('total'))
            credit = cre['total__sum'] or 0
            total_credit = float(credit) + float(opening)
            remain = total_credit
            if CreditPay.objects.filter(supplier_id=sid).exists():
                recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
                rec = recc['amount__sum'] or 0
                remain = float(total_credit) - float(rec)
                record = CreditPay.objects.filter(supplier_id=sid)
        else:
            if CreditPay.objects.filter(supplier_id=sid).exists():
                recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
                rec = recc['amount__sum'] or 0
                remain = float(total_credit) - float(rec)
                record = CreditPay.objects.filter(supplier_id=sid)

        context = {
            'a': s_good, 'rec': rec, 'record': record, 
            'opening': opening, 'total_credit': total_credit, 'remain': remain
        }
        pdf = render_to_pdf('printcredit.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportcredit_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('login_user')

@user_access
def manage_location(request):
    location_dash = Location.objects.all().order_by('-id')
    context = {'location_dash': location_dash}    
    return render(request, 'location.html', context)

@user_access
def add_location(request):
    if request.method == "POST":
        current_user = request.user.username
        name = request.POST.get('name')
        url = request.POST.get('url')
        u_site = user_site(request)

        if Location.objects.filter(location_url=url).exists():
            messages.info(request, 'error')
            return redirect('manage_location')
        else:
            query = Location(location_name=name, location_url=url, user_site=u_site, entry_by=current_user)
            query.save()
            messages.info(request, 'done')
            return redirect('manage_location')
    return redirect('manage_location')

@user_access
def edit_location(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        name = request.POST.get('name')
        url = request.POST.get('url')

        if Location.objects.filter(location_url=url).exclude(id=lid).exists():
            messages.info(request, 'error')
            return redirect('manage_location')
        else:
            Location.objects.filter(id=lid).update(location_name=name, location_url=url)
            messages.info(request, 'done')
            return redirect('manage_location')
    return redirect('manage_location')

@user_access
def delete_location(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        Location.objects.filter(id=lid).delete()
        messages.info(request, 'done')
        return redirect('manage_location')
    return redirect('manage_location')

# ==================== LEGACY VEHICLES (SETUP) ====================
@user_access
def manage_vehicle(request):
    vehicle_dash = Vehicle.objects.all().order_by('-id')
    context = {'vehicle_dash': vehicle_dash}    
    return render(request, 'vehicle.html', context)

@user_access
def add_vehicle(request):
    if request.method == "POST":
        name = request.POST.get('name')
        current_user = request.user.username

        if Vehicle.objects.filter(vehicle_number=name, entry_by=current_user).exists():
            messages.info(request, 'error')
            return redirect('manage_vehicle')
        else:
            query = Vehicle(vehicle_number=name, entry_by=current_user)
            query.save()
            messages.info(request, 'done')
            return redirect('manage_vehicle')
    return redirect('manage_vehicle')

@user_access
def edit_vehicle(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        name = request.POST.get('name')

        if Vehicle.objects.filter(vehicle_number=name).exclude(id=lid).exists():
            messages.info(request, 'error')
            return redirect('manage_vehicle')
        else:
            Vehicle.objects.filter(id=lid).update(vehicle_number=name)
            messages.info(request, 'done')
            return redirect('manage_vehicle')
    return redirect('manage_vehicle')

@user_access
def delete_vehicle(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        Vehicle.objects.filter(id=lid).delete()
        messages.info(request, 'done')
        return redirect('manage_vehicle')
    return redirect('manage_vehicle')

# ==================== SUPPLIER CATEGORIES ====================
@user_access
def manage_supplier_category(request):
    category_dash = SupplierCategory.objects.all().order_by('-id')
    context = {'category_dash': category_dash}    
    return render(request, 'supplier_category.html', context)

@user_access
def add_supplier_category(request):
    if request.method == "POST":
        current_user = request.user.username
        name = request.POST.get('name')
        url = request.POST.get('url')
        user_s = user_site(request)

        if SupplierCategory.objects.filter(url=url).exists():
            messages.info(request, 'error')
            return redirect('manage_supplier_category')
        else:
            query = SupplierCategory(name=name, url=url, entry_by=current_user, user_site=user_s)
            query.save()
            messages.info(request, 'done')
            return redirect('manage_supplier_category')
    return redirect('manage_supplier_category')

@user_access
def edit_supplier_category(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        name = request.POST.get('name')
        url = request.POST.get('url')

        if SupplierCategory.objects.filter(url=url).exclude(id=lid).exists():
            messages.info(request, 'error')
            return redirect('manage_supplier_category')
        else:
            SupplierCategory.objects.filter(id=lid).update(name=name, url=url)
            messages.info(request, 'done')
            return redirect('manage_supplier_category')
    return redirect('manage_supplier_category')

@user_access
def delete_supplier_category(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        SupplierCategory.objects.filter(id=lid).delete()
        messages.info(request, 'done')
        return redirect('manage_supplier_category')
    return redirect('manage_supplier_category')

# ==================== UNIT OF MEASURE (UOM) ====================
@user_access
def manage_uom(request):
    uom_dash = UOM.objects.all().order_by('-id')
    context = {'uom_dash': uom_dash}    
    return render(request, 'uom.html', context)

@user_access
def add_uom(request):
    if request.method == "POST":
        name = request.POST.get('name')
        current_user = request.user.username
        u_site = user_site(request)

        if UOM.objects.filter(uom=name).exists():
            messages.info(request, 'error')
            return redirect('manage_uom')
        else:
            query = UOM(uom=name, entry_by=current_user, user_site=u_site)
            query.save()
            messages.info(request, 'done')
            return redirect('manage_uom')
    return redirect('manage_uom')

@user_access
def edit_uom(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        default_name = request.POST.get('default')
        name = request.POST.get('name')

        if UOM.objects.filter(uom=name).exclude(id=lid).exists():
            messages.info(request, 'error')
            return redirect('manage_uom')
        else:
            UOM.objects.filter(id=lid).update(uom=name)
            if name != default_name:
                Goods.objects.filter(uom=default_name).update(uom=name)
                InvoiceItem.objects.filter(uom=default_name).update(uom=name)
                MaterialItem.objects.filter(uom=default_name).update(uom=name)
                TransferItem.objects.filter(uom=default_name).update(uom=name)
                InternalGrnItems.objects.filter(uom=default_name).update(uom=name)
                MaintainanceItem.objects.filter(uom=default_name).update(uom=name)
                DamageItem.objects.filter(uom=default_name).update(uom=name)
                ReturnItem.objects.filter(uom=default_name).update(uom=name)
                InternalDamageItem.objects.filter(uom=default_name).update(uom=name)
            messages.info(request, 'done')
            return redirect('manage_uom')
    return redirect('manage_uom')

@user_access
def delete_uom(request):
    if request.method == "POST":
        lid = request.POST.get('lid')
        UOM.objects.filter(id=lid).delete()
        messages.info(request, 'done')
        return redirect('manage_uom')
    return redirect('manage_uom')

# ==================== SITES ====================
@user_access
def manage_site(request):
    scount = Supplier.objects.all().count()
    lcount = Location.objects.all().count()
    vcount = UOM.objects.all().count()
    sitecount = Site.objects.all().count()
    context = {'scount': scount, 'sitecount': sitecount, 'lcount': lcount, 'vcount': vcount}    
    return render(request, 'site.html', context)

@user_access
def site_display(request):
    site_dash = Site.objects.all().order_by('-id')
    context = {'site_dash': site_dash}    
    return render(request, 'display/site_display.html', context)

@user_access
def add_site(request):
    if request.method == "POST":
        current_user = request.user.username
        name = request.POST.get('name')
        url = request.POST.get('url')
        address = request.POST.get('address')
        pan = request.POST.get('pan')
        contact = request.POST.get('contact')
        role = request.POST.get('admin_sta')
        u_site = user_site(request)

        if Site.objects.filter(url=url).exists():
            messages.info(request, 'error')
            return redirect('manage_site')
        else:
            query = Site(name=name, url=url, address=address, pan_number=pan, contact=contact, role=role, entry_by=current_user, user_site=u_site)
            query.save()
            s_site = query.name
            stoc = StockItem.objects.all()
            for s in stoc:
                itemid = s.id
                alias = s.alias
                s_url = s.url
                cat = s.stock_category
                subcat = s.stock_subcategory
                caturl = s.cat_url
                subcaturl = s.subcat_url
                uom = s.uom
                stock_type = s.stock_type 

                if not StockEntry.objects.filter(url=s_url, stock_site=s_site).exists():
                    s_entry = StockEntry(
                        item=s.item, item_id=itemid, url=s_url, stock_site=s_site, 
                        alias=alias, stock_category=cat, stock_subcategory=subcat, 
                        cat_url=caturl, subcat_url=subcaturl, uom=uom, opening=0, 
                        quantity=0, rate=0, amount=0, stock_type=stock_type, 
                        entry_by=current_user, user_site=s_site
                    )
                    s_entry.save()
            messages.info(request, 'done')
            return redirect('manage_site')
    return redirect('manage_site')

@user_access
def edit_site(request):
    if request.method == "POST":
        sid = request.POST.get('suid')
        name = request.POST.get('name')
        dname = request.POST.get('dname')
        url = request.POST.get('url')
        address = request.POST.get('address')
        pan = request.POST.get('pan')
        contact = request.POST.get('contact')
        role = request.POST.get('admin_sta')

        if Site.objects.filter(url=url).exclude(id=sid).exists():
            messages.info(request, 'error')
            return redirect('site_display')
        else:
            Site.objects.filter(id=sid).update(name=name, url=url, address=address, pan_number=pan, contact=contact, role=role)
            UserDetail.objects.filter(site=dname).update(site=name)
            Supplier.objects.filter(user_site=dname).update(user_site=name)
            CreditPay.objects.filter(user_site=dname).update(user_site=name)
            SupplierCategory.objects.filter(user_site=dname).update(user_site=name)
            StockCategory.objects.filter(user_site=dname).update(user_site=name)
            UOM.objects.filter(user_site=dname).update(user_site=name)
            GoodsEntry.objects.filter(user_site=dname).update(user_site=name)
            PurchaseEntry.objects.filter(user_site=dname).update(user_site=name)
            StockEntry.objects.filter(stock_site=dname).update(stock_site=name)
            StockEntry.objects.filter(user_site=dname).update(user_site=name)
            StockItem.objects.filter(user_site=dname).update(user_site=name)
            MaterialIssueEntry.objects.filter(user_site=dname).update(user_site=name)
            MaterialIssueEntry.objects.filter(issuing_location=dname).update(issuing_location=name)
            MaterialIssueEntry.objects.filter(receiving_location=dname).update(receiving_location=name)
            InternalTransfer.objects.filter(user_site=dname).update(user_site=name)
            InternalTransfer.objects.filter(issuing_location=dname).update(issuing_location=name)
            InternalTransfer.objects.filter(receiving_location=dname).update(receiving_location=name)
            InternalGrn.objects.filter(user_site=dname).update(user_site=name)
            PurchaseOrder.objects.filter(issuing_site=dname).update(issuing_site=name)
            PurchaseOrder.objects.filter(user_site=dname).update(user_site=name)
            PurchaseItem.objects.filter(purchase_location=dname).update(purchase_location=name)
            MaintainanceBill.objects.filter(user_site=dname).update(user_site=name)
            Fuel.objects.filter(user_site=dname).update(user_site=name)
            Reserviour.objects.filter(user_site=dname).update(user_site=name)
            FuelPurchase.objects.filter(issuing_site=dname).update(issuing_site=name)
            FuelPurchase.objects.filter(purchase_location=dname).update(purchase_location=name)
            FuelPurchase.objects.filter(user_site=dname).update(user_site=name)
            FuelBill.objects.filter(issuing_site=dname).update(issuing_site=name)
            FuelBill.objects.filter(purchase_location=dname).update(purchase_location=name)
            FuelBill.objects.filter(user_site=dname).update(user_site=name)
            DamageEntry.objects.filter(user_site=dname).update(user_site=name)
            ReturnEntry.objects.filter(user_site=dname).update(user_site=name)
            InternalDamageEntry.objects.filter(user_site=dname).update(user_site=name)
            VehicleList.objects.filter(current=dname).update(current=name)
            FuelLeakage.objects.filter(user_site=dname).update(user_site=name)
            messages.info(request, 'done')
            return redirect('site_display')
    return redirect('site_display')

@user_access
def delete_site(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        Site.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('site_display')
    return redirect('site_display')

@user_access
def deactivate_site(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        ss = Site.objects.get(id=sid)
        sname = ss.name

        if UserDetail.objects.filter(site=sname).exists():
            uu = UserDetail.objects.filter(site=sname)
            for u in uu:
                uuid = u.id
                uid = u.user_id
                u_obj = User.objects.get(id=uid)
                u_obj.is_staff = False
                u_obj.is_superuser = False
                u_obj.is_active = False
                u_obj.save()
                UserDetail.objects.filter(id=uuid).update(active_status='no')
        Site.objects.filter(id=sid).update(active_status='no')
        messages.info(request, 'done')
        return redirect('site_display')
    return redirect('site_display')