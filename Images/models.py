from django.db import models

class Image(models.Model):
    sku = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=128)
    height = models.IntegerField()
    width = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    material_type = models.CharField(max_length=32)
    category = models.CharField(max_length=64)
    sub_category = models.CharField(max_length=64)
    collection = models.CharField(max_length=72)
    sub_collection = models.CharField(max_length=72)
    url = models.CharField(max_length=200)
    path = models.CharField(max_length=400)
