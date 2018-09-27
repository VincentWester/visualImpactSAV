# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from decimal import Decimal

from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from visualImpactSAV.models import SAV_file, SAV_file_status, Event, Designation, Furnisher
from visualImpactSAV.forms import SAV_fileForm

import constants
from django.contrib.auth.mixins import LoginRequiredMixin


class SAVFileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'djangoApp/SAVFile/detailSAVFile.html'
    queryset = SAV_file.objects.all()

    def get_object(self):
        object = super(SAVFileDetailView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        context = super(SAVFileDetailView, self).get_context_data(**kwargs)
        context['pkSAVFile'] = self.object.id
        context['events'] = Event.objects.all().filter(refered_SAV_file=self.object).order_by('date')
        context['furnishers'] = Furnisher.objects.all().order_by('mark')

        designations = self.object.designations.all().order_by('id')
        context['designations'] = designations

        total = Decimal(0.0)
        for designation in designations:
            total += Decimal(designation.quantity) * Decimal(designation.price)

        context['totalHT'] = round(total, 2)
        context['totalTC'] = round(total * constants.TAX_RATE, 2)

        return context


class SAVFileCreateView(LoginRequiredMixin, CreateView):
    model = SAV_file
    form_class = SAV_fileForm
    template_name = 'djangoApp/SAVFile/createSAVFile.html'

    def get_context_data(self, **kwargs):
        context = super(SAVFileCreateView, self).get_context_data(**kwargs)
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['furnishers'] = Furnisher.objects.all().order_by('mark')

        return context

    def form_invalid(self, form):
        return render(
            self.request,
            'djangoApp/SAVFile/createSAVFile.html',
            {'form': form, 'sav_file_status': SAV_file_status.objects.all()}
        )

    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        form.instance.registred_by = self.request.user
        return super(SAVFileCreateView, self).form_valid(form)


class SAVFileUpdateView(LoginRequiredMixin, UpdateView):
    model = SAV_file
    form_class = SAV_fileForm
    template_name = 'djangoApp/SAVFile/updateSAVFile.html'

    def get_context_data(self, **kwargs):
        context = super(SAVFileUpdateView, self).get_context_data(**kwargs)
        context['current_sav_file'] = self.object
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['events'] = Event.objects.all().filter(refered_SAV_file=self.object).order_by('date')
        context['furnishers'] = Furnisher.objects.all()

        designations = self.object.designations.all()
        context['designations'] = designations

        total = Decimal(0.0)
        for designation in designations:
            total += Decimal(designation.quantity) * Decimal(designation.price)

        context['totalHT'] = round(total, 2)
        context['totalTC'] = round(total * constants.TAX_RATE, 2)

        return context

    def form_invalid(self, form):
        return render(self.request, 'djangoApp/SAVFile/updateSAVFile.html', {'form': form})

    def form_valid(self, form):
        return super(SAVFileUpdateView, self).form_valid(form)


class SAVFileListView(LoginRequiredMixin, ListView):
    template_name = 'djangoApp/SAVFile/searchSAVFile.html'
    context_object_name = 'results'
    paginate_by = constants.DEFAULT_ASS_FILE_LIST_VIEW_PAGINATION_BY

    def get_context_data(self, **kwargs):
        context = super(SAVFileListView, self).get_context_data(**kwargs)
        context['sav_file_status'] = SAV_file_status.objects.all()
        results = self.get_queryset()

        libelle_stats = {}
        for sav_file_status in SAV_file_status.objects.all():
            libelle_stats[sav_file_status.libelle] = results.filter(sav_file_status__libelle=sav_file_status.libelle).count()

        context['libelle_stats'] = libelle_stats
        context['nb_sav_file_status'] = results.count()

        return context

    """
    Display a SAV_file List page filtered by the search query.
    """
    def get_queryset(self):
        file_reference = self.request.GET.get('file_reference')
        rma_number = self.request.GET.get('status')
        client_name = self.request.GET.get('client_name')
        client_society = self.request.GET.get('client_society')
        product_name = self.request.GET.get('product_name')
        product_mark = self.request.GET.get('product_mark')
        product_serial_number = self.request.GET.get('product_serial_number')
        rma_number = self.request.GET.get('rma_number')
        sav_file_status = self.request.GET.get('sav_file_status')
        results = SAV_file.objects.all()

        kwargs = {}

        if file_reference:
            kwargs['id'] = file_reference

        if client_name:
            kwargs['name_client__icontains'] = client_name

        if client_society:
            kwargs['society_client__icontains'] = client_society

        if product_name:
            kwargs['name_product__icontains'] = product_name

        if product_mark:
            kwargs['mark_product__icontains'] = product_mark

        if product_serial_number:
            kwargs['serial_number_product__icontains'] = product_serial_number

        if rma_number:
            kwargs['rma_number__icontains'] = rma_number

        if sav_file_status:
            kwargs['sav_file_status'] = sav_file_status

        if not kwargs:
            return results

        return results.filter(**kwargs)
