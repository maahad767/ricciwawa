from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin import register

from .models import ReportUser, IgnoreBlockUser


@register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    pass


@register(ReportUser)
class ReportUserAdmin(admin.ModelAdmin):
    pass


@register(IgnoreBlockUser)
class IgnoreBlockUserAdmin(admin.ModelAdmin):
    pass
