# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .views_template_parameters_sav_files import ParameterCreateView, ParameterUpdateView, ParameterDeleteView

# models part
from visualImpactSAV.models import Event
# forms part
from visualImpactSAV.forms import EventForm

class EventCreateView(ParameterCreateView):
    model = Event
    form_class = EventForm 
    template_name = 'djangoApp/Event/createEvent.html'

class EventUpdateView(ParameterUpdateView):
    model = Event
    form_class = EventForm
    template_name = 'djangoApp/Event/updateEvent.html'

class EventDeleteView(ParameterDeleteView):
    model = Event
    template_name = 'djangoApp/Event/confirmDeleteEvent.html'
    
    def dispatch(self, *args, **kwargs):
        self.pk = kwargs['pk']
        self.url_to_redirect = 'visualImpactSAV:updateSAVFile'
        return super(EventDeleteView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventDeleteView, self).get_context_data(**kwargs)
        print self.pk
        context['id_to_delete'] = self.pk
        context['name_class'] = self.object.__class__.__name__
        context['name_object'] = self.object.title

        return context
    
