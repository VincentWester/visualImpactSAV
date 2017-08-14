# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render, render_to_response

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import SAV_file, SAV_file_status, Reparation_status, Event
from .forms import SAV_fileForm, SAV_fileUpdateForm, EventForm

import operator

def home(request):
    return render(request, 'djangoApp/home/home.html')

class SAVFileDetailView(DetailView):
    queryset = SAV_file.objects.all()
    template_name = 'djangoApp/detailSAVFile/detailSAVFile.html'

    def get_object(self):
        # Call the superclass
        object = super(SAVFileDetailView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        # qui dit overriding, dit appel de la méthode parent...
        context = super(SAVFileDetailView, self).get_context_data(**kwargs)
        # et on rajoute la date du jour dans le context
        context['events'] = Event.objects.all().filter(refered_SAV_file = self.object).order_by('date')
        print context['events']

        # le context retourné sera automatiquement injecté dans le template
        # dans la méthode render(), que vous ne voyez pas...
        return context

class SAVFileCreateView(CreateView):
    model = SAV_file
    form_class = SAV_fileForm
    template_name = 'djangoApp/createSAVFile/createSAVFile.html'

    def get_context_data(self, **kwargs):
        # qui dit overriding, dit appel de la méthode parent...
        context = super(SAVFileCreateView, self).get_context_data(**kwargs)
        # et on rajoute la date du jour dans le context
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['reparation_status'] = Reparation_status.objects.all()

        # le context retourné sera automatiquement injecté dans le template
        # dans la méthode render(), que vous ne voyez pas...
        return context 

    def form_invalid(self, form):
        print form
        return HttpResponse("touché coulé")

    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        form.instance.file_reference = 'VisualImpact-SAV-' + form.instance.file_reference
        return super(SAVFileCreateView, self).form_valid(form)

class SAVFileUpdateView(UpdateView):
    model = SAV_file
    form_class = SAV_fileUpdateForm
    template_name = 'djangoApp/updateSAVFile/updateSAVFile.html'

    def get_context_data(self, **kwargs):
        # qui dit overriding, dit appel de la méthode parent...
        context = super(SAVFileUpdateView, self).get_context_data(**kwargs)
        # et on rajoute la date du jour dans le context
        context['current_sav_file'] = self.object
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['reparation_status'] = Reparation_status.objects.all()
        context['events'] = Event.objects.all().filter(refered_SAV_file = self.object).order_by('date')
        print context['events']

        # le context retourné sera automatiquement injecté dans le template
        # dans la méthode render(), que vous ne voyez pas...
        return context 

    def form_invalid(self, form):
        print form
        return HttpResponse("touché coulé")
        
    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        return super(SAVFileUpdateView, self).form_valid(form)


DEFAULT_PAGINATION_BY = 10

class SAVFileListView(ListView):
    template_name = 'djangoApp/searchSAVFile/searchSAVFile.html'
    context_object_name = 'results'
    queryset = SAV_file.objects.all()
    paginate_by = DEFAULT_PAGINATION_BY

    def get_context_data(self, **kwargs):
        # qui dit overriding, dit appel de la méthode parent...
        context = super(SAVFileListView, self).get_context_data(**kwargs)
        # et on rajoute la date du jour dans le context
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['reparation_status'] = Reparation_status.objects.all()

        results = self.get_queryset()

        libelle_stats = {}
        for sav_file_status in SAV_file_status.objects.all():
            libelle_stats[sav_file_status.libelle] = results.filter(sav_file_status__libelle = sav_file_status.libelle).count()

        context['libelle_stats'] = libelle_stats
        context['nb_sav_file_status'] = results.count()
        # le context retourné sera automatiquement injecté dans le template
        # dans la méthode render(), que vous ne voyez pas...
        return context

    """
    Display a SAV_file List page filtered by the search query.
    """
    def get_queryset(self):
        file_reference = self.request.GET.get('file_reference')
        tracking_number = self.request.GET.get('status')
        client_name = self.request.GET.get('client_name')
        product_name = self.request.GET.get('product_name')
        product_mark = self.request.GET.get('product_mark')
        product_serial_number = self.request.GET.get('product_serial_number')
        tracking_number = self.request.GET.get('tracking_number')
        sav_file_status = self.request.GET.get('sav_file_status')
        reparation_status = self.request.GET.get('reparation_status')
        results = SAV_file.objects.all()
        
        if file_reference:
            results = results.filter(file_reference__icontains = file_reference)

        if client_name:
            results = results.filter(name_client__icontains = client_name) 
        
        if product_name:
            results = results.filter(name_product__icontains = product_name)

        if product_mark:
            results = results.filter(mark_product__icontains = product_mark) 

        if product_serial_number:
            results = results.filter(serial_number_product__icontains = product_serial_number)

        if tracking_number:
            results = results.filter(tracking_number__icontains = tracking_number)

        if sav_file_status:
            results = results.filter(sav_file_status = sav_file_status)

        if reparation_status:
            results = results.filter(reparation_status = reparation_status)

        return results.order_by('file_reference')

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm 
    template_name = 'djangoApp/detailSAVFile/createEvent.html'

    def dispatch(self, *args, **kwargs):
        self.pkSAVFile = kwargs['pkSAVFile']

        # le context retourné sera automatiquement injecté dans le template
        # dans la méthode render(), que vous ne voyez pas...
        return super(EventCreateView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        # qui dit overriding, dit appel de la méthode parent...
        context = super(EventCreateView, self).get_context_data(**kwargs)

        context['pkSAVFile'] = self.pkSAVFile
        return context 

    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        sav_file = SAV_file.objects.get(file_reference = self.kwargs['pkSAVFile'])
        form.instance.refered_SAV_file = sav_file
        self.object = form.save()

        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)
