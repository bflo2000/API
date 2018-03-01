from django.db import models

class Image(models.Model):
    item_sku = models.CharField(max_length=16)
    item_name = models.CharField(max_length=16)
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    main_image_url = models.CharField(max_length=200)
    main_image_path = models.CharField(max_length=400)
    category = models.CharField(max_length=16)
    collection = models.CharField(max_length=72)
    sub_collection = models.CharField(max_length=72)

