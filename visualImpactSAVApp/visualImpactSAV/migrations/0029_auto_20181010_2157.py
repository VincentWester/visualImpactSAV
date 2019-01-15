# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-10 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0028_sav_file_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sav_file',
            old_name='mark_product',
            new_name='brand_product',
        ),
        migrations.AlterField(
            model_name='sav_file',
            name='status',
            field=models.CharField(choices=[('O', 'Ouvert'), ('IP', 'En attente'), ('P', 'En litige'), ('C', 'Ferm\xe9')], default='O', max_length=20, verbose_name='Status'),
        ),
    ]