from django.contrib import admin

from service import models

# Register your models here.
admin.site.register(models.Service)
admin.site.register(models.ServiceRate)
admin.site.register(models.Region)
admin.site.register(models.City)
admin.site.register(models.Street)
