# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-18 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Amazon', '0002_remove_amazon_variation_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazon_variation',
            name='part_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='amazon_variation',
            name='catalog_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
