from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extends the Django's AbstractUser to create a customizable User model.
    """
    pass


class ReportUser(models.Model):
    """
    Model for tracking and storing user reports (to other users).
    """
    STATUS = (
        (0, 'pending'),
        (1, 'reviewed'),
    )
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='reported user', on_delete=models.CASCADE)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='reported by', on_delete=models.CASCADE)
    reasoning = models.TextField(verbose_name='comments/reasoning')
    comment = models.TextField(verbose_name='comment by reviewer', null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS, default=0)
    attachment = models.FileField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return f'{self.reported_by} reported {self.reported_user}'


class IgnoreBlockUser(models.Model):
    """
    Model of blocking/ignoring a user
    """
    TYPES = (
        (0, 'ignored'),
        (1, 'blocked'),
    )

    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='blocked/ignored user', on_delete=models.CASCADE)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='blocked/ignored by', on_delete=models.CASCADE)
    _type = models.SmallIntegerField(choices=TYPES, default=0)
