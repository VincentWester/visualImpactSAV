# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.conf import settings
from PIL import Image
from io import BytesIO
import urllib, cStringIO

# models part
from visualImpactSAV.models import Event, SAV_file
# forms part
from visualImpactSAV.forms import EventForm

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm 
    template_name = 'djangoApp/detailSAVFile/createEvent.html'

    def dispatch(self, *args, **kwargs):
        self.pkSAVFile = kwargs['pkSAVFile']

        return super(EventCreateView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)

        context['pkSAVFile'] = self.pkSAVFile
        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))

    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        sav_file = SAV_file.objects.get(file_reference = self.kwargs['pkSAVFile'])
        form.instance.refered_SAV_file = sav_file
        self.object = form.save()

        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'djangoApp/detailSAVFile/updateEvent.html'

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context['current_event'] = self.object

        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))
        
    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        self.object = form.save()

        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'djangoApp/detailSAVFile/confirmDeleteEvent.html'

    def get_success_url(self, *args, **kwargs): 
        return reverse_lazy('visualImpactSAV:detailSAVFile',  kwargs={ 'pk' : self.object.refered_SAV_file.file_reference }) 