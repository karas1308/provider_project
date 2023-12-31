from django.db import models

from account.models import User
from common import get_utc_date_time
from service.models import Service


# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    order_id = models.CharField(max_length=36)
    amount = models.IntegerField()
    successful_payment = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=get_utc_date_time())
    expired_at = models.DateTimeField(default=get_utc_date_time(hours=1))
    is_expired = models.BooleanField(default=False)
