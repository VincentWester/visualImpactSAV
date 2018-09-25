# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from visualImpactSAV.models import Waranty

class Command(BaseCommand):

    help = "Transform Guarantee model into Waranty model"

    def handle(self, *args, **options):
    	waranties = Waranty.objects.all()
    	for w in waranties:
    		w.delete()