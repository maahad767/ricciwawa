from django.db import models


class VersionInfo(models.Model):
    """
    Model for the version information.
    """
    min_version = models.DecimalField(max_digits=6, decimal_places=3)
    latest_version = models.DecimalField(max_digits=6, decimal_places=3)
    updated_at = models.DateTimeField(auto_now_add=True)


