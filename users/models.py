from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager
from users.config import Role
from erp.models import TimeStamp


class User(AbstractUser, TimeStamp):
    username = None
    email = models.EmailField(_("email"), max_length=254, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(TimeStamp):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
        verbose_name=_("role"),
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        blank=True,
        null=True,
    )
    subscription_start_date = models.DateTimeField(blank=True, null=True)
    subscription_end_date = models.DateTimeField(blank=True, null=True)
