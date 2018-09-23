from django.conf.urls import url

from .views.views_sav_files import SAVFileCreateView, SAVFileUpdateView, SAVFileDetailView, SAVFileListView
from .views.views_events import EventCreateView, EventUpdateView, EventDeleteView
from .views.views_designations import DesignationCreateView, DesignationUpdateView, DesignationDeleteView, DesignationListView
from .views.views_guarantee import GuaranteeCreateView, GuaranteeUpdateView, GuaranteeDeleteView, GuaranteeListView
from .views.views_furnisher import FurnisherCreateView, FurnisherUpdateView, FurnisherDeleteView, FurnisherListView

from .views.views_pdf_generator import Pdf_generator_cost_estimate, Pdf_generator_client, Pdf_generator_furnisher, Pdf_answer_reparation

urlpatterns = [
    url(r'^createSAVFile/$', SAVFileCreateView.as_view(), name="createSAVFile"),
    url(r'^updateSAVFile/(?P<pk>[\w\-]+)$', SAVFileUpdateView.as_view(), name='updateSAVFile'),
    url(r'^detailSAVFile/(?P<pk>[\w\-]+)$', SAVFileDetailView.as_view(), name='detailSAVFile'),
    url(r'^searchSAVFile/$', SAVFileListView.as_view(), name="searchSAVFile"),

    url(r'^createEvent/(?P<pkSAVFile>[\w\-]+)$$', EventCreateView.as_view(), name="createEvent"),
    url(r'^updateEvent/(?P<pk>[\w\-]+)$$', EventUpdateView.as_view(), name="updateEvent"),
    url(r'^deleteEvent/(?P<pk>[\w\-]+)$$', EventDeleteView.as_view(), name="deleteEvent"),

    url(r'^createDesignation/(?P<pkSAVFile>[\w\-]+)$$', DesignationCreateView.as_view(), name="createDesignation"),
    url(r'^updateDesignation/(?P<pk>[\w\-]+)$$', DesignationUpdateView.as_view(), name="updateDesignation"),
    url(r'^deleteDesignation/(?P<pk>[\w\-]+)$$', DesignationDeleteView.as_view(), name="deleteDesignation"),
    url(r'^listDesignation/(?P<pkSAVFile>[\w\-]+)$$', DesignationListView.as_view(), name="listDesignation"),

    url(r'^listGuarantee/$', GuaranteeListView.as_view(), name="listGuarantee"),
    url(r'^createGuarantee/$', GuaranteeCreateView.as_view(), name="createGuarantee"),
    url(r'^updateGuarantee/(?P<pk>[\w\-]+)$$', GuaranteeUpdateView.as_view(), name="updateGuarantee"),
    url(r'^deleteGuarantee/(?P<pk>[\w\-]+)$$', GuaranteeDeleteView.as_view(), name="deleteGuarantee"),

    url(r'^listFurnisher/$', FurnisherListView.as_view(), name="listFurnisher"),
    url(r'^createFurnisher/$', FurnisherCreateView.as_view(), name="createFurnisher"),
    url(r'^updateFurnisher/(?P<pk>[\w\-]+)$$', FurnisherUpdateView.as_view(), name="updateFurnisher"),
    url(r'^deleteFurnisher/(?P<pk>[\w\-]+)$$', FurnisherDeleteView.as_view(), name="deleteFurnisher"),

    url(r'^generatePdfClientCostEstimate/(?P<pkSAVFile>[\w\-]+)$$', Pdf_generator_cost_estimate.as_view(), name="generatePdfClientCostEstimate"),
    url(r'^generatePdfClient/(?P<pkSAVFile>[\w\-]+)$$', Pdf_generator_client.as_view(), name="generatePdfClient"),
    url(r'^generatePdfFurnisher/(?P<pkSAVFile>[\w\-]+)$$', Pdf_generator_furnisher.as_view(), name="generatePdfFurnisher"),
    url(r'^generatePdfReparation/(?P<pkSAVFile>[\w\-]+)$$', Pdf_answer_reparation.as_view(), name="generatePdfReparation"),
]
