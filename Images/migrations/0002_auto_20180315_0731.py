# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-15 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]