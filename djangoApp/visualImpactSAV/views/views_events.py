# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from visualImpactSAV.models import Event
from visualImpactSAV.forms import EventForm
from visualImpactSAV.views.views_template_parameters_sav_files import ParameterCreateView, ParameterUpdateView, ParameterDeleteView


class EventCreateView(ParameterCreateView):
    model = Event
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:createEvent', args=[], kwargs={'pkSAVFile': self.pkSAVFile})
        context['id_modal'] = 'createEvent'
        context['action_to_made'] = _('Create')
        context['value_button'] = _('Create this %s') % _('event')

        return context


class EventUpdateView(ParameterUpdateView):
    model = Event
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:updateEvent', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'updateEvent'
        context['action_to_made'] = _('Update')
        context['value_button'] = _('Update this %s') % _('event')

        return context


class EventDeleteView(ParameterDeleteView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventDeleteView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:deleteEvent', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'deleteEvent'
        context['action_to_made'] = _('Delete')
        context['value_button'] = _('Delete this %s') % _('event')

        return context
