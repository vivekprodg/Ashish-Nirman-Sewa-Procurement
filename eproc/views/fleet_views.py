import datetime
from datetime import datetime as dt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from eproc.models import (
    VehicleType, VehicleList, VehicleTrack, Site, 
    PurchaseOrder, MaintainanceBill, Fuel, Notification
)
from eproc.decorators import user_access
from .dashboard_views import user_site


# ==================== VEHICLE TYPES ====================

@user_access
def vehicle_type(request):
    v_type = VehicleType.objects.all().order_by('-id')
    context = {'v_type': v_type}
    return render(request, 'fuelmaintain/vehicle_type.html', context)


@user_access
def add_vehicle_type(request):
    if request.method == "POST":
        name = request.POST.get('vehi_type')
        url = request.POST.get('url')
        if VehicleType.objects.filter(url=url).exists():
            messages.info(request, 'error')
            return redirect('vehicle_type')
        else:
            query = VehicleType(type_name=name, url=url)
            query.save()
            messages.info(request, 'done')
            return redirect('vehicle_type')
    return redirect('vehicle_type')


@user_access
def vehicle_type_display(request):
    v_item = VehicleType.objects.all()
    context = {'party': v_item}
    return render(request, 'fuelmaintain/display/vehicle_type_display.html', context)


@user_access
def update_vehicle_type(request):
    if request.method == "POST":
        fid = request.POST.get('lid')
        name = request.POST.get('name')
        url = request.POST.get('url')

        if VehicleType.objects.filter(url=url).exclude(id=fid).exists():
            messages.info(request, 'error')
            return redirect('vehicle_type')
        else:
            VehicleType.objects.filter(id=fid).update(type_name=name, url=url)
            messages.info(request, 'done')
            return redirect('vehicle_type')
    return redirect('vehicle_type')


@user_access
def delete_vehicle_type(request):
    if request.method == "POST":
        sid = request.POST.get('lid')
        VehicleType.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('vehicle_type')
    return redirect('vehicle_type')


# ==================== VEHICLE DIRECTORY ====================

@user_access
def vehicle_dash(request):
    v_type = VehicleType.objects.all()
    context = {'v_type': v_type}
    return render(request, 'fuelmaintain/vehicles.html', context)


@user_access
def vehicle_display(request):
    s_item = VehicleList.objects.all().order_by('-id')
    v_type = VehicleType.objects.all().order_by('-id')
    context = {'s_item': s_item, 'v_type': v_type}
    return render(request, 'fuelmaintain/display/vehicle_display.html', context)


@user_access
def vehicle_add(request):
    if request.method == "POST":
        vehicle_number = request.POST.get('vehicle_number')
        url = request.POST.get('vehi_url')
        chasis_url = request.POST.get('chasis_url')
        engine_url = request.POST.get('engine_url')
        chasis = request.POST.get('chasis_number')
        engine = request.POST.get('engine_number')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_type_name = request.POST.get('vehicle_type_name')
        owner = request.POST.get('owner_name')
        driver = request.POST.get('driver_name')
        helper = request.POST.get('helper_name')
        capacity = request.POST.get('capacity')
        contact1 = request.POST.get('contact1')
        contact2 = request.POST.get('contact2')

        if (VehicleList.objects.filter(url=url).exists() or 
            VehicleList.objects.filter(chasis_number=chasis).exists() or 
            VehicleList.objects.filter(engine_number=engine).exists()):
            messages.info(request, 'error')
            return redirect('vehicle')
        else:
            query = VehicleList(
                vehicle_number=vehicle_number, url=url, chasis_url=chasis_url, 
                engine_url=engine_url, chasis_number=chasis, engine_number=engine, 
                vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name, 
                owner_name=owner, driver_name=driver, helper_name=helper, 
                capacity=capacity, contact1=contact1, contact2=contact2
            )
            query.save()
            messages.info(request, 'done')
            return redirect('vehicle')
    return redirect('vehicle')


