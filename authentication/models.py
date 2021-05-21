from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.contrib.contenttypes.models import ContentType
from django.db import models

from authentication.managers import UserManager


class Groups(models.Model):
    title = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    params = models.JSONField(default=dict)

    def __str__(self):
        return self.title


class EcomInformation(models.Model):
    title = models.CharField(max_length=255)
    law_definition = models.CharField(
        max_length=20,
        help_text='Наименование организационно-правовой формы'
    )
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=40, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Groups, related_name='users')
    company = models.ForeignKey(
        EcomInformation,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
