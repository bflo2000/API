from django.db import models

class Image(models.Model):
    source_identifier = models.CharField(max_length=64, null = True, blank=True)
    sku = models.CharField(max_length=16, unique=True, primary_key=True)
    root_sku = models.CharField(max_length=16, null=True)
    old_sku = models.CharField(max_length=200, null=True, blank=True)
    image_name = models.CharField(max_length=128)
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    short_title = models.CharField(max_length=200, null=True, blank=True)
    source_title = models.CharField(max_length=2000, null=True, blank=True)
    item_name = models.CharField(max_length=200, null=True, blank=True)
    original_image_name = models.CharField(max_length=200, null = True, blank=True)
    date = models.CharField(max_length=32, null=True, blank=True)
    product_description = models.CharField(max_length=10000, null=True, blank=True)
    photographer = models.CharField(max_length=72,  null=True, blank=True)
    artist = models.CharField(max_length=72,  null=True, blank=True)
    medium = models.CharField(max_length=72,  null=True, blank=True)
    format = models.CharField(max_length=72,  null=True, blank=True)
    reproduction_number = models.CharField(max_length=72,  null=True, blank=True)
    material_type = models.CharField(max_length=32, null=True, blank=True)
    category = models.CharField(max_length=64)
    sub_category = models.CharField(max_length=64, null=True, blank=True)
    collection = models.CharField(max_length=72)
    sub_collection = models.CharField(max_length=72, null=True, blank=True)
    image_folder = models.CharField(max_length=200, null=True, blank=True)
    hp_url = models.CharField(max_length=300, null=True, blank=True)
    source_url = models.CharField(max_length=300, null=True, blank=True)
    path = models.CharField(max_length=400, null=True, blank=True)
    notes = models.CharField(max_length=2000, null=True, blank=True)
    rights = models.CharField(max_length=2000, null=True, blank=True)
    original_keywords = models.CharField(max_length=2000, null=True, blank=True)
    additional_keywords = models.CharField(max_length=2000, null=True, blank=True)
    additional_keywords_source = models.CharField(max_length=200, null=True, blank=True)
