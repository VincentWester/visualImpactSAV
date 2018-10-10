# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from visualImpactSAV.models import SAV_file
import constants

class Command(BaseCommand):
    from visualImpactSAV.models import SAV_file_status
    help = 'Replace status of File AS'

    def handle(self, *args, **options):
        SAV_file.objects.filter(sav_file_status__libelle="Ouvert").update(status=constants.SAV_FILE_STATUS_TYPE_OPENED)
        SAV_file.objects.filter(sav_file_status__libelle="Fermé").update(status=constants.SAV_FILE_STATUS_TYPE_CLOSED)
        SAV_file.objects.filter(sav_file_status__libelle="En litige").update(status=constants.SAV_FILE_STATUS_TYPE_PROBLEM)
        SAV_file.objects.filter(sav_file_status__libelle="En attente").update(status=constants.SAV_FILE_STATUS_TYPE_IN_PROGRESS)