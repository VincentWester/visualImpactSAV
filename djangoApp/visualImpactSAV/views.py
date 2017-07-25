# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.shortcuts import render, render_to_response

from .models import SAV_file, Client, Product, SAV_file_status
from .forms import SAV_fileForm

def add_SAV_file(request):
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

        return render(request, 'djangoApp/addSAVFile.html', {'sav_file': sav_file})

    else:
        return HttpResponse('Le formulaire est mal rempli.')

def services(request):

    sav_file_form = SAV_fileForm()
    clients = Client.objects.all()
    status = SAV_file_status.objects.all()
    products = Product.objects.all()
    return render(request, 'djangoApp/services.html', { 'sav_file_form': sav_file_form, 'clients': clients, 'status': status, 'products': products })