# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, render_to_response

from .models import SAV_file, Client, Product, SAV_file_status
from .forms import SAV_fileForm

import operator

def saveSAVFile(request):
    # create a form instance and populate it with data from the request:

    form = SAV_fileForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
    # process the data in form.cleaned_data as required    
        sav_file = SAV_file()
        sav_file.file_reference = 'VisualImpact-SAV-' + form.cleaned_data['file_reference']
        sav_file.status = form.cleaned_data['status']
        sav_file.client = form.cleaned_data['client']
        sav_file.product_referenced = form.cleaned_data['product_referenced']
        sav_file.out_of_order_reason = form.cleaned_data['out_of_order_reason']
        sav_file.file_import_export_note = form.cleaned_data['file_import_export_note']
        sav_file.file_import_export_reparation_client_side = form.cleaned_data['file_import_export_reparation_client_side']
        sav_file.file_import_export_reparation_furnisher_side = form.cleaned_data['file_import_export_reparation_furnisher_side']
        sav_file.reparation_validated = form.cleaned_data['reparation_validated']
        sav_file.tracking_number = form.cleaned_data['tracking_number']
        sav_file.save()

        return render(request, 'djangoApp/view.html', {'sav_file': sav_file})

    else:
        return HttpResponse('Le formulaire est mal rempli.')

def addSAVFile(request):

    sav_file_form = SAV_fileForm()
    clients = Client.objects.all()
    status = SAV_file_status.objects.all()
    products = Product.objects.all()
    return render(request, 'djangoApp/addSAVFile/addSAVFile.html', { 'sav_file_form': sav_file_form, 'clients': clients, 'status': status, 'products': products })

class SAVFileSearchListView(generic.ListView):
    template_name = 'djangoApp/searchSAVFile/searchSAVFile.html'
    context_object_name = 'results'

    """
    Display a SAV_file List page filtered by the search query.
    """
    def get_queryset(self):
        file_reference = self.request.GET.get('file_reference')
        client_name = self.request.GET.get('client_name')
        client_surname = self.request.GET.get('client_surname')
        product_model = self.request.GET.get('product_model')
        product_mark = self.request.GET.get('product_mark')
        product_serial_number = self.request.GET.get('product_serial_number')
        tracking_number = self.request.GET.get('tracking_number')
        results = SAV_file.objects.all()
        
        if file_reference:
            results = results.filter(file_reference__icontains = file_reference)

        if client_name:
            results = results.filter(client__name__icontains = client_name) 

        if client_surname:
            results = results.filter(client__surname__icontains = client_surname)
        
        if product_model:
            results = results.filter(product_referenced__model__icontains = product_model)

        if product_mark:
            results = results.filter(product_referenced__mark__icontains = product_mark) 

        if product_serial_number:
            results = results.filter(product_referenced__serial_number__icontains = product_serial_number)

        if tracking_number:
            results = results.filter(tracking_number__icontains = tracking_number)

        return results
