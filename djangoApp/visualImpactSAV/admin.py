from django.contrib import admin

from .models import SAV_file_status, Reparation_status, SAV_file, Event, Pdf_client_invoice_file

admin.site.register(SAV_file_status)
admin.site.register(Reparation_status)
admin.site.register(SAV_file)
admin.site.register(Event)
admin.site.register(Pdf_client_invoice_file)