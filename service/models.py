from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255)
    media = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.name


class ServiceRate(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True)

    def __str__(self):
        return self.service.name


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Street(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    building = models.IntegerField()
    apt = models.IntegerField(blank=True)
    entrance = models.IntegerField(blank=True)
    floor = models.IntegerField(blank=True)
