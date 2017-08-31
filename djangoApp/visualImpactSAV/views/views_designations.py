# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        self.url = 'visualImpactSAV:detailSAVFile'
        return super(DesignationDeleteView, self).dispatch( *args, **kwargs)

