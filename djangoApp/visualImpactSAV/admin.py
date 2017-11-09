from django.contrib import admin

from .models import SAV_file_status, SAV_file

admin.site.register(SAV_file)
admin.site.register(SAV_file_status)