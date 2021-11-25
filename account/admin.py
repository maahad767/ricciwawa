from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin import register
from django.utils.translation import gettext_lazy as _
from .models import ReportUser, BlockUser


@register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('uid', 'username', 'email')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'picture')}),

        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'picture', 'is_staff',
                       'is_superuser'),
        }),
    )
    list_display = ('uid', 'username', 'email', 'is_superuser')
    search_fields = ('username', 'email', 'uid')
    ordering = ('username',)
    readonly_fields = ('uid',)
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_superuser')

    def has_add_permission(self, request, *args, **kwargs):
        return False


@register(ReportUser)
class ReportUserAdmin(admin.ModelAdmin):
    pass


@register(BlockUser)
class IgnoreBlockUserAdmin(admin.ModelAdmin):
    pass
