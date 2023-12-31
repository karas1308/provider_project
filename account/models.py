from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from common import get_utc_date_time
from service.models import Building, City, Region, Service, Street


# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=100, unique=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.password.startswith(('sha1$', 'bcrypt$', 'pbkdf2_sha256$')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default="")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, default="")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    apt = models.IntegerField(blank=True, null=True)
    entrance = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)


class UserService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    active_date = models.DateField(default=get_utc_date_time(date_format="%Y-%m-%d"))
    is_active = models.BooleanField(default=True)
