from django.db import models

class BulletPoint(models.Model):
	name = models.CharField(max_length=200, unique=True)
    bullet = models.CharField(max_length=200, unique=True)

class Variation(models.Model):
	parent = models.ForeignKey()
	catalog_number = models.CharField()
	size_name = models.CharField()
	variation_theme = models.CharField()
	product_tax_code = models.CharField()
	image_name = models.CharField()
	bullet1 = models.CharField()
	bullet2 = models.CharField()
	bullet3 = models.CharField()
	bullet4 = models.CharField()
	bullet5 = models.CharField()