from django.conf.urls import include, url
from knox import views as knox_views

from .views.views_pdf_generator import (
    Pdf_generator_cost_estimate,
    Pdf_generator_client,
    Pdf_generator_furnisher,
    Pdf_answer_reparation,
)
from .views.home_page_views import (
    SAV_fileList,
)
from .views.user_views import (
    RegistrationView,
    LoginView,
    UserView,
)

urlpatterns = [
    url(
        r'^generatePdfClientCostEstimate/(?P<pkSAVFile>[\w\-]+)$$',
        Pdf_generator_cost_estimate.as_view(),
        name="generatePdfClientCostEstimate"
    ),
    url(
        r'^generatePdfClient/(?P<pkSAVFile>[\w\-]+)$$',
        Pdf_generator_client.as_view(),
        name="generatePdfClient"
    ),
    url(
        r'^generatePdfFurnisher/(?P<pkSAVFile>[\w\-]+)$$',
        Pdf_generator_furnisher.as_view(),
        name="generatePdfFurnisher"
    ),
    url(
        r'^generatePdfReparation/(?P<pkSAVFile>[\w\-]+)$$',
        Pdf_answer_reparation.as_view(),
        name="generatePdfReparation"
    ),
    url(r'^api/auth/register/', RegistrationView.as_view()),
    url(r'^api/auth/login/', LoginView.as_view()),
    url(r'^api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    url(r'^api/auth/user/', UserView.as_view()),
    url(
        r'^api/dossiers_sav/',
        SAV_fileList.as_view(),
        name="restListSAVFiles"
    ),
]
