# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=10)

class Client(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.CharField(max_length=400)
    address = models.OneToOneField(Address)

class Product(models.Model):
    serial_number = models.CharField(max_length=50)
    mark = models.CharField(max_length=50)
    model = models.CharField(max_length=100)

class SAV_file_status(models.Model):
    libelle = models.CharField(max_length=50)

class SAV_file(models.Model):
    status = models.ForeignKey(SAV_file_status)
    client = models.ForeignKey(Client)
    product = models.ForeignKey(Product)
    out_of_order_reason = models.TextField()
    file_import_export_note = models.FileField()
    file_import_export_reparation_client_side = models.FileField()
    file_import_export_reparation_furnisher_side = models.FileField()
    reparation_validated = models.BooleanField()
    traking_number = models.CharField(max_length=100)

class Event(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file)
    title = models.CharField(max_length=100)
    action = models.TextField()
    date = models.DateTimeField('date published')

