def notify_everywhere(request):
	import datetime
	from django.db.models import Q
	from account.models import UserDetail, NotificationPermission
	from eproc.models import Notification
	if request.user.is_staff:
		notify  = []
		checked = []
		len1 = 0
		len2 = 0
		noti_c = 0
		current_user = request.user.username
		udet = UserDetail.objects.filter(user_name=current_user).first()
		status = udet.status
		if status == 'main_admin':
			npp = []
			np = NotificationPermission.objects.filter(main_admin='yes')
			for i in np:
				ii = i.url
				npp.append(ii)
			notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
			checked = Notification.objects.filter(notify_topic__in=npp, status='checked').order_by('-id')
			noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
			# lookup1 = Q(Q(notify_topic='purchase_order') | Q(notify_topic='grn') | Q(notify_topic='purchase_invoice_entry') | Q(notify_topic='material_issue') | Q(notify_topic='internal_transfer') | Q(notify_topic='out_sales_entry')) & Q(status='pending') & Q(main_admin='yes')
			# lookup2 = Q(Q(notify_topic='purchase_order') | Q(notify_topic='grn') | Q(notify_topic='purchase_invoice_entry') | Q(notify_topic='material_issue') | Q(notify_topic='internal_transfer') | Q(notify_topic='out_sales_entry')) & Q(status='checked') & Q(main_admin='yes')
		if status == 'main_staff':
			npp = []
			np = NotificationPermission.objects.filter(main_staff='yes')
			for i in np:
				ii = i.url
				npp.append(ii)
			notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
			checked = Notification.objects.filter(notify_topic__in=npp, status='checked').order_by('-id')
			noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
		if status == 'site_admin':
			npp = []
			np = NotificationPermission.objects.filter(site_admin='yes')
			for i in np:
				ii = i.url
				npp.append(ii)
			notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
			checked = Notification.objects.filter(notify_topic__in=npp, status='checked').order_by('-id')
			noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
		if status == 'site_staff':
			npp = []
			np = NotificationPermission.objects.filter(site_staff='yes')
			for i in np:
				ii = i.url
				npp.append(ii)
			notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
			checked = Notification.objects.filter(notify_topic__in=npp, status='checked').order_by('-id')
			noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
		len1 = len(notify)
		len2 = len(checked)
		context = {'noti_c': noti_c, 'notify': notify, 'checked': checked, 'len1': len1, 'len2': len2}    
		return context
	else:
		return {}
