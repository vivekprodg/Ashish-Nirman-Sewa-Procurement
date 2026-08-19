from django.shortcuts import redirect
from account.models import UserDetail, OperationPermission
from django.urls import resolve
from django.db.models import Q


def user_access(func):
    def decorated(request, *args, **kwargs):
        # 1. Ensure user is logged in and is staff
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('login_user')

        # 2. Superusers bypass custom permission restrictions
        if request.user.is_superuser:
            return func(request, *args, **kwargs)

        # 3. Fetch UserDetail profile safely
        current_user = request.user.id
        use = UserDetail.objects.filter(user_id=current_user).first()

        if not use or not use.status:
            return redirect('login_user')

        status = use.status
        current_url = resolve(request.path_info).url_name

        # 4. Check URL permissions based on user status
        url_query = (
            Q(url_name=current_url) | Q(url_name1=current_url) | Q(url_name2=current_url) | 
            Q(url_name3=current_url) | Q(url_name4=current_url) | Q(url_name5=current_url) | 
            Q(url_name6=current_url) | Q(url_name7=current_url) | Q(url_name8=current_url) | 
            Q(url_name9=current_url) | Q(url_name10=current_url) | Q(url_name11=current_url)
        )

        if status == 'main_admin':
            if not OperationPermission.objects.filter(url_query & Q(main_admin='yes')).exists():
                return redirect('login_user')
        elif status == 'main_staff':
            if not OperationPermission.objects.filter(url_query & Q(main_staff='yes')).exists():
                return redirect('login_user')
        elif status == 'site_admin':
            if not OperationPermission.objects.filter(url_query & Q(site_admin='yes')).exists():
                return redirect('login_user')
        elif status == 'site_staff':
            if not OperationPermission.objects.filter(url_query & Q(site_staff='yes')).exists():
                return redirect('login_user')
        else:
            return redirect('login_user')

        return func(request, *args, **kwargs)
    return decorated