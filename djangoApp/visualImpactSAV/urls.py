from django.conf.urls import include, url
from django.contrib import admin

from .views.views_sav_files import SAVFileCreateView, SAVFileUpdateView, SAVFileDetailView, SAVFileListView
from .views.views_events import EventCreateView, EventUpdateView, EventDeleteView
from .views.views_pdf_generator import PDFGeneratorCreateView

urlpatterns = [
    url(r'^createSAVFile/$', SAVFileCreateView.as_view(), name="createSAVFile"),
    url(r'^updateSAVFile/(?P<pk>[\w\-]+)$', SAVFileUpdateView.as_view() , name='updateSAVFile'),
    url(r'^detailSAVFile/(?P<pk>[\w\-]+)$', SAVFileDetailView.as_view() , name='detailSAVFile'),
    url(r'^searchSAVFile/$', SAVFileListView.as_view(), name="searchSAVFile"),

    url(r'^createEvent/(?P<pkSAVFile>[\w\-]+)$$', EventCreateView.as_view(), name="createEvent"),
    url(r'^updateEvent/(?P<pk>[\w\-]+)$$', EventUpdateView.as_view(), name="updateEvent"),
    url(r'^deleteEvent/(?P<pk>[\w\-]+)$$', EventDeleteView.as_view(), name="deleteEvent"),

    url(r'^generatePDF/(?P<pkSAVFile>[\w\-]+)$$', PDFGeneratorCreateView.as_view(), name="generatePDF"),
]
