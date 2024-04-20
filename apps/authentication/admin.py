from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from smtplib import SMTPException
from .models import User


# Monkey patch: Unregister django user admin
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Custom user model admin.
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'account_status')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'),
        }),
        (_('Important dates'),
            {'fields': ('last_login', 'date_joined')}),
    )
