# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-27 23:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0038_auto_20181127_2227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailandphone',
            options={'ordering': ['name'], 'verbose_name': 'contact', 'verbose_name_plural': 'contacts'},
        ),
        migrations.RenameField(
            model_name='mailandphone',
            old_name='email_customer',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='mailandphone',
            old_name='name_customer',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='mailandphone',
            old_name='phone_customer',
            new_name='phone',
        ),
    ]
