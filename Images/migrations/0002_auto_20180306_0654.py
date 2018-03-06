# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-06 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Images', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image_height',
            new_name='height',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='item_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='main_image_path',
            new_name='path',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='item_sku',
            new_name='sku',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='main_image_url',
            new_name='url',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='image_width',
            new_name='width',
        ),
        migrations.AddField(
            model_name='image',
            name='description',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
