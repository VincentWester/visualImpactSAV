# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import PROTECT


DEFAULT_SAV_FILE_STATUS_ID = 1


class SAV_file_status(models.Model):
    libelle = models.CharField(max_length=50)
    class_css = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return str(self.id) + "-" + self.libelle

    class Meta:
        verbose_name = _("after sale file status")
        verbose_name_plural = _("after sale file status")


class Guarantee(models.Model):
    mark = models.CharField(_("Brand"), max_length=200, default="")
    complements = models.CharField(_("Complements"), max_length=200, default="", blank=True)
    guarantee_time = models.CharField(_("Waranty_time"), max_length=20, default="")
    procedure = models.TextField(_("Procedure"))

    class Meta:
        verbose_name = _("waranty")
        verbose_name_plural = _("waranties")
        ordering = ['mark']


class Furnisher(models.Model):
    mark = models.CharField(_("Brand"), max_length=200, default="")
    street = models.CharField(_("Street"), max_length=300, default="")
    complements = models.CharField(_("Complements"), max_length=300, default="", blank=True)
    zipcode = models.CharField(_("Zipcode"), max_length=30, default="")
    city = models.CharField(_("City"), max_length=100, default="")
    phone = models.CharField(_("Phone"), max_length=200, default="")
    commentary = models.TextField(_("Commentary"), blank=True)

    def __str__(self):
        return self.mark.encode('utf-8')

    class Meta:
        verbose_name = _("furnisher")
        verbose_name_plural = _("furnishers")
        ordering = ['mark']


class SAV_file(models.Model):
    creation_date = models.DateTimeField(_("Creation date"), default=timezone.now)
    sav_file_status = models.ForeignKey(SAV_file_status, default=DEFAULT_SAV_FILE_STATUS_ID, verbose_name=_("Status"))
    society_client = models.CharField(_("Society"), max_length=300, default="", blank=True)
    name_client = models.CharField(_("Customer name"), max_length=300, default="")
    street_client = models.CharField(_("Customer street"), max_length=300, default="")
    complements_client = models.CharField(_("Customer address complements"), max_length=300, default="", blank=True)
    zipcode_client = models.CharField(_("Customer zipcode"), max_length=30, default="")
    city_client = models.CharField(_("Customer city"), max_length=100, default="")
    phone_client = models.CharField(_("Customer phone"), max_length=30, default="")
    email_client = models.CharField(_("Customer email"), max_length=100, default="")
    name_product = models.CharField(_("Product model"), max_length=200, default="")
    mark_product = models.CharField(_("Product brand"), max_length=200, default="")
    serial_number_product = models.CharField(_("Product serial number"), max_length=200, default="")
    rma_number = models.CharField(_("Product RMA number"), max_length=100, default="", blank=True)
    guarantee = models.CharField(_("Waranty"), max_length=100, default="Sous garantie")
    out_of_order_reason = models.TextField(_("Out of order reason"))
    client_bill = models.FileField(_("Client bill"), blank=True)
    furnisher = models.ForeignKey(Furnisher, null=True, on_delete=PROTECT, verbose_name=_("Furnisher"))

    registred_by = models.ForeignKey(get_user_model(), default=1, verbose_name=_("User"))

    def __unicode__(self):
        return str(self.id).encode('utf-8')

    def get_absolute_url(self):
        return reverse('visualImpactSAV:detailSAVFile', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("After sale file")
        verbose_name_plural = _("After sale files")
        ordering = ['creation_date']


class Event(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file, verbose_name=_("After sale file"))
    title = models.CharField(_("Title"), max_length=100)
    action = models.TextField(_("Action"))
    date = models.DateTimeField(_("Date"), default=timezone.now)

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ['refered_SAV_file']


class Designation(models.Model):
    refered_SAV_file = models.ForeignKey(SAV_file, verbose_name=_("After sale file"), related_name="designations")
    designation = models.CharField(_("Designation"), max_length=100, default="")
    quantity = models.IntegerField(_("Quantity"), default=1)
    price = models.DecimalField(_("Price"), default=0.0, max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = _("designation")
        verbose_name_plural = _("designations")
        ordering = ['quantity']
