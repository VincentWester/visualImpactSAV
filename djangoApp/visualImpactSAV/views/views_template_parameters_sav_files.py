# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from visualImpactSAV.models import SAV_file


class ParameterCreateView(LoginRequiredMixin, CreateView):
    template_name = 'djangoApp/common/createOrUpdate.html'

    def dispatch(self, *args, **kwargs):
        if 'pkSAVFile' in kwargs:
            self.pkSAVFile = kwargs['pkSAVFile']
        return super(ParameterCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParameterCreateView, self).get_context_data(**kwargs)
        if hasattr(self, 'pkSAVFile'):
            context['pkSAVFile'] = self.pkSAVFile
        return context

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))

    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        sav_file = SAV_file.objects.get(id=self.kwargs['pkSAVFile'])
        form.instance.refered_SAV_file = sav_file
        self.object = form.save()
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)


class ParameterUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'djangoApp/common/createOrUpdate.html'

    def dispatch(self, *args, **kwargs):
        self.pk = kwargs['pk']
        return super(ParameterUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParameterUpdateView, self).get_context_data(**kwargs)
        context['pk'] = self.pk

        return context

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))

    def form_valid(self, form):
        self.object = form.save()
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponseRedirect(url)


class ParameterDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'djangoApp/common/confirmDelete.html'

    def get_success_url(self, *args, **kwargs):
        return reverse(self.url_to_redirect,  kwargs={'pk': self.object.refered_SAV_file.id})

    def dispatch(self, *args, **kwargs):
        self.pk = kwargs['pk']
        if self.get_object().__class__.__name__ == 'Waranty':
            self.url_to_redirect = 'visualImpactSAV:listWaranty'
        else:
            self.url_to_redirect = 'visualImpactSAV:updateSAVFile'
        return super(ParameterDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParameterDeleteView, self).get_context_data(**kwargs)
        context['name_class'] = self.object.__class__.__name__
        context['name_object'] = unicode(self.object)

        return context
