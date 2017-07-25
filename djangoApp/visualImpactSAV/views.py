# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.shortcuts import render, render_to_response

from .models import SAV_file, Client, Product, SAV_file_status
from .forms import SAV_fileForm

def add_SAV_file(request):
    # if this is a POST request we need to process the form data
        # create a form instance and populate it with data from the request:
        #clients = Client.objects.all()
        #status = SAV_file_status.objects.all()
        #products = Product.objects.all()

        form = SAV_fileForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        
            sav_file = SAV_file()
            sav_file.file_reference = form.cleaned_data['file_reference']
            sav_file.save()

        #return render(request, 'djangoApp/addSAVFile.html', {'form': form})
            return render(request, 'djangoApp/addSAVFile.html', {'sav_file': sav_file})
        #return HttpResponseRedirect('vous avez bien rempli le formulaire de fiche SAV')

        else:
            return HttpResponse("Le formulaire est mal rempli.")
    #return HttpResponseRedirect('Le formulaire est mal rempli.')

#, 'clients': clients, 'status': status, 'products': products


def services(request):

    sav_file_form = SAV_fileForm()

    return render(request, 'djangoApp/services.html', { 'sav_file_form': sav_file_form })