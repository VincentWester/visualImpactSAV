# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

# models part
from visualImpactSAV.models import Guarantee
# forms part
from visualImpactSAV.forms import GuaranteeForm

from .views_template_parameters_sav_files import ParameterUpdateView, ParameterDeleteView

class GuaranteeCreateView(CreateView):
    model = Guarantee
    form_class = GuaranteeForm 
    template_name = 'djangoApp/Guarantee/createGuarantee.html'    

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


class GuaranteeUpdateView(ParameterUpdateView):
    model = Guarantee
    form_class = GuaranteeForm
    template_name = 'djangoApp/Guarantee/updateGuarantee.html'

    def get_context_data(self, **kwargs):
        context = super(GuaranteeUpdateView, self).get_context_data(**kwargs)
        context['current_event'] = self.object

        return context

class GuaranteeDeleteView(ParameterDeleteView):
    model = Guarantee
    template_name = 'djangoApp/Guarantee/confirmDeleteGuarantee.html'

    def dispatch(self, *args, **kwargs):
        self.pk = kwargs['pk']
        self.url_to_redirect = 'visualImpactSAV:listDesignation'
        return super(GuaranteeDeleteView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GuaranteeDeleteView, self).get_context_data(**kwargs)
        context['id_to_delete'] = self.pk
        context['name_class'] = self.object.__class__.__name__
        context['name_object'] = self.object.designation

        return context

DEFAULT_PAGINATION_BY = 40

class GuaranteeListView(LoginRequiredMixin, ListView):
    queryset = Guarantee.objects.order_by('mark')
    template_name = 'djangoApp/Guarantee/listGuarantee.html'
    context_object_name = 'results'
    paginate_by = DEFAULT_PAGINATION_BY