from django.db import models


class VersionInfo(models.Model):
    """
    Model for the version information.
    """
    min_build_number = models.PositiveIntegerField()
    latest_build_number = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now_add=True)


