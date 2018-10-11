# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField, ModelChoiceField, ChoiceField
from .models import SAV_file, SAV_file_status, Event, Designation, Furnisher, Waranty
from django.contrib.auth.forms import UserCreationForm

from django.utils.translation import ugettext_lazy as _

import constants


class SignUpForm(UserCreationForm):
    email = EmailField(max_length=254, help_text=_('Required. Write a valide email.'))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = _('Required. Write a username.')
        self.fields['password1'].help_text = _('Required. Choose a password.')
        self.fields['password2'].help_text = _('Required. Password checking : copy your password.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        error_messages = {
            'username': {
                'required': _("The username attribute should be filled"),
            },
            'email': {
                'required': _("The email attribute should be filled"),
            },
            'password1': {
                'required': _("The password attribute should be filled"),
            },
            'password2': {
                'required': _("The password haven't been well copied"),
            },
        }

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class SAV_fileForm(ModelForm):
    furnisher = ModelChoiceField(queryset=Furnisher.objects.all(), empty_label="---", required=False)
    status = ChoiceField(choices=constants.SAV_FILE_STATUS_CHOICES, required=False)

    class Meta:
        model = SAV_file
        fields = [
            field.name for field in model._meta.fields
            if not (field.name == "creation_date" or field.name == "sav_file_status" or field.name == "registred_by")
        ]

        error_messages = {
            'name_customer': {
                'required': _("The customer name attribute should be filled"),
            },
            'street_customer': {
                'required': _("The customer street attribute should be filled"),
            },
            'city_customer': {
                'required': _("The customer city attribute should be filled"),
            },
            'zipcode_customer': {
                'required': _("The customer zipcode attribute should be filled"),
            },
            'phone_customer': {
                'required': _("The customer phone attribute should be filled"),
            },
            'email_customer': {
                'required': _("The customer email attribute should be filled"),
            },
            'name_product': {
                'required': _("The product's model attribute should be filled"),
            },
            'brand_product': {
                'required': _("The product's brand attribute should be filled"),
            },
            'serial_number_product': {
                'required': _("The product's serial number attribute should be filled").encode('utf-8'),
            },
            'rma_number': {
                'required': _("The RMA number attribute should be filled"),
            },
            'guarantee': {
                'required': _("The waranty's status attribute should be filled"),
            },
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            field.name for field in model._meta.fields
            if not (field.name == "date" or field.name == "refered_SAV_file")
        ]


class DesignationForm(ModelForm):
    class Meta:
        model = Designation
        fields = [field.name for field in model._meta.fields if not (field.name == "refered_SAV_file")]


class WarantyForm(ModelForm):
    class Meta:
        model = Waranty
        fields = [field.name for field in model._meta.fields]


class FurnisherForm(ModelForm):
    class Meta:
        model = Furnisher
        fields = [field.name for field in model._meta.fields]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = []
