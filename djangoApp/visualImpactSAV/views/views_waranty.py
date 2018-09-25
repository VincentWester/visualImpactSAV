# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

from visualImpactSAV.models import Waranty
from visualImpactSAV.forms import WarantyForm

import constants
from .views_template_parameters_sav_files import ParameterUpdateView


class WarantyCreateView(CreateView):
    model = Waranty
    form_class = WarantyForm
    template_name = 'djangoApp/Warantee/createWaranty.html'

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))

    def form_valid(self, form):
        self.object = form.save()
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)


class WarantyUpdateView(ParameterUpdateView):
    model = Waranty
    form_class = WarantyForm
    template_name = 'djangoApp/Waranty/updateWaranty.html'

    def get_context_data(self, **kwargs):
        context = super(WarantyUpdateView, self).get_context_data(**kwargs)
        context['current_waranty'] = self.object

        return context


class WarantyDeleteView(DeleteView):
    model = Waranty
    template_name = 'djangoApp/Waranty/confirmDeleteWaranty.html'

    def dispatch(self, *args, **kwargs):
        self.pk = kwargs['pk']
        self.url_to_redirect = 'visualImpactSAV:listWaranty'
        return super(WarantyDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WarantyDeleteView, self).get_context_data(**kwargs)
        context['id_to_delete'] = self.pk
        context['name_class'] = self.object.__class__.__name__
        context['name_object'] = self.object.mark

        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy(self.url_to_redirect, kwargs={})


class WarantyListView(LoginRequiredMixin, ListView):
    queryset = Waranty.objects.order_by('brand')
    template_name = 'djangoApp/Waranty/listWaranty.html'
    context_object_name = 'results'
    paginate_by = constants.DEFAULT_WARANTY_LIST_VIEW_PAGINATION_BY
