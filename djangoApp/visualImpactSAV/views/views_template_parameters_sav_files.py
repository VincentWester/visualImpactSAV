# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from visualImpactSAV.models import SAV_file

class ParameterCreateView(CreateView):
    def dispatch(self, *args, **kwargs):
        self.pkSAVFile = kwargs['pkSAVFile']
        return super(ParameterCreateView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParameterCreateView, self).get_context_data(**kwargs)
        context['pkSAVFile'] = self.pkSAVFile
        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url }))

    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        sav_file = SAV_file.objects.get(file_reference = self.kwargs['pkSAVFile'])
        form.instance.refered_SAV_file = sav_file
        self.object = form.save()
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)

class ParameterUpdateView(UpdateView):
    def dispatch(self, *args, **kwargs):
        self.pk = kwargs['pk']
        return super(ParameterUpdateView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParameterUpdateView, self).get_context_data(**kwargs)
        context['pk'] = self.pk

        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url }))
        
    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        self.object = form.save()

        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)

class ParameterDeleteView(DeleteView):      
    #template_name = 'djangoApp/common/confirmDelete.html'

    #def dispatch(self, *args, **kwargs):
    #    self.pk = kwargs['pk']
    #    self.url = 'visualImpactSAV:listDesignation'
    #    return super(ParameterDeleteView, self).dispatch( *args, **kwargs)

    #def get_context_data(self, **kwargs):
    #    context = super(ParameterDeleteView, self).get_context_data(**kwargs)
    #    print self.pk
    #    context['id_to_delete'] = self.pk
    #    context['name_class'] = self.object.__class__.__name__
    #    context['name_object'] = self.object.designation

    #    return context

    def get_success_url(self, *args, **kwargs): 
        if self.url_to_redirect == 'visualImpactSAV:listDesignation':
            return reverse_lazy(self.url_to_redirect,  kwargs={ 'pkSAVFile' : self.object.refered_SAV_file.file_reference }) 
        else:
            return reverse_lazy(self.url_to_redirect,  kwargs={ 'pk' : self.object.refered_SAV_file.file_reference }) 
