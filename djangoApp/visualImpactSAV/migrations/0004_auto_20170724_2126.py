# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 21:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0003_auto_20170724_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='refered_SAV_file',
        ),
        migrations.RemoveField(
            model_name='sav_file',
            name='client',
        ),
        migrations.RemoveField(
            model_name='sav_file',
            name='product',
        ),
        migrations.RemoveField(
            model_name='sav_file',
            name='status',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='SAV_file',
        ),
    ]
