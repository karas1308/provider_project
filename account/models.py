from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from service.models import Address


# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=100, unique=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith(('sha1$', 'bcrypt$', 'pbkdf2_sha256$')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
