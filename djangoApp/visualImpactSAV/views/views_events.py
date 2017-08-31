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
        self.url = 'visualImpactSAV:updateSAVFile'
        return super(EventDeleteView, self).dispatch( *args, **kwargs)
    
