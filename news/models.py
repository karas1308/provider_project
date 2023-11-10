from django.db import models


# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=255)
    entry = models.TextField()
    media = models.ImageField(null=True, blank=True)
    create_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
