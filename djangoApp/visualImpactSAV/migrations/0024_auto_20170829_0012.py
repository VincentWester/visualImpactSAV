# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 00:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visualImpactSAV', '0023_auto_20170828_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pdf_generation_file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(default='invoice_client.pdf', max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='pdf_client_invoice_file',
            name='refered_sav_file',
        ),
        migrations.AlterField(
            model_name='designation',
            name='refered_pdf_client_invoice_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualImpactSAV.SAV_file'),
        ),
        migrations.DeleteModel(
            name='Pdf_client_invoice_file',
        ),
    ]
