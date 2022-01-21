from django.contrib import admin

from .models import VersionInfo


@admin.register(VersionInfo)
class VersionInfoAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return not VersionInfo.objects.exists()
