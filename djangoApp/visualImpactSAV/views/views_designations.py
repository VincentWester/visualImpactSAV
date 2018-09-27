# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.views.generic import ListView

import constants
from .views_template_parameters_sav_files import ParameterCreateView, ParameterUpdateView, ParameterDeleteView
from visualImpactSAV.models import Designation
from visualImpactSAV.forms import DesignationForm


class DesignationCreateView(ParameterCreateView):
    model = Designation
    form_class = DesignationForm
    template_name = 'djangoApp/Designation/createDesignation.html'


class DesignationUpdateView(ParameterUpdateView):
    model = Designation
    form_class = DesignationForm
    template_name = 'djangoApp/Designation/updateDesignation.html'


class DesignationDeleteView(ParameterDeleteView):
    model = Designation
    template_name = 'djangoApp/Designation/confirmDeleteDesignation.html'

    def dispatch(self, *args, **kwargs):
        self.pk = kwargs['pk']
        self.url_to_redirect = 'visualImpactSAV:updateSAVFile'
        return super(DesignationDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DesignationDeleteView, self).get_context_data(**kwargs)
        context['id_to_delete'] = self.pk
        context['name_class'] = self.object.__class__.__name__
        context['name_object'] = self.object.designation

        return context
