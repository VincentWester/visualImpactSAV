# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-05 00:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visualImpactSAV', '0005_remove_sav_file_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='sav_file',
            name='registred_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]