from django.db import models
from Images.models import Image

class BulletPoint(models.Model):
	name = models.CharField(max_length=200, unique=True)
	bullet = models.CharField(max_length=200, unique=True)

class Amazon_Variation(models.Model):
	parent_sku = models.OneToOneField(Image, on_delete=models.CASCADE)
	item_sku = models.CharField(max_length = 200)
	item_name = models.CharField(max_length = 200)
	product_description = models.CharField(max_length = 200)
	asin = models.CharField(max_length=64)
	catalog_number = models.CharField(max_length=200)
	size_name = models.CharField(max_length=200, null=True, blank=True)
	variation_theme = models.CharField(max_length=200)
	product_tax_code = models.CharField(max_length=200)
<<<<<<< HEAD
	currency = models.CharField(max_length=16)
	parent = models.BooleanField()
=======
	is_parent = models.BooleanField()
>>>>>>> 4b5d93095bd996e5a54d6e18d3578b92a484b261
	bullet1 = models.CharField(max_length=200)
	bullet2 = models.CharField(max_length=200)
	bullet3 = models.CharField(max_length=200)
	bullet4 = models.CharField(max_length=200)
	bullet5 = models.CharField(max_length=200)
	keywords = models.CharField(max_length=20000)
<<<<<<< HEAD
	sales = models.DecimalField(max_digits = 10, decimal_places=2)

class Verification_Table(models.Model):
	sku = models.OneToOneField(Amazon_Variation, on_delete=models.CASCADE)
	size_verfied = models.BooleanField()
	bullets_verified = models.BooleanField()
	price_verified = models.BooleanField()
	keywords_verified = models.BooleanField()
=======
	price = models.DecimalField(max_digits = 10, decimal_places=2, null=True, blank=True)
	sales = models.IntegerField()
>>>>>>> 4b5d93095bd996e5a54d6e18d3578b92a484b261
