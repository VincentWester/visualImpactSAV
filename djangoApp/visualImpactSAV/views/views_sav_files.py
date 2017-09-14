# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# models part
from visualImpactSAV.models import SAV_file, SAV_file_status, Reparation_status, Event, Designation
# forms part
from visualImpactSAV.forms import SAV_fileForm

class SAVFileDetailView(DetailView):
    queryset = SAV_file.objects.all()
    template_name = 'djangoApp/SAVFile/detailSAVFile.html'

    def get_object(self):
        object = super(SAVFileDetailView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        context = super(SAVFileDetailView, self).get_context_data(**kwargs)
        context['pkSAVFile'] = self.object.id
        context['events'] = Event.objects.all().filter(refered_SAV_file = self.object).order_by('date')

        return context

class SAVFileCreateView(CreateView):
    model = SAV_file
    form_class = SAV_fileForm
    template_name = 'djangoApp/SAVFile/createSAVFile.html'

    def get_context_data(self, **kwargs):
        context = super(SAVFileCreateView, self).get_context_data(**kwargs)
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['reparation_status'] = Reparation_status.objects.all()

        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))

    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        return super(SAVFileCreateView, self).form_valid(form)

class SAVFileUpdateView(UpdateView):
    model = SAV_file
    form_class = SAV_fileForm
    template_name = 'djangoApp/SAVFile/updateSAVFile.html'

    def get_context_data(self, **kwargs):
        context = super(SAVFileUpdateView, self).get_context_data(**kwargs)
        context['current_sav_file'] = self.object
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['reparation_status'] = Reparation_status.objects.all()
        context['events'] = Event.objects.all().filter(refered_SAV_file = self.object).order_by('date')

        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))
        
    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        return super(SAVFileUpdateView, self).form_valid(form)

DEFAULT_PAGINATION_BY = 10

class SAVFileListView(ListView):
    template_name = 'djangoApp/SAVFile/searchSAVFile.html'
    context_object_name = 'results'
    queryset = SAV_file.objects.all()
    paginate_by = DEFAULT_PAGINATION_BY

    def get_context_data(self, **kwargs):
        context = super(SAVFileListView, self).get_context_data(**kwargs)
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['reparation_status'] = Reparation_status.objects.all()

        results = self.get_queryset()

        libelle_stats = {}
        for sav_file_status in SAV_file_status.objects.all():
            libelle_stats[sav_file_status.libelle] = results.filter(sav_file_status__libelle = sav_file_status.libelle).count()

        context['libelle_stats'] = libelle_stats
        context['nb_sav_file_status'] = results.count()
        return context

    """
    Display a SAV_file List page filtered by the search query.
    """
    def get_queryset(self):
        file_reference = self.request.GET.get('file_reference')
        tracking_number = self.request.GET.get('status')
        client_name = self.request.GET.get('client_name')
        client_society = self.request.GET.get('client_society')
        product_name = self.request.GET.get('product_name')
        product_mark = self.request.GET.get('product_mark')
        product_serial_number = self.request.GET.get('product_serial_number')
        tracking_number = self.request.GET.get('tracking_number')
        sav_file_status = self.request.GET.get('sav_file_status')
        reparation_status = self.request.GET.get('reparation_status')
        results = SAV_file.objects.all()
        
        if file_reference:
            results = results.filter(id__icontains = file_reference)

        if client_name:
            results = results.filter(name_client__icontains = client_name) 

        if client_society:
            results = results.filter(society_client__icontains = client_society) 
        
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

        return results.order_by('id')