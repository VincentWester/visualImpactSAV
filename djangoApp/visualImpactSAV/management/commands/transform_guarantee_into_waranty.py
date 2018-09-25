# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from visualImpactSAV.models import Guarantee, Waranty

class Command(BaseCommand):

    help = "Transform Guarantee model into Waranty model"

    def handle(self, *args, **options):
        guarantee_all = Guarantee.objects.all().order_by('id')

        for guarantee in guarantee_all:
            kwargs = {
                'id': guarantee.id,
                'brand': guarantee.mark,
                'complements': guarantee.complements,
                'waranty_time': guarantee.guarantee_time,
                'procedure': guarantee.procedure
            }
            print(kwargs)
            waranty = Waranty(**kwargs)
            waranty.save()