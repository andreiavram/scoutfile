#coding: utf8
from django.conf.urls.defaults import patterns
from documente.views import DeclaratieCotizatieSocialaAdauga, CentruLocalRegistre, RegistruCreate, RegistruUpdate, RegistruDetail, SelectieAdaugareDocument, DecizieCuantumAdauga, DecizieCuantumDetail, CalculeazaAcoperireCotizatie, CotizatiiCentruLocal, CotizatiiLider, PreiaIncasariCasier
from documente.views import CotizatieMembruAdauga

urlpatterns = patterns('structuri.views',
#     (r'cotizatie/adauga/$', CotizatieAdauga.as_view(), {}, "cotizatie_add"),
    (r'cotizatie/(?P<pk>\d+)/adauga/$', CotizatieMembruAdauga.as_view(), {}, "cotizatie_membru_add"),
#     (r'adeziune/adauga/$', AdeziuneAdauga.as_view(), {}, "adeziune_add"),
#     (r'document/adauga/$', AdeziuneAdauga.as_view(), {}, "document_add"),

    (r'declaratie/cotizatie-sociala/(?P<pk>\d+)/adauga/$', DeclaratieCotizatieSocialaAdauga.as_view(), {}, "declaratie_cotizatie_sociala_add"),

    (r'(?P<pk>\d+)/registru/list/$', CentruLocalRegistre.as_view(), {}, "registre"),
    (r'(?P<pk>\d+)/registru/adauga/$', RegistruCreate.as_view(), {}, "registru_add"),
    (r'registru/(?P<pk>\d+)/edit/$', RegistruUpdate.as_view(), {}, "registru_edit"),
    (r'registru/(?P<pk>\d+)/$', RegistruDetail.as_view(), {}, "registru_detail"),

    (r'(?P<pk>\d+)/documente/selectie/$', SelectieAdaugareDocument.as_view(), {}, "selectie_document"),

    (r'(?P<pk>\d+)/documente/decizie/cuantum/adauga/$', DecizieCuantumAdauga.as_view(), {}, "decizie_cuantum_adauga"),
    (r'decizie/cuantum/(?P<pk>\d+)/$', DecizieCuantumDetail.as_view(), {}, "decizie_cuantum_detail"),
    (r'cotizatie/calculeaza-acoperire/$', CalculeazaAcoperireCotizatie.as_view(), {}, "cotizatie_calculeaza_acoperire"),
    (r'cotizatii/centru_local/(?P<pk>\d+)/$', CotizatiiCentruLocal.as_view(), {}, "cotizatii_centru_local"),
    (r'cotizatii/lider/(?P<pk>\d+)/$', CotizatiiLider.as_view(), {}, "cotizatii_lider"),
    (r'cotizatii/preia/(?P<pk>\d+)/$', PreiaIncasariCasier.as_view(), {}, "transfer_cotizatii"),
)
