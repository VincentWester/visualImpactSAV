from django.contrib import admin

from .models import SAV_file, SAV_file_status

admin.site.register(SAV_file_status)
admin.site.register(SAV_file)
