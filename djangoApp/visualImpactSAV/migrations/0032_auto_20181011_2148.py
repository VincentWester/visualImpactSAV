# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-11 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0031_auto_20181011_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sav_file',
            name='guarantee',
            field=models.CharField(choices=[('IW', 'Sous garantie'), ('EW', 'Hors garantie')], default='IW', max_length=100, verbose_name='Waranty'),
        ),
    ]
