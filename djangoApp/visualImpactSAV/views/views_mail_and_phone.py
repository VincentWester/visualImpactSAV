# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .views_template_parameters_sav_files import ParameterCreateView, ParameterUpdateView, ParameterDeleteView
from visualImpactSAV.models.business_models import MailAndPhone
from visualImpactSAV.models.session_models import SessionMailAndPhone
from visualImpactSAV.forms import MailAndPhoneForm

import constants


class MailAndPhoneUpdateView(ParameterUpdateView):
    model = MailAndPhone
    form_class = MailAndPhoneForm

    def get_context_data(self, **kwargs):
        context = super(MailAndPhoneUpdateView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:updateMailAndPhone', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'updateMailAndPhone'
        context['action_to_made'] = _('Update')
        context['value_button'] = _('Update this %s') % _('contact')

        return context


class MailAndPhoneDeleteView(ParameterDeleteView):
    model = MailAndPhone

    def get_context_data(self, **kwargs):
        context = super(MailAndPhoneDeleteView, self).get_context_data(**kwargs)
        context['url_action'] = reverse('visualImpactSAV:deleteMailAndPhone', args=[], kwargs={'pk': self.pk})
        context['id_modal'] = 'deleteMailAndPhone'
        context['action_to_made'] = _('Delete')
        context['value_button'] = _('Delete this %s') % _('contact')

        return context


class MailAndPhoneCreateView(ParameterCreateView):
    model = MailAndPhone
    form_class = MailAndPhoneForm

    def get_context_data(self, **kwargs):
        context = super(MailAndPhoneCreateView, self).get_context_data(**kwargs)
        context['id_modal'] = 'createMailAndPhone'
        context['action_to_made'] = _('Create')
        context['value_button'] = _('Create this %s') % _('contact')

        return context


class MailAndPhoneInSessionCreateView(MailAndPhoneCreateView):

    def get_context_data(self, **kwargs):
        context = super(MailAndPhoneInSessionCreateView, self).get_context_data(**kwargs)   
        context['url_action'] = reverse('visualImpactSAV:createMailAndPhoneInSession', args=[], kwargs={})
    
        return context

    def form_valid(self, form):
        session = SessionMailAndPhone.load()
        form.instance.in_session = session
        self.object = form.save()
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)


class MailAndPhoneInSAVFileCreateView(MailAndPhoneCreateView):

    def get_context_data(self, **kwargs):
        context = super(MailAndPhoneInSAVFileCreateView, self).get_context_data(**kwargs)   
        context['url_action'] = reverse('visualImpactSAV:createMailAndPhoneInSAVFile', args=[], kwargs={'pkSAVFile': self.pkSAVFile})
    
        return context
