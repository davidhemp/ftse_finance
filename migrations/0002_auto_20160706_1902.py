# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-06 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ftsefinance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='which_stock',
            name='change',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]