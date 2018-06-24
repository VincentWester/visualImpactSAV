# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-24 02:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0015_auto_20180514_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guarantee',
            name='complements',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='sav_file',
            name='furnisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='visualImpactSAV.Furnisher'),
        ),
    ]