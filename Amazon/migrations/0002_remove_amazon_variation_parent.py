# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-18 20:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Amazon', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amazon_variation',
            name='parent',
        ),
    ]
