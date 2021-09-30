from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class ReportUser(models.Model):
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='reported user', on_delete=models.CASCADE)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='reported by', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='comments/reasoning')
    attachment = models.FileField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return f'{self.reported_by} reported {self.reported_user}'


class BlockUser(models.Model):
    blocked_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='blocked user', on_delete=models.CASCADE)
    blocked_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='blocked by', on_delete=models.CASCADE)
