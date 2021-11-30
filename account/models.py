from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, uid, username, email, password=None, **extra_fields):
        if not uid:
            raise ValueError('UID number must be set')
        email = self.normalize_email(email)
        user = self.model(uid=uid, username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, uid, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(uid, username, email, password, **extra_fields)

    def create_superuser(self, uid, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(uid, username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Extends the Django's AbstractUser to create a customizable User model.
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), null=True, blank=True)
    uid = models.CharField(max_length=255, editable=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    picture = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'uid'
    objects = UserManager()

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self


class ReportUser(models.Model):
    """
    Model for tracking and storing user reports (to other users).
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

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.reported_by

    def __str__(self):
        return f'{self.reported_by} reported {self.reported_user}'

    class Meta:
        unique_together = ('reported_user', 'reported_by')


class BlockUser(models.Model):
    """
    Model of blocking/ignoring a user, the information will be used to filter out posts from blocked/ignored users.
    """
    to_user = models.ForeignKey(get_user_model(), verbose_name=_('blocked/ignored user'), on_delete=models.CASCADE)
    by_user = models.ForeignKey(get_user_model(), verbose_name=_('blocked/ignored by'),
                                related_name='ignore_blocked_users', on_delete=models.CASCADE)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.by_user

    class Meta:
        unique_together = ('to_user', 'by_user')
