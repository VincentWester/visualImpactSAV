# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-07 14:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0026_auto_20180929_1359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['date'], 'verbose_name': 'event', 'verbose_name_plural': 'events'},
        ),
    ]
