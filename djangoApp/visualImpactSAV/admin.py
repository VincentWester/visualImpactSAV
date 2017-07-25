from django.contrib import admin

from .models import Address, Client, Product, SAV_file_status, SAV_file

admin.site.register(Address)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(SAV_file_status)
admin.site.register(SAV_file)