# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-11 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0018_auto_20180709_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designation',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=18),
        ),
    ]
