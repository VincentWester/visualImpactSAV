# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-26 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(default='', max_length=100)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('action', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Reparation_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SAV_file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('society_client', models.CharField(blank=True, default='', max_length=300)),
                ('name_client', models.CharField(default='', max_length=300)),
                ('street_client', models.CharField(default='', max_length=300)),
                ('zipcode_client', models.CharField(default='', max_length=10)),
                ('city_client', models.CharField(default='', max_length=10)),
                ('phone_client', models.CharField(default='', max_length=30)),
                ('email_client', models.CharField(default='', max_length=100)),
                ('name_product', models.CharField(default='', max_length=200)),
                ('mark_product', models.CharField(default='', max_length=200)),
                ('serial_number_product', models.CharField(default='', max_length=200)),
                ('tracking_number', models.CharField(blank=True, max_length=100)),
                ('out_of_order_reason', models.TextField()),
                ('client_bill', models.FileField(blank=True, upload_to=b'')),
                ('furnisher_invoice', models.FileField(blank=True, upload_to=b'')),
                ('reparation_status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='visualImpactSAV.Reparation_status')),
            ],
        ),
        migrations.CreateModel(
            name='SAV_file_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('class_css', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='sav_file',
            name='sav_file_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='visualImpactSAV.SAV_file_status'),
        ),
        migrations.AddField(
            model_name='event',
            name='refered_SAV_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualImpactSAV.SAV_file'),
        ),
        migrations.AddField(
            model_name='designation',
            name='refered_SAV_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualImpactSAV.SAV_file'),
        ),
    ]
