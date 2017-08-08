# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, render_to_response

from .models import SAV_file, SAV_file_status, Reparation_status
from .forms import SAV_fileForm

import operator

def home(request):
    return render(request, 'djangoApp/home/home.html')

def saveSAVFile(request):
    # create a form instance and populate it with data from the request:

    form = SAV_fileForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
    # process the data in form.cleaned_data as required    
        sav_file = SAV_file()
        sav_file.file_reference = 'VisualImpact-SAV-' + form.cleaned_data['file_reference']

        sav_file.sav_file_status = form.cleaned_data['sav_file_status']
        sav_file.reparation_status = form.cleaned_data['reparation_status']

        sav_file.name_client = form.cleaned_data['name_client']
        sav_file.street_client = form.cleaned_data['street_client']
        sav_file.city_client = form.cleaned_data['city_client']
        sav_file.zipcode_client = form.cleaned_data['zipcode_client']
        sav_file.email_client = form.cleaned_data['email_client']
        sav_file.phone_client = form.cleaned_data['phone_client']

        sav_file.mark_product = form.cleaned_data['mark_product']
        sav_file.name_product = form.cleaned_data['name_product']
        sav_file.serial_number_product = form.cleaned_data['serial_number_product']

        sav_file.tracking_number = form.cleaned_data['tracking_number']
        sav_file.out_of_order_reason = form.cleaned_data['out_of_order_reason']

        sav_file.file_import_export_note = form.cleaned_data['file_import_export_note']
        sav_file.file_import_export_reparation_client_side = form.cleaned_data['file_import_export_reparation_client_side']
        sav_file.file_import_export_reparation_furnisher_side = form.cleaned_data['file_import_export_reparation_furnisher_side']
        sav_file.save()

        return render(request, 'djangoApp/view.html', {'sav_file': sav_file})

    else:
        errors = ""
        for error in form.errors:
             errors += error + "   - "

        return HttpResponse('Le formulaire est mal rempli.\n   ' + errors)

def addSAVFile(request):
    sav_file_form = SAV_fileForm()
    sav_file_status = SAV_file_status.objects.all()
    reparation_status = Reparation_status.objects.all()
    return render(request, 'djangoApp/addSAVFile/addSAVFile.html', { 'sav_file_form': sav_file_form, 'sav_file_status': sav_file_status, 'reparation_status': reparation_status})

class SAVFileSearchListView(generic.ListView):
    template_name = 'djangoApp/searchSAVFile/searchSAVFile.html'
    context_object_name = 'results'
    list_SAV_file_status = SAV_file_status.objects.all()
    list_reparation_status = SAV_file_status.objects.all()

    """
    Display a SAV_file List page filtered by the search query.
    """
    def get_queryset(self):
        file_reference = self.request.GET.get('file_reference')
        tracking_number = self.request.GET.get('status')
        client_name = self.request.GET.get('client_name')
        product_model = self.request.GET.get('product_model')
        product_mark = self.request.GET.get('product_mark')
        product_serial_number = self.request.GET.get('product_serial_number')
        tracking_number = self.request.GET.get('tracking_number')
        results = SAV_file.objects.all()
        
        if file_reference:
            results = results.filter(file_reference__icontains = file_reference)

        if client_name:
            results = results.filter(name_client__icontains = client_name) 
        
        if product_model:
            results = results.filter(name_product__icontains = product_model)

        if product_mark:
            results = results.filter(mark_product__icontains = product_mark) 

        if product_serial_number:
            results = results.filter(serial_number_product__icontains = product_serial_number)

        if tracking_number:
            results = results.filter(tracking_number__icontains = tracking_number)

        return results
