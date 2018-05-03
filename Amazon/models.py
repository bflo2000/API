from django.db import models
from Images.models import Image
from decimal import Decimal

class BulletPoint(models.Model):
	name = models.CharField(max_length=200, unique=True)
	bullet = models.CharField(max_length=200, unique=True)

class Amazon_Variation(models.Model):
	image_sku = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
	item_sku = models.CharField(max_length = 200, unique = True)
	item_name = models.CharField(max_length = 200)
	product_description = models.CharField(max_length = 2000)
	asin = models.CharField(max_length=64, null=True, blank=True)
	catalog_number = models.CharField(max_length=200, null=True, blank=True)
	part_number = models.CharField(max_length=200, null=True, blank=True)
	size_name = models.CharField(max_length=200, null=True, blank=True)
	variation_theme = models.CharField(max_length=200, null=True, blank=True)
	product_tax_code = models.CharField(max_length=200, null=True, blank=True)
	currency = models.CharField(max_length=16, null=True, blank=True)
	is_parent = models.BooleanField()
	is_orphan = models.BooleanField(default=True)
	is_unique = models.BooleanField(default=False)
	is_dirty = models.BooleanField(default=False)
	check_bullets = models.BooleanField(default=False)
	check_unicode = models.BooleanField(default=False)
	check_size = models.BooleanField(default=False)
	bullet1 = models.CharField(max_length=200, null=True, blank=True)
	bullet2 = models.CharField(max_length=200, null=True, blank=True)
	bullet3 = models.CharField(max_length=200, null=True, blank=True)
	bullet4 = models.CharField(max_length=200, null=True, blank=True)
	bullet5 = models.CharField(max_length=2000, null=True, blank=True)
	keywords = models.CharField(max_length=4000, null=True, blank=True)
	price = models.DecimalField(max_digits = 10, decimal_places=2, default=0)
	sales = models.IntegerField(default=0)

class Verification_Table(models.Model):
	sku = models.OneToOneField(Amazon_Variation, on_delete=models.CASCADE)
	size_verfied = models.BooleanField()
	bullets_verified = models.BooleanField()
	price_verified = models.BooleanField()
	keywords_verified = models.BooleanField()

