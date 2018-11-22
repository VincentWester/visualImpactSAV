# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from decimal import Decimal

from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from visualImpactSAV.models import SAV_file, Furnisher
from visualImpactSAV.forms import SAV_fileForm

import constants


class SAVFileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'djangoApp/SAVFile/detailSAVFile.html'
    queryset = SAV_file.objects.all()

    def get_object(self):
        object = super(SAVFileDetailView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        context = super(SAVFileDetailView, self).get_context_data(**kwargs)
        context['pkSAVFile'] = self.object.id
        context['events'] = self.object.events.all()

        designations = self.object.designations.all()
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
        context['sav_file_status'] = constants.SAV_FILE_STATUS_CHOICES
        context['waranties'] = constants.SAV_FILE_WARANTY_TYPE_CHOICES
        context['furnishers'] = Furnisher.objects.all()

        return context

    def form_invalid(self, form):
        return render(
            self.request,
            'djangoApp/SAVFile/createSAVFile.html',
            {'form': form, 'sav_file_status': constants.SAV_FILE_STATUS_CHOICES}
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
        context['sav_file_status'] = constants.SAV_FILE_STATUS_CHOICES
        context['waranties'] = constants.SAV_FILE_WARANTY_TYPE_CHOICES
        context['events'] = self.object.events.all()
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
        context['sav_file_status'] = constants.SAV_FILE_STATUS_CHOICES
        results = self.get_queryset()

        libelle_stats = {}
        for status in constants.SAV_FILE_STATUS_CHOICES:
            libelle_stats[status[0]] = results.filter(status=status[0]).count()

        context['libelle_stats'] = libelle_stats
        context['nb_sav_file_status'] = results.count()

        if re.match('.*/$', self.request.get_full_path()):
            context['redirection_adresse'] = self.request.get_full_path() + '?'
        else:
            context['redirection_adresse'] = self.request.get_full_path() + '&'

        return context

    """
    Display a SAV_file List page filtered by the search query.
    """
    def get_queryset(self):
        file_reference = self.request.GET.get('file_reference')
        rma_number = self.request.GET.get('status')
        name_customer = self.request.GET.get('name_customer')
        society_customer = self.request.GET.get('society_customer')
        name_product = self.request.GET.get('name_product')
        brand_product = self.request.GET.get('brand_product')
        serial_number_product = self.request.GET.get('serial_number_product')
        rma_number = self.request.GET.get('rma_number')
        sav_file_status = self.request.GET.get('sav_file_status')
        begin_date = self.request.GET.get('begin_date')
        end_date = self.request.GET.get('end_date')
        results = SAV_file.objects.all()

        kwargs = {}

        if file_reference:
            kwargs['id'] = file_reference

        if name_customer:
            kwargs['name_customer__icontains'] = name_customer

        if society_customer:
            kwargs['society_customer__icontains'] = society_customer

        if name_product:
            kwargs['name_product__icontains'] = name_product

        if brand_product:
            kwargs['brand_product__icontains'] = brand_product

        if serial_number_product:
            kwargs['serial_number_product__icontains'] = serial_number_product

        if rma_number:
            kwargs['rma_number__icontains'] = rma_number

        if sav_file_status:
            kwargs['status'] = sav_file_status
        
        if begin_date:
            kwargs['creation_date__gte'] = begin_date
        
        if end_date:
            kwargs['creation_date__lte'] = end_date

        if not kwargs:
            return results.exclude(status='C')

        return results.filter(**kwargs)
