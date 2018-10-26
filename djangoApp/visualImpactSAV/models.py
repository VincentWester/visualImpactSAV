# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import PROTECT

import constants


class Waranty(models.Model):
    brand = models.CharField(_("Brand"), max_length=200, default="")
    complements = models.CharField(_("Complements"), max_length=200, default="", blank=True)
    waranty_time = models.CharField(_("Waranty time"), max_length=20, default="")
    procedure = models.TextField(_("Procedure"))

    def __unicode__(self):
        return self.brand + " " + self.complements

    class Meta:
        verbose_name = _("waranty")
        verbose_name_plural = _("waranties")
        ordering = ['brand']


class Furnisher(models.Model):
    brand = models.CharField(_("Brand"), max_length=200, default="")
    street = models.CharField(_("Street"), max_length=300, default="")
    complements = models.CharField(_("Complements"), max_length=300, default="", blank=True)
    zipcode = models.CharField(_("Zipcode"), max_length=30, default="")
    city = models.CharField(_("City"), max_length=100, default="")
    phone = models.CharField(_("Phone"), max_length=200, default="")
    commentary = models.TextField(_("Commentary"), blank=True)

    def __unicode__(self):
        return self.brand

    class Meta:
        verbose_name = _("furnisher")
        verbose_name_plural = _("furnishers")
        ordering = ['brand']


class SAV_file(models.Model):
    creation_date = models.DateTimeField(_("Creation date"), default=timezone.now)
    status = models.CharField(
        _("Status"), 
        max_length=20,
        choices=constants.SAV_FILE_STATUS_CHOICES,
        default=constants.SAV_FILE_STATUS_TYPE_OPENED,
    )
    society_customer = models.CharField(_("Society"), max_length=300, default="", blank=True)
    name_customer = models.CharField(_("Customer name"), max_length=300, default="")
    street_customer = models.CharField(_("Customer street"), max_length=300, default="")
    complements_customer = models.CharField(_("Customer address complements"), max_length=300, default="", blank=True)
    zipcode_customer = models.CharField(_("Customer zipcode"), max_length=30, default="")
    city_customer = models.CharField(_("Customer city"), max_length=100, default="")
    phone_customer = models.CharField(_("Customer phone"), max_length=30, default="")
    email_customer = models.CharField(_("Customer email"), max_length=100, default="")
    name_product = models.CharField(_("Product model"), max_length=200, default="")
    brand_product = models.CharField(_("Product brand"), max_length=200, default="")
    serial_number_product = models.CharField(_("Product serial number"), max_length=200, default="")
    rma_number = models.CharField(_("Product RMA number"), max_length=100, default="", blank=True)
    waranty = models.CharField(
        _("Waranty"), 
        max_length=100,         
        choices=constants.SAV_FILE_WARANTY_TYPE_CHOICES,
        default=constants.SAV_FILE_WARANTY_TYPE_INCLUDED,
    )
    out_of_order_reason = models.TextField(_("Out of order reason"))
    bill_customer = models.FileField(_("Customer bill"), blank=True)
    furnisher = models.ForeignKey(Furnisher, null=True, on_delete=PROTECT, verbose_name=_("Furnisher"))
    registred_by = models.ForeignKey(get_user_model(), default=constants.DEFAULT_USERS_ID, verbose_name=_("User"))

    def __unicode__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('visualImpactSAV:detailSAVFile', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("After sale file")
        verbose_name_plural = _("After sale files")
        ordering = ['creation_date']


class Event(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file, verbose_name=_("After sale file"), related_name="events")
    title = models.CharField(_("Title"), max_length=100)
    action = models.TextField(_("Action"))
    date = models.DateTimeField(_("Date"), default=timezone.now)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ['date']


class Designation(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file, verbose_name=_("After sale file"), related_name="designations")
    designation = models.CharField(_("Designation"), max_length=100, default="")
    quantity = models.IntegerField(_("Quantity"), default=1)
    price = models.DecimalField(_("Price"), default=0.0, max_digits=18, decimal_places=2)

    def __unicode__(self):
        return self.designation

    class Meta:
        verbose_name = _("designation")
        verbose_name_plural = _("designations")
        ordering = ['id']