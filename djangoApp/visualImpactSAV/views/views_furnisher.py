# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView
from django.db.models import ProtectedError

# models part
from visualImpactSAV.models import Furnisher
# forms part
from visualImpactSAV.forms import FurnisherForm

from .views_template_parameters_sav_files import ParameterUpdateView, ParameterDeleteView

class FurnisherCreateView(CreateView):
    model = Furnisher
    form_class = FurnisherForm
    template_name = 'djangoApp/Furnisher/createFurnisher.html'

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url }))

    def form_valid(self, form):
        self.object = form.save()
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)


class FurnisherUpdateView(ParameterUpdateView):
    model = Furnisher
    form_class = FurnisherForm
    template_name = 'djangoApp/Furnisher/updateFurnisher.html'

    def get_context_data(self, **kwargs):
        context = super(FurnisherUpdateView, self).get_context_data(**kwargs)
        context['current_furnisher'] = self.object

        return context

class FurnisherDeleteView(DeleteView):
    model = Furnisher
    template_name = 'djangoApp/Furnisher/confirmDeleteFurnisher.html'

    def dispatch(self, *args, **kwargs):
        self.pk = kwargs['pk']
        self.url_to_redirect = 'visualImpactSAV:listFurnisher'
        return super(FurnisherDeleteView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FurnisherDeleteView, self).get_context_data(**kwargs)
        context['id_to_delete'] = self.pk
        context['name_class'] = self.object.__class__.__name__
        context['name_object'] = self.object.mark

        return context

    def delete(self, request, *args, **kwargs):
        try:
            return super(FurnisherDeleteView, self).delete(request, *args, **kwargs)
        except ProtectedError:
            url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
            return HttpResponse(render(request, 'djangoApp/errors/nonValideSAVFile.html', {'errors': 'Un de vos dossiers possède ce fournisseur comme référence', 'url': url })) 


    def get_success_url(self, *args, **kwargs):
        return reverse_lazy(self.url_to_redirect, kwargs={})

DEFAULT_PAGINATION_BY = 40

class FurnisherListView(LoginRequiredMixin, ListView):
    queryset = Furnisher.objects.order_by('mark')
    template_name = 'djangoApp/Furnisher/listFurnisher.html'
    context_object_name = 'results'
    paginate_by = DEFAULT_PAGINATION_BY