@user_access
def vehicle_update(request):
    if request.method == "POST":
        vid = request.POST.get('suid')
        default_vehi = request.POST.get('defaultvehi')
        default_chasis = request.POST.get('defaultchasis')
        default_engine = request.POST.get('defaultengine')
        owner_name = request.POST.get('owner_name')
        vehicle_number = request.POST.get('vehicle_number')
        url = request.POST.get('vehi_url')
        chasis_url = request.POST.get('chasis_url')
        engine_url = request.POST.get('engine_url')
        chasis = request.POST.get('chasis_number')
        engine = request.POST.get('engine_number')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_type_name = request.POST.get('vehicle_type_name')
        driver = request.POST.get('driver_name')
        helper = request.POST.get('helper_name')
        capacity = request.POST.get('capacity')
        contact1 = request.POST.get('contact1')
        contact2 = request.POST.get('contact2')

        if (VehicleList.objects.filter(url=url).exclude(id=vid).exists() or 
            VehicleList.objects.filter(chasis_number=chasis).exclude(id=vid).exists() or 
            VehicleList.objects.filter(engine_number=engine).exclude(id=vid).exists()):
            messages.info(request, 'error')
            return redirect('vehicle_display')
        else:
            VehicleList.objects.filter(id=vid).update(
                vehicle_number=vehicle_number, url=url, chasis_url=chasis_url, 
                engine_url=engine_url, chasis_number=chasis, engine_number=engine, 
                vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name, 
                owner_name=owner_name, driver_name=driver, helper_name=helper, 
                capacity=capacity, contact1=contact1, contact2=contact2
            )
            # Cascade updates
            for target_model in [PurchaseOrder, MaintainanceBill, Fuel, VehicleTrack]:
                target_model.objects.filter(vehicle_number=default_vehi).update(
                    vehicle_number=vehicle_number, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name
                )
                target_model.objects.filter(vehicle_number=default_chasis).update(
                    vehicle_number=chasis, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name
                )
                target_model.objects.filter(vehicle_number=default_engine).update(
                    vehicle_number=engine, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name
                )
            messages.info(request, 'done')
            return redirect('vehicle_display')
    return redirect('vehicle_display')


