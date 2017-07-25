from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^services/$', views.services, name="services"),
    url(r'^addSAVFile/$', views.add_SAV_file, name="addSAVfile"),
]
