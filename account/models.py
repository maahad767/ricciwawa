from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Extends the Django's AbstractUser to create a customizable User model.
    """
    pass


class ReportUser(models.Model):
    """
    Model for tracking and storing user reports (to other users).
    status = (
        (0, 'pending'),
        (1, 'reviewed'),
    )
    """
    STATUS = (
        (0, 'pending'),
        (1, 'reviewed'),
    )
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('reported user'),
                                      on_delete=models.CASCADE)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('reported by'),
                                    related_name='reports', on_delete=models.CASCADE)
    reasoning = models.TextField(_('comments/reasoning'))
    comment = models.TextField(_('comment by reviewer'), null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS, default=0)
    attachment = models.FileField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return f'{self.reported_by} reported {self.reported_user}'


class IgnoreBlockUser(models.Model):
    """
    Model of blocking/ignoring a user, the information will be used to filter out posts from blocked/ignored users.
    _type = (
        (0, 'ignored'),
        (1, 'blocked'),
    )
    """
    TYPES = (
        (0, 'ignored'),
        (1, 'blocked'),
    )

    to = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('blocked/ignored user'), on_delete=models.CASCADE)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('blocked/ignored by'),
                           related_name='ignore_blocked_users', on_delete=models.CASCADE)
    _type = models.SmallIntegerField(choices=TYPES, default=0)
