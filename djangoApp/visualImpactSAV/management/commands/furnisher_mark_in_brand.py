# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from visualImpactSAV.models import Furnisher

class Command(BaseCommand):

    def handle(self, *args, **options):
    	furnishers = Furnisher.objects.all()
    	for f in furnishers:
    		f.brand = f.mark
    		f.save()