# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-26 12:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0034_auto_20181016_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='designation',
            options={'ordering': ['id'], 'verbose_name': 'designation', 'verbose_name_plural': 'designations'},
        ),
    ]
