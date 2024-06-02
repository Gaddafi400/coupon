from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email
