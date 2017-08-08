# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.utils import timezone
from django import forms

class SAV_file_status(models.Model):
    libelle = models.CharField(max_length=50)
    class_css = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.libelle 

class Reparation_status(models.Model):
    libelle = models.CharField(max_length=50)

    def __unicode__(self):
        return self.libelle

DEFAULT_SAV_FILE_STATUS_ID = 1
DEFAULT_REPARATION_STATUS_ID = 1

class SAV_file(models.Model):
    creation_date = models.DateTimeField(default=timezone.now)
    file_reference = models.CharField(primary_key=True, max_length=50, default="0")
    
    sav_file_status = models.ForeignKey(SAV_file_status, default = DEFAULT_SAV_FILE_STATUS_ID)
    reparation_status = models.ForeignKey(Reparation_status, default = DEFAULT_REPARATION_STATUS_ID)

    name_client = models.CharField(max_length=300, default="")
    street_client = models.CharField(max_length=300, default="")
    zipcode_client = models.CharField(max_length=10, default="")
    city_client = models.CharField(max_length=10, default="")
    phone_client = models.CharField(max_length=30, default="")
    email_client = models.CharField(max_length=100, default="")

    name_product = models.CharField(max_length=200, default="")
    mark_product = models.CharField(max_length=200, default="")
    serial_number_product = models.CharField(max_length=200, default="")

    out_of_order_reason = models.TextField()
    file_import_export_note = models.FileField(blank=True)
    file_import_export_reparation_client_side = models.FileField(blank=True)
    file_import_export_reparation_furnisher_side = models.FileField(blank=True)
    tracking_number = models.CharField(max_length=100)

    def __unicode__(self):
        return self.file_reference 

class Event(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file)
    title = models.CharField(max_length=100)
    action = models.TextField()
    date = models.DateTimeField('date published')

