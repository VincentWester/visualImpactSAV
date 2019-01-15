# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

index = TemplateView.as_view(template_name='reactApp/index.html')
