from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^createSAVFile/$', views.SAVFileCreateView.as_view(), name="createSAVFile"),
    url(r'^updateSAVFile/(?P<pk>[\w\-]+)$', views.SAVFileUpdateView.as_view() , name='updateSAVFile'),
    url(r'^detailSAVFile/(?P<pk>[\w\-]+)$', views.SAVFileDetailView.as_view() , name='detailSAVFile'),
    url(r'^searchSAVFile/$', views.SAVFileListView.as_view(), name="searchSAVFile"),

    url(r'^createEvent/(?P<pkSAVFile>[\w\-]+)$$', views.EventCreateView.as_view(), name="createEvent"),
]
