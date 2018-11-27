# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from visualImpactSAV.models.business_models import Designation
from visualImpactSAV.forms import DesignationForm
from .views_template_parameters_sav_files import ParameterCreateView, ParameterUpdateView, ParameterDeleteView


class DesignationCreateView(ParameterCreateView):
    model = Designation
    form_class = DesignationForm

    def get_context_data(self, **kwargs):
        context = super(DesignationCreateView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:createDesignation', args=[], kwargs={'pkSAVFile': self.pkSAVFile})
        context['id_modal'] = 'createDesignation'
        context['action_to_made'] = _('Create')
        context['value_button'] = _('Create this %s') % _('designation')

        return context


class DesignationUpdateView(ParameterUpdateView):
    model = Designation
    form_class = DesignationForm

    def get_context_data(self, **kwargs):
        context = super(DesignationUpdateView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:updateDesignation', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'updateDesignation'
        context['action_to_made'] = _('Update')
        context['value_button'] = _('Update this %s') % _('designation')

        return context


class DesignationDeleteView(ParameterDeleteView):
    model = Designation

    def get_context_data(self, **kwargs):
        context = super(DesignationDeleteView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:deleteDesignation', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'deleteDesignation'
        context['action_to_made'] = _('Delete')
        context['value_button'] = _('Delete this %s') % _('designation')

        return context
