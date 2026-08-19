from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Q

from eproc.models import Notification
from account.models import UserDetail, NotificationPermission


def notify(request):
    notify_list = []
    checked_list = []
    noti_c = 0
    current_user = request.user.username
    udet = UserDetail.objects.filter(user_name=current_user).first()
    
    if udet:
        status = udet.status
        npp = [i.url for i in NotificationPermission.objects.filter(**{status: 'yes'})] if status else []

        notify_list = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
        checked_list = Notification.objects.filter(notify_topic__in=npp, status='checked').order_by('-id')
        noti_c = notify_list.count()

    len1 = len(notify_list)
    len2 = len(checked_list)
    context = {'noti_c': noti_c, 'notify': notify_list, 'checked': checked_list, 'len1': len1, 'len2': len2}    
    return render(request, 'display/notify.html', context)


def noti_count(request):
    noti_c = 0
    current_user = request.user.username
    udet = UserDetail.objects.filter(user_name=current_user).first()
    
    if udet:
        status = udet.status
        site = udet.site
        if status in ['main_admin', 'main_staff']:
            npp = [i.url for i in NotificationPermission.objects.filter(**{status: 'yes'})]
            noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
        elif status in ['site_admin', 'site_staff']:
            npp = [i.url for i in NotificationPermission.objects.filter(**{status: 'yes'})]
            noti_c = Notification.objects.filter(
                Q(Q(notify_topic__in=npp) & Q(status='pending')) & 
                Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))
            ).count()

    context = {'noti_c': noti_c}    
    return render(request, 'display/noti_count.html', context)


def noti(request):
    notify_list = []
    checked_list = []
    noti_c = 0
    current_user = request.user.username
    udet = UserDetail.objects.filter(user_name=current_user).first()
    todate = date.today()
    
    if udet:
        status = udet.status
        site = udet.site
        if status in ['main_admin', 'main_staff']:
            npp = [i.url for i in NotificationPermission.objects.filter(**{status: 'yes'})]
            notify_list = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
            checked_list = Notification.objects.filter(notify_topic__in=npp, status='checked', date_on=todate).order_by('-id')
            noti_c = notify_list.count()
        elif status in ['site_admin', 'site_staff']:
            npp = [i.url for i in NotificationPermission.objects.filter(**{status: 'yes'})]
            notify_list = Notification.objects.filter(
                Q(Q(notify_topic__in=npp) & Q(status='pending')) & 
                Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))
            ).order_by('-id')
            checked_list = Notification.objects.filter(
                Q(Q(notify_topic__in=npp) & Q(status='checked') & Q(date_on=todate)) & 
                Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))
            ).order_by('-id')
            noti_c = notify_list.count()

    len1 = len(notify_list)
    len2 = len(checked_list)
    context = {'notify': notify_list, 'checked': checked_list, 'len1': len1, 'len2': len2}    
    return render(request, 'display/noti.html', context)


def notify_check(request, nid, nt, cid):
    if Notification.objects.filter(id=nid).exists():
        Notification.objects.filter(id=nid).update(status='checked')
        
        redirection_map = {
            'purchase_order': f'/purchase-order-detail/{cid}/',
            'grn': f'/ashish-goods-detail/{cid}/',
            'purchase_invoice_entry': f'/ashish-invoice-detail/{cid}/',
            'material_issue': f'/material-issue-detail/{cid}/',
            'internal_transfer': f'/internal-transfer-detail/{cid}/',
            'transfer_grn': f'/transfer-goods-detail/{cid}/',
            'out_sales_entry': f'/sales-detail/{cid}/',
            'fuel_purchase_order': f'/fuel-purchase-order-detail/{cid}/',
            'damage_entry': f'/damage-detail/{cid}/',
            'return_entry': f'/return-detail/{cid}/',
            'movement': f'/movement-detail/{cid}/',
            'grn_notify': f'/ashish-invoice-detail/{cid}/',
            'credit_notify': f'/ashish-invoice-detail/{cid}/',
            'internal_damage_entry': f'/internal-damage-detail/{cid}/',
        }
        
        target_url = redirection_map.get(nt, 'home')
        return redirect(target_url)
    return redirect('home')