# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-11 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0030_auto_20181011_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sav_file',
            name='bill_customer',
            field=models.FileField(blank=True, upload_to=b'', verbose_name='Customer bill'),
        ),
    ]
