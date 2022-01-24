from django.db import models


class VersionInfo(models.Model):
    """
    Model for the version information.
    """
    min_version_number = models.PositiveIntegerField()
    latest_version_number = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now_add=True)


