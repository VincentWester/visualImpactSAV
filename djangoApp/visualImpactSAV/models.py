# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from datetime import datetime

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import PROTECT


DEFAULT_SAV_FILE_STATUS_ID = 1

class SAV_file_status(models.Model):
    libelle = models.CharField(max_length = 50)
    class_css = models.CharField(max_length = 50, blank = True)

    def __unicode__(self):
        return str(self.id) + "-" + self.libelle 

class Guarantee(models.Model):
    mark = models.CharField(max_length = 200, default = "")
    complements = models.CharField(max_length = 200, default = "", blank = True)
    guarantee_time = models.CharField(max_length = 20, default = "")
    procedure = models.TextField()    

class Furnisher(models.Model):
    mark = models.CharField(max_length = 200, default = "")
    street = models.CharField(max_length = 300, default = "")
    complements = models.CharField(max_length = 300, default = "", blank = True)
    zipcode = models.CharField(max_length = 30, default = "")
    city = models.CharField(max_length = 100, default = "")
    phone = models.CharField(max_length = 200, default = "")
    commentary = models.TextField(blank = True)   

    def __str__(self):
        return self.mark.encode('utf-8')

class SAV_file(models.Model):
    creation_date = models.DateTimeField(default = timezone.now)
    sav_file_status = models.ForeignKey(SAV_file_status, default = DEFAULT_SAV_FILE_STATUS_ID)
    society_client = models.CharField(max_length = 300, default = "", blank = True)
    name_client = models.CharField(max_length = 300, default = "")
    street_client = models.CharField(max_length = 300, default = "")
    complements_client = models.CharField(max_length = 300, default = "", blank = True)
    zipcode_client = models.CharField(max_length = 30, default = "")
    city_client = models.CharField(max_length = 100, default = "")
    phone_client = models.CharField(max_length = 30, default = "")
    email_client = models.CharField(max_length = 100, default = "")
    name_product = models.CharField(max_length = 200, default = "")
    mark_product = models.CharField(max_length = 200, default = "")
    serial_number_product = models.CharField(max_length = 200, default = "")    
    rma_number = models.CharField(max_length = 100, default = "")       
    guarantee = models.CharField(max_length = 100, default = "Sous garantie")
    out_of_order_reason = models.TextField()
    client_bill = models.FileField(blank = True)
    furnisher = models.ForeignKey(Furnisher, null = True, on_delete = PROTECT)

    registred_by = models.ForeignKey(get_user_model(), default = 1)

    def __unicode__(self):
        return str(self.id) 

    def get_absolute_url(self):
        return reverse('visualImpactSAV:detailSAVFile', kwargs = {'pk' : self.pk})

class Event(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file)
    title = models.CharField(max_length = 100)
    action = models.TextField()
    date = models.DateTimeField(default = timezone.now)

class Designation(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file)
    designation = models.CharField(max_length = 100, default = "")
    quantity = models.IntegerField(default = 1)
    price = models.DecimalField(default = 0.0, max_digits = 18, decimal_places = 2)