@user_access
def search_vehicle(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        lookup = (
            Q(vehicle_number=search) | Q(url=search) | Q(chasis_number=search) | 
            Q(engine_number=search) | Q(vehicle_type=search) | Q(owner_name=search) | 
            Q(vehicle_number=sea) | Q(url=sea) | Q(chasis_number=sea) | 
            Q(engine_number=sea) | Q(vehicle_type=sea) | Q(owner_name=sea) | 
            Q(vehicle_number=se) | Q(url=se) | Q(chasis_number=se) | 
            Q(engine_number=se) | Q(vehicle_type=se) | Q(owner_name=se) | 
            Q(vehicle_number=s) | Q(url=s) | Q(chasis_number=s) | 
            Q(engine_number=s) | Q(vehicle_type=s) | Q(owner_name=s)
        )
        s_item = VehicleList.objects.filter(lookup).order_by('-id')
        v_type = VehicleType.objects.all().order_by('-id')
        context = {'s_item': s_item, 'search': search, 'v_type': v_type}
        return render(request, 'fuelmaintain/display/search_vehicle.html', context)
    return redirect('vehicle_display')


@user_access
def vehicle_delete(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        VehicleList.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('vehicle_display')
    return redirect('vehicle_display')


@user_access
def deactivate_vehicle(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        VehicleList.objects.filter(id=sid).update(active_status='no')
        messages.info(request, 'done')
        return redirect('vehicle_display')
    return redirect('vehicle_display')


# ==================== VEHICLE MOVEMENT TRACKING ====================

@user_access
def track_dash(request):
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
    
    newpei = (int(VehicleTrack.objects.last().move_count or 0) + 1) if VehicleTrack.objects.last() else 1
    u_site = user_site(request)
    site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
    context = {'v_type': v_type, 'u_site': u_site, 'vehis': vehis, 'newpei': newpei, 'site_dash': site_dash}
    return render(request, 'fuelmaintain/vehicle_track.html', context)


@user_access
def track_display(request):
    vehis = []
    seen = set()
    seen_add = seen.add
    ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for e in ent:
        vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
        n = len(vehi)
        vehis.append([vehi, range(1, n)])
    u_site = user_site(request)
    site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
    s_item = VehicleTrack.objects.all().order_by('-id')
    v_type = VehicleType.objects.all()
    context = {'s_item': s_item, 'v_type': v_type, 'vehis': vehis, 'site_dash': site_dash}
    return render(request, 'fuelmaintain/display/move_display.html', context)


@user_access
def move_add(request):
    if request.method == "POST":
        current_user = request.user.username
        date_str = request.POST.get('date')
        mid = request.POST.get('mid')
        mcount = request.POST.get('mcount')
        vtype = request.POST.get('vehicle_type')
        vtypeid = request.POST.get('vehicle_type_id')
        vnum = request.POST.get('vehicle')
        tosite = request.POST.get('site')
        fromsite = request.POST.get('issue_locate')
        num_type = request.POST.get('num_type')
        u_site = user_site(request)

        if VehicleTrack.objects.filter(entry_date=date_str, from_site=fromsite, to_site=tosite, vehicle_number=vnum).exists():
            messages.info(request, 'error')
            return redirect('vehicle_move')
        else:
            query = VehicleTrack(
                entry_date=date_str, move_number=mid, move_count=mcount, 
                vehicle_number=vnum, from_site=fromsite, to_site=tosite, 
                vehicle_type_id=vtypeid, vehicle_type=vtype, num_type=num_type, 
                user_site=u_site, entry_by=current_user
            )
            query.save()

            q = Notification(
                notify_topic='movement', content_id=query.id, content='move_add', 
                from_site=fromsite, from_user=current_user, content_val=mid, 
                content_val1=vnum, content_val2=tosite
            )
            q.save()

            messages.info(request, 'done')
            return redirect('vehicle_move')
    return redirect('vehicle_move')


@user_access
def move_update(request):
    if request.method == "POST":
        vid = request.POST.get('suid')
        date_str = request.POST.get('date')
        mid = request.POST.get('mid')
        vtype = request.POST.get('vehicle_type')
        vtypeid = request.POST.get('vehicle_type_id')
        vnum = request.POST.get('vehicle')
        tosite = request.POST.get('site')
        fromsite = request.POST.get('issue_locate')
        num_type = request.POST.get('num_type')

        if VehicleTrack.objects.filter(entry_date=date_str, from_site=fromsite, to_site=tosite, vehicle_number=vnum).exclude(id=vid).exists():
            messages.info(request, 'error')
            return redirect('move_display')
        else:
            VehicleTrack.objects.filter(id=vid).update(
                entry_date=date_str, num_type=num_type, vehicle_number=vnum, 
                vehicle_type_id=vtypeid, vehicle_type=vtype, to_site=tosite
            )
            Notification.objects.filter(content_val=mid).update(content_val1=vnum, content_val2=tosite)
            messages.info(request, 'done')
            return redirect('move_display')
    return redirect('move_display')


@user_access
def search_move(request):
    if request.method == "POST":
        search = request.POST.get('search', '')
        sea = search.upper()
        se = search.title()
        s = search.lower()
        lookup = (
            Q(vehicle_number__icontains=search) | Q(move_number__icontains=search) | 
            Q(from_site__icontains=search) | Q(to_site__icontains=search) | 
            Q(vehicle_type__icontains=search) | Q(vehicle_number__icontains=sea) | 
            Q(move_number__icontains=sea) | Q(from_site__icontains=sea) | 
            Q(to_site__icontains=sea) | Q(vehicle_type__icontains=sea) | 
            Q(vehicle_number__icontains=se) | Q(move_number__icontains=se) | 
            Q(from_site__icontains=se) | Q(to_site__icontains=se) | 
            Q(vehicle_type__icontains=se) | Q(vehicle_number__icontains=s) | 
            Q(move_number__icontains=s) | Q(from_site__icontains=s) | 
            Q(to_site__icontains=s) | Q(vehicle_type__icontains=s)
        )
        s_item = VehicleTrack.objects.filter(lookup).order_by('-id')
        v_type = VehicleType.objects.all()
        context = {'s_item': s_item, 'search': search, 'v_type': v_type}
        return render(request, 'fuelmaintain/display/search_move.html', context)
    return redirect('move_display')


@user_access
def move_delete(request):
    if request.method == "POST":
        sid = request.POST.get('sid')
        VehicleTrack.objects.filter(id=sid).delete()
        messages.info(request, 'done')
        return redirect('move_display')
    return redirect('move_display')


@user_access
def track_detail(request, vid):
    if VehicleTrack.objects.filter(id=vid).exists():
        u_site = user_site(request)
        site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
        s_item = VehicleTrack.objects.filter(id=vid).first()
        v_type = VehicleType.objects.all()
        context = {'item': s_item, 'v_type': v_type, 'site_dash': site_dash}
        return render(request, 'fuelmaintain/display/move_detail.html', context)
    return redirect('move_display')


def move_status(request):
    if request.method == "POST":
        u_site = user_site(request)
        sid = request.POST.get('sid')
        vt = VehicleTrack.objects.filter(id=sid).first()
        if vt and vt.to_site == u_site:
            date_str = request.POST.get('date')
            now = dt.now()
            current_time = now.strftime("%H:%M")
            arrive = date_str + ' ' + current_time
            VehicleTrack.objects.filter(id=sid).update(status="arrived", arrival_datetime=arrive)
            
            vnum = vt.vehicle_number
            ntype = vt.num_type
            if ntype == 'vehicle':
                VehicleList.objects.filter(vehicle_number=vnum).update(current=vt.to_site)
            elif ntype == 'chasis':
                VehicleList.objects.filter(chasis_number=vnum).update(current=vt.to_site)
            elif ntype == 'engine':
                VehicleList.objects.filter(engine_number=vnum).update(current=vt.to_site)
                
            messages.info(request, 'done')
            return redirect('/movement-detail/' + str(sid) + '/')
        else:
            messages.info(request, 'error')
            return redirect('/movement-detail/' + str(sid) + '/')
    return redirect('move_display')