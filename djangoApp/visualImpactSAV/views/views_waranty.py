# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from visualImpactSAV.models.business_models import Waranty
from visualImpactSAV.forms import WarantyForm

import constants
from .views_template_parameters_sav_files import ParameterCreateView, ParameterUpdateView, ParameterDeleteView


class WarantyCreateView(ParameterCreateView):
    model = Waranty
    form_class = WarantyForm

    def form_valid(self, form):
        self.object = form.save()
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(WarantyCreateView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:createWaranty', args=[], kwargs={})
        context['id_modal'] = 'createWaranty'
        context['action_to_made'] = _('Create')
        context['value_button'] = _('Create this %s') % _('waranty')

        return context


class WarantyUpdateView(ParameterUpdateView):
    model = Waranty
    form_class = WarantyForm

    def get_context_data(self, **kwargs):
        context = super(WarantyUpdateView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:updateWaranty', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'updateWaranty'
        context['action_to_made'] = _('Update')
        context['value_button'] = _('Update this %s') % _('waranty')

        return context


class WarantyDeleteView(ParameterDeleteView):
    model = Waranty

    def get_context_data(self, **kwargs):
        context = super(WarantyDeleteView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:deleteWaranty', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'deleteWaranty'
        context['action_to_made'] = _('Delete')
        context['value_button'] = _('Delete this %s') % _('waranty')

        return context

    def get_success_url(self, *args, **kwargs):
        return reverse(self.url_to_redirect, kwargs={})


class WarantyListView(LoginRequiredMixin, ListView):
    queryset = Waranty.objects.order_by('brand')
    template_name = 'djangoApp/Waranty/listWaranty.html'
    context_object_name = 'results'
    paginate_by = constants.DEFAULT_WARANTY_LIST_VIEW_PAGINATION_BY
