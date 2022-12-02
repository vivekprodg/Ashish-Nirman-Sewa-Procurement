from django.shortcuts import redirect
from account.models import UserDetail, OperationPermission
from django.urls import resolve
from django.db.models import Q

def user_access(func):
	def decorated(request, *args, **kwargs):
		if request.user.is_staff:
			current_user = request.user.id
			use = UserDetail.objects.filter(user_id=current_user).first()
			status = use.status
			if status != '' and status != None: 
				current_url = resolve(request.path_info).url_name
				if status == 'main_admin':
					lookup = Q(Q(url_name=current_url) | Q(url_name1=current_url) | Q(url_name2=current_url) | Q(url_name3=current_url) | Q(url_name4=current_url) | Q(url_name5=current_url) | Q(url_name6=current_url) | Q(url_name7=current_url) | Q(url_name8=current_url) | Q(url_name9=current_url) | Q(url_name10=current_url) | Q(url_name11=current_url)) & Q(main_admin='yes')
					if not OperationPermission.objects.filter(lookup).exists():
						return redirect('login_user')
				if status == 'main_staff':
					lookup = Q(Q(url_name=current_url) | Q(url_name1=current_url) | Q(url_name2=current_url) | Q(url_name3=current_url) | Q(url_name4=current_url) | Q(url_name5=current_url) | Q(url_name6=current_url) | Q(url_name7=current_url) | Q(url_name8=current_url) | Q(url_name9=current_url) | Q(url_name10=current_url) | Q(url_name11=current_url)) & Q(main_staff='yes')
					if not OperationPermission.objects.filter(lookup).exists():
						return redirect('login_user')
				if status == 'site_admin':
					lookup = Q(Q(url_name=current_url) | Q(url_name1=current_url) | Q(url_name2=current_url) | Q(url_name3=current_url) | Q(url_name4=current_url) | Q(url_name5=current_url) | Q(url_name6=current_url) | Q(url_name7=current_url) | Q(url_name8=current_url) | Q(url_name9=current_url) | Q(url_name10=current_url) | Q(url_name11=current_url)) & Q(site_admin='yes')
					if not OperationPermission.objects.filter(lookup).exists():
						return redirect('login_user')
				if status == 'site_staff':
					lookup = Q(Q(url_name=current_url) | Q(url_name1=current_url) | Q(url_name2=current_url) | Q(url_name3=current_url) | Q(url_name4=current_url) | Q(url_name5=current_url) | Q(url_name6=current_url) | Q(url_name7=current_url) | Q(url_name8=current_url) | Q(url_name9=current_url) | Q(url_name10=current_url) | Q(url_name11=current_url)) & Q(site_staff='yes')
					if not OperationPermission.objects.filter(lookup).exists():
						return redirect('login_user')
			else:
				return redirect('login_user')
		else:
			return redirect('login_user')
		return func(request, *args, **kwargs)
	return decorated