from django.db import models

class BulletPoint(models.Model):
	name = models.CharField(max_length=200, unique=True)
	bullet = models.CharField(max_length=200, unique=True)

class Variation(models.Model):
	#parent = models.ForeignKey()
	catalog_number = models.CharField(max_length=200)
	size_name = models.CharField(max_length=200)
	variation_theme = models.CharField(max_length=200)
	product_tax_code = models.CharField(max_length=200)
	image_name = models.CharField(max_length=200)
	bullet1 = models.CharField(max_length=200)
	bullet2 = models.CharField(max_length=200)
	bullet3 = models.CharField(max_length=200)
	bullet4 = models.CharField(max_length=200)
	bullet5 = models.CharField(max_length=200)