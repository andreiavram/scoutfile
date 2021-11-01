# coding: utf8
from django.urls import path
from documente.views import CotizatieMembruAdauga
from documente.views import DeclaratieCotizatieSocialaAdauga, CentruLocalRegistre, RegistruCreate, RegistruUpdate, \
    RegistruDetail, SelectieAdaugareDocument, DecizieCuantumAdauga, DecizieCuantumDetail, CalculeazaAcoperireCotizatie, \
    CotizatiiCentruLocal, CotizatiiLider, PreiaIncasariCasier, AdeziuneMembruModifica, AdeziuneMembruAdauga, \
    ChitantaPrintare, \
    DecizieGeneralaAdauga, DecizieGeneralaModifica, ToggleBlocatCotizatie

urlpatterns = [
    path('cotizatie/<int:pk>/adauga/', CotizatieMembruAdauga.as_view(), name="cotizatie_membru_add"),
    path('adeziune/<int:pk>/adauga/', AdeziuneMembruAdauga.as_view(), name="adeziune_add"),
    path('adeziune/<int:pk>/modifica/', AdeziuneMembruModifica.as_view(), name="adeziune_edit"),
    #     path('document/adauga/', AdeziuneAdauga.as_view(), name="document_add"),

    path('declaratie/cotizatie-sociala/<int:pk>/adauga/', DeclaratieCotizatieSocialaAdauga.as_view(),
         name="declaratie_cotizatie_sociala_add"),

    path('<int:pk>/registru/list/', CentruLocalRegistre.as_view(), name="registre"),
    path('<int:pk>/registru/adauga/', RegistruCreate.as_view(), name="registru_add"),
    path('registru/<int:pk>/edit/', RegistruUpdate.as_view(), name="registru_edit"),
    path('registru/<int:pk>/', RegistruDetail.as_view(), name="registru_detail"),

    path('<int:pk>/documente/selectie/', SelectieAdaugareDocument.as_view(), name="selectie_document"),

    path('<int:pk>/documente/decizie/cuantum/adauga/', DecizieCuantumAdauga.as_view(),
         name="decizie_cuantum_adauga"),
    path('decizie/cuantum/<int:pk>/', DecizieCuantumDetail.as_view(), name="decizie_cuantum_detail"),
    path('cotizatie/calculeaza-acoperire/', CalculeazaAcoperireCotizatie.as_view(),
         name="cotizatie_calculeaza_acoperire"),
    path('cotizatii/centru_local/<int:pk>/', CotizatiiCentruLocal.as_view(), name="cotizatii_centru_local"),
    path('cotizatii/lider/<int:pk>/', CotizatiiLider.as_view(), name="cotizatii_lider"),
    path('cotizatii/preia/<int:pk>/', PreiaIncasariCasier.as_view(), name="transfer_cotizatii"),

    path('chitanta/<int:pk>/print/', ChitantaPrintare.as_view(), name="chitanta_print"),

    path('<int:pk>/decizie/adauga/', DecizieGeneralaAdauga.as_view(), name="centru_local_decizie_adauga"),
    path('decizie/<int:pk>/modifica/', DecizieGeneralaModifica.as_view(), name="centru_local_decizie_modifica"),
    path('api/document/toggle/', ToggleBlocatCotizatie.as_view(), name="toggle_document_blocat"),
]
