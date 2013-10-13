#coding: utf8
from django.conf.urls.defaults import patterns
from documente.views import DeclaratieCotizatieSocialaAdauga, CentruLocalRegistre, RegistruCreate, RegistruUpdate, RegistruDetail
from documente.views import CotizatieMembruAdauga

urlpatterns = patterns('structuri.views',
#     (r'cotizatie/adauga/$', CotizatieAdauga.as_view(), {}, "cotizatie_add"),
    (r'cotizatie/(?P<pk>\d+)/adauga/$', CotizatieMembruAdauga.as_view(), {}, "cotizatie_membru_add"),
#     (r'adeziune/adauga/$', AdeziuneAdauga.as_view(), {}, "adeziune_add"),
#     (r'document/adauga/$', AdeziuneAdauga.as_view(), {}, "document_add"),

    (r'declaratie/cotizatie-sociala/(?P<pk>\d+)/adauga/$', DeclaratieCotizatieSocialaAdauga.as_view(), {}, "declaratie_cotizatie_sociala_add"),

    (r'(?P<pk>\d)/registru/list/$', CentruLocalRegistre.as_view(), {}, "registre"),
    (r'(?P<pk>\d)/registru/adauga/$', RegistruCreate.as_view(), {}, "registru_add"),
    (r'registru/(?P<pk>\d)/edit/$', RegistruUpdate.as_view(), {}, "registru_edit"),
    (r'registru/(?P<pk>\d)/$', RegistruDetail.as_view(), {}, "registru_detail"),
)
