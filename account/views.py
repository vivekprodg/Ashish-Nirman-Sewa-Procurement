from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.urls import resolve
from django.db.models import Q

from .models import *
from eproc.models import Site
from eproc.decorators import user_access


def check_admin(user):
	return user.is_superuser


def check_staff(user):
	return user.is_staff


def login_user(request):
	if request.user.is_staff:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('user_name')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				if user.is_staff:
					login(request, user)
					return redirect('home')
				else:
					messages.info(request, 'error')
			else:
				messages.info(request, 'error')

	context = {}
	return render(request, 'login.html', context)


def logout_user(request):
	logout(request)
	return redirect('login_user')


@user_access
def registerUser(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['user_name']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		role = request.POST['role']
		site = request.POST.get('site')
		s = Site.objects.filter(name=site).first()
		s_role = s.role
		if s_role == 'admin' and role == 'admin':
			status = 'main_admin'
		if s_role == 'admin' and role == 'staff':
			status = 'main_staff'
		if s_role == 'staff' and role == 'admin':
			status = 'site_admin'
		if s_role == 'staff' and role == 'staff':
			status = 'site_staff'

		if User.objects.filter(username=username).exists():
			messages.info(request, 'error')
			return redirect('manage_user')
		elif User.objects.filter(email=email).exists():
			messages.info(request, 'error')
			return redirect('manage_user')
		else:
			user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
											password=password1, email=email)
			if role == 'staff':
				user.is_staff = True
			if role == 'admin':
				user.is_staff = True
				user.is_superuser = True
			user.save()
			user_id = user.id
			detail = UserDetail(user_id=user_id, user_name=username, first_name=first_name, last_name=last_name, email=email, role=role, site=site, status=status)
			detail.save()

			messages.info(request, 'done')
			return redirect('manage_user')


@user_passes_test(check_staff, login_url='login_user')
def manage_user(request):
	udet = UserDetail.objects.all()
	mat = UserDetail.objects.all().count()
	site_dash = Site.objects.all()
	ope = OperationPermission.objects.all().count()
	nott = NotificationPermission.objects.all().count()
	opera = ope + nott

	context = {'site_dash': site_dash, 'udet': udet, 'mat': mat, 'opera': opera}
	return render(request, 'account.html', context)


@user_access
def user_display(request):
	s_item = UserDetail.objects.all()
	site_dash = Site.objects.all()

	context = {'site_dash': site_dash, 's_item': s_item}
	return render(request, 'account_display.html', context)


@user_access
def user_update(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		site = request.POST.get('site')
		role = request.POST['role']
		user_id = request.POST['user_id']
		uid = request.POST['uid']

		if first_name != '' and last_name != '' and role != '':
			User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name)
			user = User.objects.filter(id=user_id).first()
			UserDetail.objects.filter(id=uid).update(first_name=first_name, last_name=last_name, site=site, role=role)
			if role == 'admin':
				user.is_staff = True
				user.is_superuser = True
				user.save()
			if role == 'staff':
				user.is_staff = True
				user.is_superuser = False
				user.save()

			messages.info(request, 'done')
		return redirect('user_display')
	else:
		return redirect('user_display')


@user_access
def changeProfilePassword(request):
	if request.method == 'POST':
		current_user = request.user.username
		password1 = request.POST['password1']

		u = User.objects.get(username__exact=current_user)
		u.set_password(password1)
		u.save()

		messages.info(request, 'Password changed successfully ')
		return redirect('profile')


@user_access
def changeUserPassword(request):
	if request.method == 'POST':
		c_user = request.POST['user']
		password1 = request.POST['password1']

		u = User.objects.get(username__exact=c_user)
		u.set_password(password1)
		u.save()

		messages.info(request, 'done')
		return redirect('user_display')
	else:
		return redirect('user_display')


@user_access
def delete_user(request):
	if request.method == 'POST':
		uid = request.POST.get('uid')
		user_id = request.POST.get('user_id')

		User.objects.filter(id=user_id).delete()
		UserDetail.objects.filter(id=uid).delete()

		messages.info(request, 'done')
		return redirect('user_display')
	else:
		return redirect('user_display')


@user_access
def manage_permission(request):
	mao = []
	seen = set()
	seen_add = seen.add
	tran = OperationPermission.objects.values_list('title', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		main_admin_op = OperationPermission.objects.filter(title=s)
		n = len(main_admin_op)
		mao.append([main_admin_op, range(1,n)])

	mso = []
	seen = set()
	seen_add = seen.add
	tran = OperationPermission.objects.values_list('title', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		main_staff_op = OperationPermission.objects.filter(title=s)
		n = len(main_staff_op)
		mso.append([main_staff_op, range(1,n)])

	sao = []
	seen = set()
	seen_add = seen.add
	tran = OperationPermission.objects.values_list('title', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		site_admin_op = OperationPermission.objects.filter(title=s)
		n = len(site_admin_op)
		sao.append([site_admin_op, range(1,n)])

	sso = []
	seen = set()
	seen_add = seen.add
	tran = OperationPermission.objects.values_list('title', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		site_staff_op = OperationPermission.objects.filter(title=s)
		n = len(site_staff_op)
		sso.append([site_staff_op, range(1,n)])
		
	main_admin_noti = NotificationPermission.objects.all().order_by('id')
	main_staff_noti = NotificationPermission.objects.all().order_by('id')
	site_admin_noti = NotificationPermission.objects.all().order_by('id')
	site_staff_noti = NotificationPermission.objects.all().order_by('id')
	context = {'mao': mao, 'mso': mso, 'sao': sao, 'sso': sso, 'main_admin_noti': main_admin_noti, 'main_staff_noti': main_staff_noti, 'site_admin_noti': site_admin_noti, 'site_staff_noti': site_staff_noti}    
	return render(request, 'permission.html', context)



@user_access
def update_operation_permission(request):
	if request.method == 'POST':
		pid = request.POST.get('pid')
		status = request.POST.get('status')
		use = request.POST.get('user')
		if use == 'main_admin':
			OperationPermission.objects.filter(id=pid).update(main_admin=status)
		if use == 'main_staff':
			OperationPermission.objects.filter(id=pid).update(main_staff=status)
		if use == 'site_admin':
			OperationPermission.objects.filter(id=pid).update(site_admin=status)
		if use == 'site_staff':
			OperationPermission.objects.filter(id=pid).update(site_staff=status)

		return HttpResponse()
	else:
		return redirect('manage_permission')


@user_access
def update_notify_permission(request):
	if request.method == 'POST':
		pid = request.POST.get('pid')
		status = request.POST.get('status')
		use = request.POST.get('user')
		if use == 'main_admin':
			NotificationPermission.objects.filter(id=pid).update(main_admin=status)
		if use == 'main_staff':
			NotificationPermission.objects.filter(id=pid).update(main_staff=status)
		if use == 'site_admin':
			NotificationPermission.objects.filter(id=pid).update(site_admin=status)
		if use == 'site_staff':
			NotificationPermission.objects.filter(id=pid).update(site_staff=status)

		return HttpResponse()
	else:
		return redirect('manage_permission')


@user_access
def deactivate_user(request):
	if request.method == 'POST':
		uid = request.POST.get('uid')
		user_id = request.POST.get('user_id')

		u = User.objects.get(id=user_id)
		u.is_staff = False
		u.is_superuser = False
		u.is_active = False
		u.save()
		UserDetail.objects.filter(id=uid).update(active_status='no')

		messages.info(request, 'done')
		return redirect('user_display')
	else:
		return redirect('user_display')