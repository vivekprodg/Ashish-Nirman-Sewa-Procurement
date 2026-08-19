import random
import datetime
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from eproc.models import (
    Reserviour, Fuel, FuelPurchase, FuelBill, FuelInternalTransfer, 
    FuelLeakage, FuelType, VehicleType, VehicleList, Supplier, Site, Notification,
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

# ==================== FUEL TYPES ====================
@user_access
def fuel_type_dash(request):
    v_type = FuelType.objects.all().order_by('-id')
    context = {'v_type': v_type}
    return render(request, 'fuelmaintain/fuel_type.html', context)

@user_access
def add_fuel_type(request):
    if request.method == "POST":
        name = request.POST.get('vehi_type')
        url = request.POST.get('url')
        if FuelType.objects.filter(url=url).exists():
            messages.info(request, 'error')
            return redirect('fuel_type')
        else:
            query = FuelType(name=name, url=url)
            query.save()
            messages.info(request, 'done')
            return redirect('fuel_type')
    return redirect('fuel_type')

@user_access
def fuel_type_display(request):
    v_item = FuelType.objects.all()
    context = {'party': v_item}
    return render(request, 'fuelmaintain/display/fuel_type_display.html', context)

@user_access
def update_fuel_type(request):
    if request.method == "POST":
        fid = request.POST.get('lid')
        name = request.POST.get('name')
        url = request.POST.get('url')

        if FuelType.objects.filter(url=url).exclude(id=fid).exists():
            messages.info(request, 'error')
            return redirect('fuel_type')
        else:
            FuelType.objects.filter(id=fid).update(name=name, url=url)
            messages.info(request, 'done')
            return redirect('fuel_type')
    return redirect('fuel_type')

@user_access
def delete_fuel_type(request):
    if request.method == "POST":
        sid = request.POST.get('lid')
        FuelType.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('fuel_type')
    return redirect('fuel_type')

# ==================== RESERVOIR OPERATIONS ====================
def manage_reserviour(request):
    count1 = Reserviour.objects.all().count()
    count2 = FuelPurchase.objects.all().count()
    count3 = FuelBill.objects.all().count()
    count4 = FuelInternalTransfer.objects.all().count()
    count5 = FuelLeakage.objects.all().count()
    context = {'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4, 'count5': count5}
    return render(request, 'fuelmaintain/reserviour_dash.html', context)

@user_access
def reserviour_add(request):
    site_dash = Site.objects.filter(active_status='yes')
    context = {'site_dash': site_dash}
    return render(request, 'fuelmaintain/reserviour.html', context)

@user_access
def add_reserviour(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        name = request.POST.get('name')
        url = request.POST.get('url')
        site = request.POST.get('site')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        opening = request.POST.get('opening')

        if Reserviour.objects.filter(url=url, site=site).exists():
            messages.info(request, 'error')
            return redirect('manage_reserviour')
        else:
            query = Reserviour(
                name=name, url=url, site=site, location=location, 
                capacity=capacity, opening=opening, stock=opening, 
                entry_by=current_user, user_site=u_site
            )
            query.save()
            messages.info(request, 'done')
            return redirect('manage_reserviour')
    return redirect('manage_reserviour')

@user_access
def reserviour_display(request):
    reserve = Reserviour.objects.all()
    site_dash = Site.objects.filter(active_status='yes')
    context = {'reserve': reserve, 'site_dash': site_dash}
    return render(request, 'fuelmaintain/display/reserviour_display.html', context)

@user_access
def update_reserviour(request):
    if request.method == "POST":
        rid = request.POST.get('suid')
        name = request.POST.get('name')
        url = request.POST.get('url')
        site = request.POST.get('site')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        opening = request.POST.get('opening')
        dopening = request.POST.get('dopening')
        dstock = request.POST.get('dstock')
        dname = request.POST.get('dname')

        opencalc = float(dopening or 0) - float(opening or 0)
        stock_val = float(dstock or 0)
        if opencalc > 0:
            stock_val -= opencalc
        elif opencalc < 0:
            stock_val += abs(opencalc)

        if Reserviour.objects.filter(url=url, site=site).exclude(id=rid).exists():
            messages.info(request, 'error')
            return redirect('reserviour_display')
        else:
            Reserviour.objects.filter(id=rid).update(
                name=name, url=url, site=site, location=location, 
                capacity=capacity, opening=opening, stock=stock_val
            )
            Fuel.objects.filter(reserviour=dname).update(reserviour=name)
            FuelPurchase.objects.filter(reserviour=dname).update(reserviour=name)
            FuelBill.objects.filter(reserviour=dname).update(reserviour=name)
            FuelInternalTransfer.objects.filter(from_reserviour=dname).update(from_reserviour=name)
            FuelInternalTransfer.objects.filter(to_reserviour=dname).update(to_reserviour=name)
            FuelLeakage.objects.filter(reserviour=dname).update(reserviour=name)
            messages.info(request, 'done')
            return redirect('reserviour_display')
    return redirect('manage_reserviour')

@user_access
def delete_reserviour(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        Reserviour.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('reserviour_display')
    return redirect('reserviour_display')

@user_access
def reserviour_report(request):
    reserve = Reserviour.objects.all()
    reserve_name = 'none'
    stocke = 0
    session = 0
    grand = 0
    consumption = 0
    total_fuel = 0
    total_price = 0
    opening = 0
    total_con = 0
    filter_purchase = []
    fuel_consump = []
    purchasee = []
    consump_total = []
    total_transfer = 0
    total_receive = 0
    rrid = []
    rid = 0

    if 'reserviour_id' in request.session:
        rid = request.session['reserviour_id']
        reser = Reserviour.objects.filter(id=rid).first()
        if reser:
            reserve_name = reser.name
            session = 1
            stocke = reser.stock
            opening = reser.opening
            purchasee = FuelBill.objects.filter(reserviour=reserve_name).last()

            if purchasee:
                approve_dt = purchasee.approved_datetime_on
                grand = purchasee.grand_stock
                consumption = float(grand or 0) - float(stocke or 0)
                fuel_consum = Fuel.objects.filter(reserviour_id=rid).order_by('id')
                for f in fuel_consum:
                    if f.entry_datetime_on and approve_dt and f.entry_datetime_on >= approve_dt:
                        rrid.append(f.id)
                fuel_consump = Fuel.objects.filter(id__in=rrid).order_by('date')
                consump_total = Fuel.objects.filter(id__in=rrid).aggregate(Sum('quantity'))
            else:
                grand = reser.opening
                consumption = float(grand or 0) - float(stocke or 0)
                fuel_consump = Fuel.objects.filter(reserviour_id=rid).order_by('date')
                consump_total = Fuel.objects.filter(reserviour_id=rid).aggregate(Sum('quantity'))

            total_fuel = FuelBill.objects.filter(reserviour=reserve_name).aggregate(Sum('quantity'))
            total_price = FuelBill.objects.filter(reserviour=reserve_name).aggregate(Sum('amount'))
            total_con = Fuel.objects.filter(reserviour_id=rid).aggregate(Sum('quantity'))

            if FuelInternalTransfer.objects.filter(from_reserviour=reserve_name).exists():
                total_transfer = FuelInternalTransfer.objects.filter(from_reserviour=reserve_name).aggregate(Sum('quantity'))
            if FuelInternalTransfer.objects.filter(to_reserviour=reserve_name).exists():
                total_receive = FuelInternalTransfer.objects.filter(to_reserviour=reserve_name).aggregate(Sum('quantity'))

    context = {
        'reserviour': reserve, 'session': session, 'rid': rid, 'total_fuel': total_fuel, 
        'total_price': total_price, 'total_con': total_con, 'opening': opening, 
        'purchasee': purchasee, 'reserve_name': reserve_name, 'stocke': stocke, 
        'grand': grand, 'consumption': consumption, 'filter_purchase': filter_purchase, 
        'fuel_consump': fuel_consump, 'consump_total': consump_total, 
        'total_transfer': total_transfer, 'total_receive': total_receive
    }
    return render(request, 'fuelmaintain/reserviour_report.html', context)

@user_access
def reserviour_report_pdf(request):
    if request.method == "POST":
        reserve_name = 'none'
        fuel_consump = []
        consump_total = []
        rrid = []
        pbn = ''
        site_name = None
        try:
            rid = request.POST.get('rid')
            reser = Reserviour.objects.filter(id=rid).first()
            if reser:
                reserve_name = reser.name
                site_name = reser.site
                purchase = FuelBill.objects.filter(reserviour=reserve_name).last()
                if purchase:
                    approve_dt = purchase.approved_datetime_on
                    pbn = purchase.purchase_bill_number
                    fuel_consum = Fuel.objects.filter(reserviour_id=rid).order_by('id')
                    for f in fuel_consum:
                        if f.entry_datetime_on and approve_dt and f.entry_datetime_on >= approve_dt:
                            rrid.append(f.id)
                    fuel_consump = Fuel.objects.filter(id__in=rrid).order_by('date')
                    consump_total = Fuel.objects.filter(id__in=rrid).aggregate(Sum('quantity'))
                else:
                    fuel_consump = Fuel.objects.filter(reserviour_id=rid).order_by('date')
                    consump_total = Fuel.objects.filter(reserviour_id=rid).aggregate(Sum('quantity'))
        except Exception:
            pass

        letterhead = get_active_letterhead(site_name)

        context = {
            'fuel_consump': fuel_consump, 
            'consump_total': consump_total, 
            'reserviour': reserve_name, 
            'pbn': pbn,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('fuelmaintain/print_reserviour.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Report_reserviour_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

@user_access
def reserviour_session(request, rid):
    request.session['reserviour_id'] = rid
    return redirect('reserviour_report')

# ==================== FUEL CONSUMPTION ====================
@user_access
def fuel_manage(request):
    fueldash = list(set(Fuel.objects.values_list('coupon_number', flat=True)))
    v_type = VehicleType.objects.all()
    reserve = Reserviour.objects.all()
    f_type = FuelType.objects.all()
    vehis = []
    seen = set()
    seen_add = seen.add
    ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for e in ent:
        vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
        n = len(vehi)
        vehis.append([vehi, range(1, n)])
    
    newpei = (Fuel.objects.last().fcn + 1) if Fuel.objects.last() else 1

    context = {
        'couponlist': fueldash, 'newpei': newpei, 'vehis': vehis, 
        'f_type': f_type, 'v_type': v_type, 'reserve': reserve
    }
    return render(request, 'fuelmaintain/fuel_manage.html', context)

@user_access
def add_consumption(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date_str = request.POST.get('date')
        coupon = request.POST.get('coupon')
        consump_number = request.POST.get('consump_number')
        fcn = request.POST.get('pvn_count')
        kilometer = request.POST.get('kilometer')
        quantity = request.POST.get('quantity')
        reserve_val = request.POST.get('reserviour_name')
        reserve_id = request.POST.get('reserviour')
        vehicle = request.POST.get('vehicle')
        vehicle_type = request.POST.get('vehicle_type_name')
        vehicle_type_id = request.POST.get('vehicle_type')
        num_type = request.POST.get('num_type')
        fuel_type = request.POST.get('fuel_type')
        
        datetim = datetime.datetime.now().replace(tzinfo=None, second=0, microsecond=0)
        dateon = datetime.date.today()

        upreserve = Reserviour.objects.filter(id=reserve_id).first()
        if upreserve:
            stock = float(upreserve.stock or 0)
            newstock = stock - float(quantity or 0)
            if newstock >= 0:
                query = Fuel(
                    date=date_str, consump_number=consump_number, fcn=fcn, fuel_type=fuel_type, 
                    coupon_number=coupon, number_type=num_type, vehicle_type=vehicle_type, 
                    vehicle_type_id=vehicle_type_id, vehicle_number=vehicle, user_site=u_site, 
                    reserviour=reserve_val, reserviour_id=reserve_id, kilometer=kilometer, 
                    quantity=quantity, entry_datetime_on=datetim, entry_date_on=dateon, 
                    entry_by=current_user
                )
                query.save()
                Reserviour.objects.filter(id=reserve_id).update(stock=newstock)
                messages.info(request, 'done')
                return redirect('fuel_manage')
        messages.info(request, 'error')
        return redirect('fuel_manage')
    return redirect('fuel_manage')

@user_access
def fuel_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_item = Fuel.objects.all().order_by('-id')[:30]
    else:
        s_item = Fuel.objects.filter(user_site=u_site).order_by('-id')
    context = {'s_item': s_item}
    return render(request, 'fuelmaintain/display/fuel_display.html', context)

@user_access
def consumption_detail(request, fid):
    item = Fuel.objects.filter(id=fid).first()
    context = {'item': item}
    return render(request, 'fuelmaintain/display/consumption_detail.html', context)

@user_access
def edit_fuel(request, fid):
    item = Fuel.objects.filter(id=fid).first()
    cp = item.coupon_number if item else ''
    fueldash = [s for s in list(set(Fuel.objects.values_list('coupon_number', flat=True))) if s != cp]
    v_type = VehicleType.objects.all()
    reserve = Reserviour.objects.all()
    f_type = FuelType.objects.all()
    vehis = []
    seen = set()
    seen_add = seen.add
    ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for e in ent:
        vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
        n = len(vehi)
        vehis.append([vehi, range(1, n)])
    context = {'couponlist': fueldash, 'item': item, 'vehis': vehis, 'f_type': f_type, 'v_type': v_type, 'reserve': reserve}
    return render(request, 'fuelmaintain/edit_cunsumption.html', context)

@user_access
def update_fuel(request):
    if request.method == "POST":
        fid = request.POST.get('fid')
        date_str = request.POST.get('date')
        coupon = request.POST.get('coupon')
        kilometer = request.POST.get('kilometer')
        quantity = request.POST.get('quantity')
        default_quantity = request.POST.get('default_quantity')
        reserve_id = request.POST.get('reserviour')
        reserve_val = request.POST.get('reserviour_name')
        default_reserve_id = request.POST.get('default_reserve')
        vehicle_type = request.POST.get('vehicle_type_name')
        vehicle_type_id = request.POST.get('vehicle_type')
        vehicle = request.POST.get('vehicle')
        num_type = request.POST.get('num_type')
        fuel_type = request.POST.get('fuel_type')

        upreserve1 = Reserviour.objects.filter(id=default_reserve_id).first()
        if upreserve1:
            stock1 = float(upreserve1.stock or 0)
            newstock1 = stock1 + float(default_quantity or 0)
            Reserviour.objects.filter(id=default_reserve_id).update(stock=newstock1)

        upreserve2 = Reserviour.objects.filter(id=reserve_id).first()
        if upreserve2:
            stock2 = float(upreserve2.stock or 0)
            newstock2 = stock2 - float(quantity or 0)
            if newstock2 >= 0:
                Reserviour.objects.filter(id=reserve_id).update(stock=newstock2)
                Fuel.objects.filter(id=fid).update(
                    coupon_number=coupon, fuel_type=fuel_type, number_type=num_type, 
                    vehicle_type=vehicle_type, vehicle_type_id=vehicle_type_id, 
                    vehicle_number=vehicle, date=date_str, kilometer=kilometer, 
                    quantity=quantity, reserviour=reserve_val, reserviour_id=reserve_id
                )
                messages.info(request, 'done')
                return redirect('/edit-fuel/' + str(fid) + '/')
        messages.info(request, 'error')
        return redirect('/edit-fuel/' + str(fid) + '/')
    return redirect('fuel_display')

@user_access
def search_fuel_consumption(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(consump_number=search) | Q(coupon_number=search) | Q(vehicle_number__icontains=search) | 
                Q(vehicle_type__icontains=search) | Q(user_site__icontains=search) | 
                Q(reserviour__icontains=search) | Q(fuel_type__icontains=search) | 
                Q(consump_number=sea) | Q(coupon_number=sea) | Q(vehicle_number=sea) | 
                Q(vehicle_type=sea) | Q(user_site=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | 
                Q(consump_number=se) | Q(coupon_number=se) | Q(vehicle_number=se) | 
                Q(vehicle_type=se) | Q(user_site=se) | Q(reserviour=se) | Q(fuel_type=se) | 
                Q(consump_number=s) | Q(coupon_number=s) | Q(vehicle_number=s) | 
                Q(vehicle_type=s) | Q(user_site=s) | Q(reserviour=s) | Q(fuel_type=s)
            )
        else:
            lookup = (
                Q(Q(consump_number=search) | Q(coupon_number=search) | Q(vehicle_number__icontains=search) | 
                  Q(vehicle_type__icontains=search) | Q(reserviour__icontains=search) | 
                  Q(fuel_type__icontains=search) | Q(consump_number=sea) | Q(coupon_number=sea) | 
                  Q(vehicle_number=sea) | Q(vehicle_type=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | 
                  Q(consump_number=se) | Q(coupon_number=se) | Q(vehicle_number=se) | 
                  Q(vehicle_type=se) | Q(reserviour=se) | Q(fuel_type=se) | 
                  Q(consump_number=s) | Q(coupon_number=s) | Q(vehicle_number=s) | 
                  Q(vehicle_type=s) | Q(reserviour=s) | Q(fuel_type=s)) & Q(user_site=u_site)
            )
        s_item = Fuel.objects.filter(lookup).order_by('-id')
        context = {'s_item': s_item, 'search': search}
        return render(request, 'fuelmaintain/display/fuel_consumption_search.html', context)
    return redirect('fuel_display')

@user_access
def delete_fuel_consumption(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        Fuel.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('fuel_display')
    return redirect('fuel_display')

@user_access
def print_fuelconsump(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        job = Fuel.objects.filter(id=jid).first()
        letterhead = get_active_letterhead(job.user_site if job else None)

        context = {
            'a': job,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('fuelmaintain/printfuel_consump.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportfuelconsump_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('fuel_display')

# ==================== FUEL PURCHASE ORDERS & BILLS ====================
@user_access
def fuel_purchase_order(request):
    reserve = Reserviour.objects.all()
    f_type = FuelType.objects.all()
    site_dash = Site.objects.filter(active_status='yes')
    u_site = user_site(request)
    newpon = (FuelPurchase.objects.last().pon + 1) if FuelPurchase.objects.last() else 1

    context = {'newpon': newpon, 'f_type': f_type, 'site_dash': site_dash, 'reserve': reserve, 'u_site': u_site}
    return render(request, 'fuelmaintain/fuel_purchase_order.html', context)

@user_access
def add_fuelpurchase(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        reserve = request.POST.get('reserviour')
        quantity = request.POST.get('quantity') or 0
        rate = request.POST.get('rate') or 0
        amount = request.POST.get('amount') or 0
        date_str = request.POST.get('date')
        purchase_number = request.POST.get('purchase_number')
        pon = request.POST.get('pon')
        location = request.POST.get('location')
        fuel_type = request.POST.get('fuel_type')
        narrat = request.POST.get('narrat')

        if FuelPurchase.objects.filter(purchase_number=purchase_number).exists():
            messages.info(request, 'error')
            return redirect('fuel_purchase_order')
        else:
            query = FuelPurchase(
                location=location, fuel_type=fuel_type, purchase_number=purchase_number, 
                pon=pon, issuing_site=u_site, user_site=u_site, entry_date=date_str, 
                reserviour=reserve, quantity=quantity, rate=rate, amount=amount, 
                narration=narrat, entry_by=current_user
            )
            query.save()
        
        q = Notification(
            notify_topic='fuel_purchase_order', content_id=query.id, 
            content='fuel_purchase_order_add', from_site=u_site, 
            from_user=current_user, content_val=purchase_number
        )
        q.save()

        messages.info(request, 'done')
        return redirect('fuel_purchase_order')
    return redirect('fuel_purchase_order')

@user_access
def fuel_purchase_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = FuelPurchase.objects.all().order_by('-id')
    else:
        s_it = FuelPurchase.objects.filter(issuing_site=u_site).order_by('-id')
    
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
    return render(request, 'fuelmaintain/display/fuel_purchase_display.html', context)

@user_access
def fuel_purchase_detail(request, fid):
    site_dash = Site.objects.filter(active_status='yes')
    item = FuelPurchase.objects.filter(id=fid).first()
    context = {'item': item, 'site_dash': site_dash}
    return render(request, 'fuelmaintain/display/fuel_purchase_detail.html', context)

@user_access
def fuel_purchase_edit(request, fid):
    item = FuelPurchase.objects.filter(id=fid).first()
    reserve = Reserviour.objects.all()
    f_type = FuelType.objects.all()
    context = {'item': item, 'f_type': f_type, 'reserve': reserve}
    return render(request, 'fuelmaintain/edit_fuel_purchase.html', context)

@user_access
def update_fuel_purchase_order(request):
    if request.method == "POST":
        pid = request.POST.get('fid')
        reserve = request.POST.get('reserviour')
        quantity = request.POST.get('quantity') or 0
        rate = request.POST.get('rate') or 0
        amount = request.POST.get('amount') or 0
        date_str = request.POST.get('date')
        location = request.POST.get('location')
        fuel_type = request.POST.get('fuel_type')
        narrat = request.POST.get('narrat')

        FuelPurchase.objects.filter(id=pid).update(
            location=location, fuel_type=fuel_type, entry_date=date_str, 
            reserviour=reserve, quantity=quantity, rate=rate, amount=amount, narration=narrat
        )
        messages.info(request, 'done')
        return redirect('/fuel-purchase-order-edit/' + str(pid) + '/')
    return redirect('fuel_purchase_display')

@user_access
def approve_fuel_purchase(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        fid = request.POST.get('pid')
        locate = request.POST.get('site')
        datetim = datetime.datetime.now().replace(tzinfo=None, second=0, microsecond=0)
        date_today = datetime.date.today()

        FuelPurchase.objects.filter(id=fid).update(
            status='approved', purchase_location=locate, approved_by=current_user, 
            approved_datetime_on=datetim, approved_date_on=date_today
        )
        f = FuelPurchase.objects.filter(id=fid).first()
        ffid = f.purchase_number if f else ''

        q1 = Notification(
            notify_topic='fuel_purchase_order', content_id=fid, content='fuel_purchase_order_approve', 
            from_site=u_site, from_user=current_user, content_val=ffid
        )
        q1.save()

        q2 = Notification(
            notify_topic='fuel_purchase_order', content_id=fid, 
            content='fuel_purchase_order_approve_location', from_site=u_site, 
            from_user=current_user, content_val=ffid, content_val2=locate
        )
        q2.save()

        return redirect('/fuel-purchase-order-detail/' + str(fid) + '/')
    return redirect('fuel_purchase_display')

@user_access
def cancel_fuel_purchase(request):
    if request.method == "POST":
        current_user = request.user.username
        fid = request.POST.get('sid')
        u_site = user_site(request)
        f = FuelPurchase.objects.filter(id=fid).first()
        ffid = f.purchase_number if f else ''
        sitee = f.issuing_site if f else ''

        FuelPurchase.objects.filter(id=fid).update(status='cancelled', cancelled_by=current_user)

        q = Notification(
            notify_topic='fuel_purchase_order', content_id=fid, content='fuel_purchase_order_cancel', 
            from_site=u_site, from_user=current_user, content_val=ffid, content_val2=sitee
        )
        q.save()

        return redirect('/fuel-purchase-order-detail/' + str(fid) + '/')
    return redirect('fuel_purchase_display')

@user_access
def delete_fuel_purchase(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        FuelPurchase.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('fuel_purchase_display')
    return redirect('fuel_purchase_display')

@user_access
def search_fuel_purchase(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(purchase_number=search) | Q(issuing_site=search) | Q(reserviour=search) | 
                Q(fuel_type=search) | Q(location=search) | Q(purchase_number=sea) | 
                Q(issuing_site=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | Q(location=sea) | 
                Q(purchase_number=se) | Q(issuing_site=se) | Q(reserviour=se) | Q(fuel_type=se) | 
                Q(location=se) | Q(purchase_number=s) | Q(issuing_site=s) | Q(reserviour=s) | 
                Q(fuel_type=s) | Q(location=s)
            )
        else:
            lookup = (
                Q(Q(purchase_number=search) | Q(reserviour=search) | Q(fuel_type=search) | 
                  Q(location=search) | Q(purchase_number=sea) | Q(reserviour=sea) | 
                  Q(fuel_type=sea) | Q(location=sea) | Q(purchase_number=se) | 
                  Q(reserviour=se) | Q(fuel_type=se) | Q(location=se) | 
                  Q(purchase_number=s) | Q(reserviour=s) | Q(fuel_type=s) | Q(location=s)) & Q(issuing_site=u_site)
            )
        s_item = []
        s_it = FuelPurchase.objects.filter(lookup).order_by('-id')
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
        return render(request, 'fuelmaintain/display/fuel_purchase_search.html', context)
    return redirect('fuel_purchase_display')

@user_access
def print_fuelpurchase(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        job = FuelPurchase.objects.filter(id=jid).first()
        letterhead = get_active_letterhead(job.issuing_site if job else None)

        context = {
            'a': job,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('fuelmaintain/printfuel_purchase.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportfuelpurchase_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('fuel_purchase_display')

@user_access
def fuel_purchase_bill(request):
    party = FuelPurchase.objects.all()
    supplier_dash = Supplier.objects.all()
    newpon = (FuelBill.objects.last().pbn + 1) if FuelBill.objects.last() else 1
    context = {'newpon': newpon, 'party': party, 'supplier_dash': supplier_dash}
    return render(request, 'fuelmaintain/fuel_purchase_bill.html', context)

@user_access
def add_purchase_bill(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        entry_date = request.POST.get('date')
        purchase_bill_number = request.POST.get('purchase_bill_number')
        pbn = request.POST.get('pbn')
        invoice = request.POST.get('invoice')
        supplier = request.POST.get('supplier')
        day = request.POST.get('day')
        trans = request.POST.get('trans')
        quantity = request.POST.get('quantity')
        rate = request.POST.get('rate')
        amount = request.POST.get('amount')
        vatval = request.POST.get('vatval')
        narrat = request.POST.get('narrat')
        
        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''
        vat = request.POST.get('vat') if vatval == 'yes' else ''

        purchase_number = request.POST.get('purchase_number', '').upper()
        if FuelBill.objects.filter(purchase_order_number=purchase_number).exists():
            messages.info(request, 'error')
            return redirect('fuel_purchase_bill')
        
        jobn = str(purchase_number)
        site = request.POST.get('site' + jobn)
        purchase_order_number = request.POST.get('pn' + jobn)
        reserviour = request.POST.get('reserve' + jobn)
        po_entry_date = request.POST.get('poentry' + jobn)
        po_status = request.POST.get('postatus' + jobn)
        po_approve = request.POST.get('poapprove' + jobn)
        fuel_type = request.POST.get('pofuel' + jobn)
        location = request.POST.get('polocation' + jobn)
        purchase_loc = request.POST.get('popurchase' + jobn)

        reserve = Reserviour.objects.filter(name=reserviour).first()
        stock = float(reserve.stock or 0) if reserve else 0
        grand_stock = stock + float(quantity or 0)
        datetim = datetime.datetime.now().replace(tzinfo=None, second=0, microsecond=0)
        date_today = datetime.date.today()

        query = FuelBill(
            entry_by=current_user, issuing_site=site, purchase_bill_number=purchase_bill_number, 
            pbn=pbn, purchase_order_number=purchase_order_number, invoice_number=invoice, 
            supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, 
            supplier_contact=sup_contact, transaction_type=trans, day=day, 
            reserviour=reserviour, quantity=quantity, rate=rate, vat=vat, amount=amount, 
            po_entry_date=po_entry_date, po_status=po_status, po_approved_by=po_approve, 
            grand_stock=grand_stock, fuel_type=fuel_type, location=location, 
            purchase_location=purchase_loc, approved_datetime_on=datetim, 
            approved_date_on=date_today, entry_date=entry_date, narration=narrat, user_site=u_site
        )
        query.save()

        Reserviour.objects.filter(name=reserviour).update(stock=grand_stock)
        messages.info(request, 'done')
        return redirect('fuel_purchase_bill')
    return redirect('fuel_purchase_bill')

@user_access
def fuel_bill_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    s_item = []
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_it = FuelBill.objects.all().order_by('-id')
    else:
        s_it = FuelBill.objects.filter(issuing_site=u_site).order_by('-id')
    
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
    return render(request, 'fuelmaintain/display/fuel_bill_display.html', context)

@user_access
def fuel_bill_detail(request, fid):
    item = FuelBill.objects.filter(id=fid).first()
    context = {'item': item}
    return render(request, 'fuelmaintain/display/fuel_bill_detail.html', context)

@user_access
def fuel_bill_edit(request, fid):
    item = FuelBill.objects.filter(id=fid).first()
    reserve = FuelPurchase.objects.all()
    supplier_dash = Supplier.objects.all()
    context = {'item': item, 'party': reserve, 'supplier_dash': supplier_dash}
    return render(request, 'fuelmaintain/edit_fuel_bill.html', context)

@user_access
def edit_purchase_bill(request):
    if request.method == "POST":
        fid = request.POST.get('pid')
        entry_date = request.POST.get('date')
        invoice = request.POST.get('invoice')
        quantity = request.POST.get('quantity')
        supplier = request.POST.get('supplier')
        trans = request.POST.get('trans')
        day = request.POST.get('day')
        dqty = request.POST.get('defaultqty')
        rate = request.POST.get('rate')
        amount = request.POST.get('amount')
        vatval = request.POST.get('vatval')
        narrat = request.POST.get('narrat')
        
        sup = Supplier.objects.filter(id=supplier).first()
        sup_name = sup.name if sup else ''
        sup_address = sup.address if sup else ''
        sup_contact = sup.landline if sup else ''
        vat = request.POST.get('vat') if vatval == 'yes' else ''

        purchase_number = request.POST.get('purchase_number', '').upper()
        if FuelBill.objects.filter(purchase_order_number=purchase_number).exclude(id=fid).exists():
            messages.info(request, 'error')
            return redirect('/fuel-purchase-bill-edit/' + str(fid) + '/')
        
        jobn = str(purchase_number)
        site = request.POST.get('site' + jobn)
        purchase_order_number = request.POST.get('pn' + jobn)
        reserviour = request.POST.get('reserve' + jobn)
        po_entry_date = request.POST.get('poentry' + jobn)
        po_status = request.POST.get('postatus' + jobn)
        po_approve = request.POST.get('poapprove' + jobn)
        fuel_type = request.POST.get('pofuel' + jobn)
        location = request.POST.get('polocation' + jobn)
        purchase_loc = request.POST.get('popurchase' + jobn)

        reserve = Reserviour.objects.filter(name=reserviour).first()
        stock = float(reserve.stock or 0) if reserve else 0
        minus = stock - float(dqty or 0)
        grand_stock = minus + float(quantity or 0)

        FuelBill.objects.filter(id=fid).update(
            issuing_site=site, purchase_order_number=purchase_order_number, 
            invoice_number=invoice, supplier_id=supplier, supplier_name=sup_name, 
            supplier_address=sup_address, supplier_contact=sup_contact, 
            transaction_type=trans, day=day, reserviour=reserviour, quantity=quantity, 
            rate=rate, vat=vat, amount=amount, po_entry_date=po_entry_date, 
            po_status=po_status, po_approved_by=po_approve, grand_stock=grand_stock, 
            fuel_type=fuel_type, location=location, purchase_location=purchase_loc, 
            narration=narrat, entry_date=entry_date
        )

        Reserviour.objects.filter(name=reserviour).update(stock=grand_stock)
        messages.info(request, 'done')
        return redirect('/fuel-purchase-bill-edit/' + str(fid) + '/')
    return redirect('fuel_bill_display')

@user_access
def search_fuel_bill(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(purchase_bill_number=search) | Q(purchase_order_number=search) | 
                Q(invoice_number=search) | Q(issuing_site=search) | Q(reserviour=search) | 
                Q(fuel_type=search) | Q(purchase_bill_number=sea) | Q(purchase_order_number=sea) | 
                Q(invoice_number=sea) | Q(issuing_site=sea) | Q(reserviour=sea) | 
                Q(fuel_type=sea) | Q(purchase_bill_number=se) | Q(purchase_order_number=se) | 
                Q(invoice_number=se) | Q(issuing_site=se) | Q(reserviour=se) | 
                Q(fuel_type=se) | Q(purchase_bill_number=s) | Q(purchase_order_number=s) | 
                Q(invoice_number=s) | Q(issuing_site=s) | Q(reserviour=s) | Q(fuel_type=s)
            )
        else:
            lookup = (
                Q(Q(purchase_bill_number=search) | Q(purchase_order_number=search) | 
                  Q(invoice_number=search) | Q(reserviour=search) | Q(fuel_type=search) | 
                  Q(purchase_bill_number=sea) | Q(purchase_order_number=sea) | 
                  Q(invoice_number=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | 
                  Q(purchase_bill_number=se) | Q(purchase_order_number=se) | 
                  Q(invoice_number=se) | Q(reserviour=se) | Q(fuel_type=se) | 
                  Q(purchase_bill_number=s) | Q(purchase_order_number=s) | 
                  Q(invoice_number=s) | Q(reserviour=s) | Q(fuel_type=s)) & Q(issuing_site=u_site)
            )
        s_item = []
        s_it = FuelBill.objects.filter(lookup).order_by('-id')
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
        return render(request, 'fuelmaintain/display/fuel_bill_search.html', context)
    return redirect('fuel_bill_display')

@user_access
def print_fuelbill(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        job = FuelBill.objects.filter(id=jid).first()
        letterhead = get_active_letterhead(job.issuing_site or job.user_site if job else None)

        context = {
            'a': job,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('fuelmaintain/printfuel_bill.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportfuelbill_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('fuel_bill_display')

@user_access
def delete_fuel_bill(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        FuelBill.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('fuel_bill_display')
    return redirect('fuel_bill_display')

# ==================== FUEL TRANSFERS & LEAKAGES ====================
@user_access
def fuel_internal_transfer(request):
    reserve = Reserviour.objects.all()
    f_type = FuelType.objects.all()
    u_site = user_site(request)
    newpon = (FuelInternalTransfer.objects.last().pon + 1) if FuelInternalTransfer.objects.last() else 1

    context = {'newpon': newpon, 'f_type': f_type, 'reserve': reserve, 'u_site': u_site}
    return render(request, 'fuelmaintain/fuel_transfer.html', context)

@user_access
def add_fueltransfer(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        freserve = request.POST.get('freserviour')
        treserve = request.POST.get('treserviour')
        quantity = float(request.POST.get('quantity') or 0)
        date_str = request.POST.get('date')
        fuel_number = request.POST.get('fuel_number')
        pon = request.POST.get('pon')
        fuel_type = request.POST.get('fuel_type')
        narrat = request.POST.get('narrat')

        fre = Reserviour.objects.filter(name=freserve).first()
        if not fre or float(fre.stock or 0) < quantity:
            messages.info(request, 'error')
            return redirect('fuel_internal_transfer')

        query = FuelInternalTransfer(
            fuel_number=fuel_number, pon=pon, fuel_type=fuel_type, user_site=u_site, 
            entry_date=date_str, from_reserviour=freserve, to_reserviour=treserve, 
            quantity=quantity, narration=narrat, entry_by=current_user
        )
        query.save()

        tre = Reserviour.objects.filter(name=treserve).first()
        tqty = float(tre.stock or 0) if tre else 0
        fqty = float(fre.stock or 0)

        Reserviour.objects.filter(name=freserve).update(stock=round(fqty - quantity, 2))
        Reserviour.objects.filter(name=treserve).update(stock=round(tqty + quantity, 2))
        
        q = Notification(
            notify_topic='fuel_transfer', content_id=query.id, content='fuel_transfer_add', 
            from_site=u_site, from_user=current_user, content_val=fuel_number
        )
        q.save()

        messages.info(request, 'done')
        return redirect('fuel_internal_transfer')
    return redirect('fuel_internal_transfer')

@user_access
def fuel_internal_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_item = FuelInternalTransfer.objects.all().order_by('-id')[:30]
    else:
        s_item = FuelInternalTransfer.objects.filter(user_site=u_site).order_by('-id')[:30]
    context = {'s_item': s_item}
    return render(request, 'fuelmaintain/display/fuel_transfer_display.html', context)

@user_access
def fuel_internal_detail(request, fid):
    item = FuelInternalTransfer.objects.filter(id=fid).first()
    context = {'item': item}
    return render(request, 'fuelmaintain/display/fuel_transfer_detail.html', context)

@user_access
def fuel_internal_edit(request, fid):
    item = FuelInternalTransfer.objects.filter(id=fid).first()
    reserve = Reserviour.objects.all()
    f_type = FuelType.objects.all()
    context = {'item': item, 'f_type': f_type, 'reserve': reserve}
    return render(request, 'fuelmaintain/fuel_transfer_edit.html', context)

@user_access
def update_fuel_transfer(request):
    if request.method == "POST":
        pid = request.POST.get('fid')
        freserve = request.POST.get('freserviour')
        treserve = request.POST.get('treserviour')
        quantity = float(request.POST.get('quantity') or 0)
        date_str = request.POST.get('date')
        fuel_number = request.POST.get('fuel_number')
        fuel_type = request.POST.get('fuel_type')
        narrat = request.POST.get('narrat')

        rec = FuelInternalTransfer.objects.filter(id=pid).first()
        if not rec:
            return redirect('fuel_internal_display')

        rqty = float(rec.quantity or 0)
        rtreserve = rec.to_reserviour
        rfreserve = rec.from_reserviour

        rtre = Reserviour.objects.filter(name=rtreserve).first()
        rfre = Reserviour.objects.filter(name=rfreserve).first()

        # Rollback prior transfer
        if rtre and rfre:
            Reserviour.objects.filter(name=rfreserve).update(stock=round(float(rfre.stock or 0) + rqty, 2))
            Reserviour.objects.filter(name=rtreserve).update(stock=round(float(rtre.stock or 0) - rqty, 2))

        # Check new transfer feasibility
        fre = Reserviour.objects.filter(name=freserve).first()
        if not fre or float(fre.stock or 0) < quantity:
            # Revert rollback
            if rtre and rfre:
                Reserviour.objects.filter(name=rfreserve).update(stock=rfre.stock)
                Reserviour.objects.filter(name=rtreserve).update(stock=rtre.stock)
            messages.info(request, 'error')
            return redirect('/fuel-transfer-edit/' + str(pid) + '/')

        FuelInternalTransfer.objects.filter(id=pid).update(
            fuel_type=fuel_type, entry_date=date_str, from_reserviour=freserve, 
            to_reserviour=treserve, quantity=quantity, narration=narrat
        )

        tre = Reserviour.objects.filter(name=treserve).first()
        Reserviour.objects.filter(name=freserve).update(stock=round(float(fre.stock or 0) - quantity, 2))
        if tre:
            Reserviour.objects.filter(name=treserve).update(stock=round(float(tre.stock or 0) + quantity, 2))

        messages.info(request, 'done')
        return redirect('/fuel-transfer-edit/' + str(pid) + '/')
    return redirect('fuel_internal_display')

@user_access
def delete_fuel_transfer(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        FuelInternalTransfer.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('fuel_internal_display')
    return redirect('fuel_internal_display')

@user_access
def search_fuel_transfer(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(fuel_number=search) | Q(from_reserviour__icontains=search) | 
                Q(to_reserviour__icontains=search) | Q(fuel_type__icontains=search) | 
                Q(user_site__icontains=search)
            )
        else:
            lookup = (
                Q(fuel_number=search) | Q(from_reserviour__icontains=search) | 
                Q(to_reserviour__icontains=search) | Q(fuel_type__icontains=search)
            ) & Q(user_site=u_site)
        s_item = FuelInternalTransfer.objects.filter(lookup).order_by('-id')
        context = {'s_item': s_item, 'search': search}
        return render(request, 'fuelmaintain/display/fuel_transfer_search.html', context)
    return redirect('fuel_internal_display')

@user_access
def print_fueltransfer(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        job = FuelInternalTransfer.objects.filter(id=jid).first()
        letterhead = get_active_letterhead(job.user_site if job else None)

        context = {
            'a': job,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('fuelmaintain/printfuel_transfer.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportfueltransfer_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('fuel_internal_display')

@user_access
def fuel_leakage(request):
    reserve = Reserviour.objects.all()
    f_type = FuelType.objects.all()
    newpei = (FuelLeakage.objects.last().fcn + 1) if FuelLeakage.objects.last() else 1
    context = {'newpei': newpei, 'f_type': f_type, 'reserve': reserve}
    return render(request, 'fuelmaintain/lickage.html', context)

@user_access
def add_leakage(request):
    if request.method == "POST":
        current_user = request.user.username
        u_site = user_site(request)
        date_str = request.POST.get('date')
        leakage_number = request.POST.get('consump_number')
        fcn = request.POST.get('pvn_count')
        quantity = float(request.POST.get('quantity') or 0)
        reserve_val = request.POST.get('reserviour_name')
        reserve_id = request.POST.get('reserviour')
        fuel_type = request.POST.get('fuel_type')

        if FuelLeakage.objects.filter(leakage_number=leakage_number).exists():
            messages.info(request, 'error')
            return redirect('fuel_leakage')
        else:
            query = FuelLeakage(
                entry_date=date_str, leakage_number=leakage_number, fcn=fcn, 
                fuel_type=fuel_type, user_site=u_site, reserviour=reserve_val, 
                reserviour_id=reserve_id, quantity=quantity, entry_by=current_user
            )
            query.save()
            
            res = Reserviour.objects.filter(id=reserve_id).first()
            if res:
                new_st = max(0, float(res.stock or 0) - quantity)
                Reserviour.objects.filter(id=reserve_id).update(stock=round(new_st, 2))

            messages.info(request, 'done')
            return redirect('fuel_leakage')
    return redirect('fuel_leakage')

@user_access
def fuel_leakage_display(request):
    u_site = user_site(request)
    u_status = user_role(request)
    if u_status == 'main_admin' or u_status == 'main_staff':
        s_item = FuelLeakage.objects.all().order_by('-id')[:30]
    else:
        s_item = FuelLeakage.objects.filter(user_site=u_site).order_by('-id')[:30]
    context = {'s_item': s_item}
    return render(request, 'fuelmaintain/display/lickage_display.html', context)

@user_access
def leakage_detail(request, fid):
    item = FuelLeakage.objects.filter(id=fid).first()
    context = {'item': item}
    return render(request, 'fuelmaintain/display/lickage_detail.html', context)

@user_access
def edit_leakage(request, fid):
    item = FuelLeakage.objects.filter(id=fid).first()
    reserve = Reserviour.objects.all()
    f_type = FuelType.objects.all()
    context = {'item': item, 'f_type': f_type, 'reserve': reserve}
    return render(request, 'fuelmaintain/lickage_edit.html', context)

@user_access
def update_fuel_leakage(request):
    if request.method == "POST":
        fid = request.POST.get('fid')
        date_str = request.POST.get('date')
        quantity = float(request.POST.get('quantity') or 0)
        default_quantity = float(request.POST.get('default_quantity') or 0)
        reserve_id = request.POST.get('reserviour')
        reserve_val = request.POST.get('reserviour_name')
        default_reserve_id = request.POST.get('default_reserve')
        fuel_type = request.POST.get('fuel_type')

        # Revert old leakage
        res_old = Reserviour.objects.filter(id=default_reserve_id).first()
        if res_old:
            Reserviour.objects.filter(id=default_reserve_id).update(stock=round(float(res_old.stock or 0) + default_quantity, 2))

        # Apply new leakage
        res_new = Reserviour.objects.filter(id=reserve_id).first()
        if res_new:
            Reserviour.objects.filter(id=reserve_id).update(stock=round(max(0, float(res_new.stock or 0) - quantity), 2))

        FuelLeakage.objects.filter(id=fid).update(
            fuel_type=fuel_type, entry_date=date_str, quantity=quantity, 
            reserviour=reserve_val, reserviour_id=reserve_id
        )
        messages.info(request, 'done')
        return redirect('/edit-leakage/' + str(fid) + '/')
    return redirect('leakage_display')

@user_access
def search_fuel_leakage(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        u_site = user_site(request)
        u_status = user_role(request)
        if u_status == 'main_admin' or u_status == 'main_staff':
            lookup = (
                Q(leakage_number=search) | Q(user_site__icontains=search) | 
                Q(reserviour__icontains=search) | Q(fuel_type__icontains=search) | 
                Q(leakage_number=sea) | Q(user_site=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | 
                Q(leakage_number=se) | Q(user_site=se) | Q(reserviour=se) | Q(fuel_type=se) | 
                Q(leakage_number=s) | Q(user_site=s) | Q(reserviour=s) | Q(fuel_type=s)
            )
        else:
            lookup = (
                Q(leakage_number=search) | Q(reserviour__icontains=search) | 
                Q(fuel_type__icontains=search) | Q(leakage_number=sea) | 
                Q(reserviour=sea) | Q(fuel_type=sea) | Q(leakage_number=se) | 
                Q(reserviour=se) | Q(fuel_type=se) | Q(leakage_number=s) | 
                Q(reserviour=s) | Q(fuel_type=s)
            ) & Q(user_site=u_site)
        s_item = FuelLeakage.objects.filter(lookup).order_by('-id')
        context = {'s_item': s_item, 'search': search}
        return render(request, 'fuelmaintain/display/lickage_seach.html', context)
    return redirect('leakage_display')

@user_access
def delete_fuel_leakage(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        FuelLeakage.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('leakage_display')
    return redirect('leakage_display')

@user_access
def print_fuelleakage(request):
    if request.method == "POST":
        jid = request.POST.get('jid')
        job = FuelLeakage.objects.filter(id=jid).first()
        letterhead = get_active_letterhead(job.user_site if job else None)

        context = {
            'a': job,
            'letterhead': letterhead
        }
        pdf = render_to_pdf('fuelmaintain/printlickage.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            rnum = random.randint(11111111, 99999999)
            filename = "Reportfuelleakage_%s.pdf" % (rnum)
            content = "inline; filename='%s'" % (filename)
            if request.GET.get("download"):
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('leakage_display')