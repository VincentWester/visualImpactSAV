# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from django.db.models import ProtectedError

from visualImpactSAV.models import Furnisher
from visualImpactSAV.forms import FurnisherForm

import constants
from .views_template_parameters_sav_files import ParameterCreateView, ParameterUpdateView, ParameterDeleteView


class FurnisherCreateView(ParameterCreateView):
    model = Furnisher
    form_class = FurnisherForm

    def form_valid(self, form):
        self.object = form.save()
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(FurnisherCreateView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:createFurnisher', args=[], kwargs={})
        context['id_modal'] = 'createFurnisher'
        context['action_to_made'] = _('Create')
        context['value_button'] = _('Create this %s') % _('furnisher')

        return context


class FurnisherUpdateView(ParameterUpdateView):
    model = Furnisher
    form_class = FurnisherForm

    def get_context_data(self, **kwargs):
        context = super(FurnisherUpdateView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:updateFurnisher', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'updateFurnisher'
        context['action_to_made'] = _('Update')
        context['value_button'] = _('Update this %s') % _('furnisher')

        return context


class FurnisherDeleteView(ParameterDeleteView):
    model = Furnisher

    def get_context_data(self, **kwargs):
        context = super(FurnisherDeleteView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:deleteFurnisher', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'deleteFurnisher'
        context['action_to_made'] = _('Delete')
        context['value_button'] = _('Delete this %s') % _('furnisher')

        return context

    def get_success_url(self, *args, **kwargs):
        return reverse(self.url_to_redirect, kwargs={})

    def delete(self, request, *args, **kwargs):
        try:
            return super(FurnisherDeleteView, self).delete(request, *args, **kwargs)
        except ProtectedError:
            url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
            return HttpResponse(
                render(
                    request,
                    'djangoApp/errors/nonValideSAVFile.html',
                    {'errors': 'Un de vos dossiers possède ce fournisseur comme référence', 'url': url}
                )
            )


class FurnisherListView(LoginRequiredMixin, ListView):
    queryset = Furnisher.objects.order_by('brand')
    template_name = 'djangoApp/Furnisher/listFurnisher.html'
    context_object_name = 'results'
    paginate_by = constants.DEFAULT_FURNISHER_LIST_VIEW_PAGINATION_BY
