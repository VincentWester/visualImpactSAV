# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-25 22:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0023_auto_20180925_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='furnisher',
            name='mark',
        ),
    ]
