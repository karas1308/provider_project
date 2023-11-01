from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=255)
    entry = models.TextField()
    media = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
