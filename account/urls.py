from django.urls import path
from . import views


urlpatterns = [
	path('', views.manage_user, name='manage_user'),
	path('login/', views.login_user, name='login_user'),
	path('logout/', views.logout_user, name='logout_user'),
	path('user-display/', views.user_display, name='user_display'),
	path('register/', views.registerUser, name='registerUser'),
	path('update-user/', views.user_update, name='user_update'),
	path('delete-user/', views.delete_user, name='delete_user'),
	path('change-profile-password/', views.changeProfilePassword, name='changeProfilePassword'),
	path('change-user-password/', views.changeUserPassword, name='changeUserPassword'),
	path('manage-permissions/', views.manage_permission, name='manage_permission'),
	path('update-operation-permission/', views.update_operation_permission, name='update_operation_permission'),
	path('update-notify-permission/', views.update_notify_permission, name='update_notify_permission'),
	path('deactivate-user/', views.deactivate_user, name='deactivate_user'),
]