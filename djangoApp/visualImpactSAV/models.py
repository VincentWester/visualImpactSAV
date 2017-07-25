# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

class Address(models.Model):
    street = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=10)

    def __unicode__(self):
        return "{} - {} - {}".format(self.street, self.zipcode, self.city) 	

class Client(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.CharField(max_length=400)
    address = models.OneToOneField(Address)

    def __unicode__(self):
        return "{} {}".format(self.surname, self.name) 

class Product(models.Model):
    serial_number = models.CharField(max_length=50)
    mark = models.CharField(max_length=50)
    model = models.CharField(max_length=100)

    def __unicode__(self):
        return "{} - {} {}".format(self.serial_number, self.mark, self.model)

class SAV_file_status(models.Model):
    libelle = models.CharField(max_length=50)

    def __unicode__(self):
        return self.libelle 

DEFAULT_STATUS_ID = 1
DEFAULT_CLIENT_ID = 1
DEFAULT_PRODUCT_ID = 1

class SAV_file(models.Model):
    file_reference = models.CharField(primary_key=True, max_length=50, default="0")
    status = models.ForeignKey(SAV_file_status, default = DEFAULT_STATUS_ID)
    client = models.ForeignKey(Client, default = DEFAULT_CLIENT_ID)
    product_referenced = models.ForeignKey(Product, default = DEFAULT_PRODUCT_ID)
    out_of_order_reason = models.TextField()
    file_import_export_note = models.FileField(blank=True)
    file_import_export_reparation_client_side = models.FileField(blank=True)
    file_import_export_reparation_furnisher_side = models.FileField(blank=True)
    reparation_validated = models.BooleanField(default=False)
    tracking_number = models.CharField(max_length=100)

    def __unicode__(self):
        return self.file_reference 

class Event(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file)
    title = models.CharField(max_length=100)
    action = models.TextField()
    date = models.DateTimeField('date published')

