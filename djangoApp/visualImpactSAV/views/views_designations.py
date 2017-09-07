# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.views.generic import ListView

from .views_template_parameters_sav_files import ParameterCreateView, ParameterUpdateView, ParameterDeleteView

# models part
from visualImpactSAV.models import Designation
# forms part
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
        self.url = 'visualImpactSAV:listDesignation'
        return super(DesignationDeleteView, self).dispatch( *args, **kwargs)

TAX_RATE = Decimal(1.2)

class DesignationListView(ListView):
    model = Designation    
    template_name = 'djangoApp/Designation/listDesignation.html'

    def dispatch(self, *args, **kwargs):
        self.pkSAVFile = kwargs['pkSAVFile']
        return super(DesignationListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DesignationListView, self).get_context_data(**kwargs)
        context['pkSAVFile'] = self.pkSAVFile

        designations = self.get_queryset()

        context['designations'] = designations

        total = Decimal(0.0)
        for designation in designations:
            total += Decimal(designation.quantity) * Decimal(designation.price)

        context['totalHT'] = round(total, 2)
        context['totalTC'] = round(total * TAX_RATE, 2)
        return context

    def get_queryset(self):
        return Designation.objects.filter(refered_SAV_file__file_reference = self.pkSAVFile)

