from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin import register

from .models import ReportUser, IgnoreBlockUser


@register(get_user_model())
class UserAdmin(admin.AdminSite):
    pass


@register(ReportUser)
class ReportUserAdmin(admin.AdminSite):
    pass


@register(IgnoreBlockUser)
class IgnoreBlockUserAdmin(admin.AdminSite):
    pass
