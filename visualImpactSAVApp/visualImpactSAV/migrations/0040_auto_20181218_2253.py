# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-18 21:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0039_auto_20181128_0037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailandphone',
            name='in_session',
        ),
        migrations.DeleteModel(
            name='MailAndPhone',
        ),
        migrations.DeleteModel(
            name='SessionMailAndPhone',
        ),
    ]