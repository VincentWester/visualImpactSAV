from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^addSAVFile/$', views.addSAVFile, name="addSAVFile"),
    url(r'^saveSAVFile/$', views.saveSAVFile, name="saveSAVFile"),
    url(r'^searchSAVFile/$', views.SAVFileSearchListView.as_view(), name="searchSAVFile"),
]
