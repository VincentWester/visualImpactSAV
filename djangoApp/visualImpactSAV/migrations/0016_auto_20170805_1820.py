# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0015_sav_file_status_class_css'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sav_file_status',
            name='class_css',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
