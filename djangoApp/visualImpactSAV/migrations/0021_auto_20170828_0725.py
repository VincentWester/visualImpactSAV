# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-28 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0020_auto_20170828_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sav_file',
            name='society_client',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='sav_file',
            name='tracking_number',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
