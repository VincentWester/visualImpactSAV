from django.contrib import admin

from .models import SAV_file_status, SAV_file, Guarantee

admin.site.register(SAV_file_status)
admin.site.register(SAV_file)
admin.site.register(Guarantee)
