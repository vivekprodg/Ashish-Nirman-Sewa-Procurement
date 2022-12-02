from django.contrib import admin
from django import forms
from .models import *


class UserDetailAdmin(admin.ModelAdmin):
	list_display = ('user_name', 'first_name', 'last_name', 'email', 'role')


class OperationPermissionAdmin(admin.ModelAdmin):
	list_display = ('title', 'main_admin', 'main_staff', 'site_admin', 'site_staff', 'description', 'url')


class NotificationPermissionAdmin(admin.ModelAdmin):
	list_display = ('main_admin', 'main_staff', 'site_admin', 'site_staff', 'description', 'url')


admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(OperationPermission, OperationPermissionAdmin)
admin.site.register(NotificationPermission, NotificationPermissionAdmin)
