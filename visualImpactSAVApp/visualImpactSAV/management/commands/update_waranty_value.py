# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from visualImpactSAV.models import SAV_file
import constants

from django.utils.translation import ugettext as _

class Command(BaseCommand):
    from visualImpactSAV.models import SAV_file_status
    help = 'Replace status of Waranty File AS'

    def handle(self, *args, **options):

        SAV_file.objects.filter(
            waranty="Sous garantie"
        ).update(
            waranty=constants.SAV_FILE_WARANTY_TYPE_INCLUDED
        )
        SAV_file.objects.filter(
            waranty="Hors garantie"
        ).update(
            waranty=constants.SAV_FILE_WARANTY_TYPE_EXCLUDED
        )
