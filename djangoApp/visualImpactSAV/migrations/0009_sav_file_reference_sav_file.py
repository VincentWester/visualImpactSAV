# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-23 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0008_sav_file_guarantee'),
    ]

    operations = [
        migrations.AddField(
            model_name='sav_file',
            name='reference_SAV_file',
            field=models.CharField(default='VIF-SAV-', max_length=100),
        ),
    ]