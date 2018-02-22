# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from datetime import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

class SAV_file_status(models.Model):
    libelle = models.CharField(max_length=50)
    class_css = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.libelle 

DEFAULT_SAV_FILE_STATUS_ID = 1

class SAV_file(models.Model):
    creation_date = models.DateTimeField(default=timezone.now)    
    sav_file_status = models.ForeignKey(SAV_file_status, default = DEFAULT_SAV_FILE_STATUS_ID)
    society_client = models.CharField(max_length=300, default="", blank=True)
    name_client = models.CharField(max_length=300, default="")
    street_client = models.CharField(max_length=300, default="")
    zipcode_client = models.CharField(max_length=10, default="")
    city_client = models.CharField(max_length=10, default="")
    phone_client = models.CharField(max_length=30, default="")
    email_client = models.CharField(max_length=100, default="")
    name_product = models.CharField(max_length=200, default="")
    mark_product = models.CharField(max_length=200, default="")
    serial_number_product = models.CharField(max_length=200, default="")    
    tracking_number = models.CharField(max_length=100, blank=True)       
    guarantee = models.CharField(max_length=100, default="Sur garantie")
    out_of_order_reason = models.TextField()
    client_bill = models.FileField(blank=True)

    registred_by = models.ForeignKey(get_user_model(), default = 1)

    def __unicode__(self):
        return str(self.id) 

    def get_absolute_url(self):
        return reverse('visualImpactSAV:detailSAVFile', kwargs = {'pk' : self.pk})

class Event(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file)
    title = models.CharField(max_length=100)
    action = models.TextField()
    date = models.DateTimeField(default=timezone.now)

class Designation(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file)
    designation = models.CharField(max_length=100, default="")
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
