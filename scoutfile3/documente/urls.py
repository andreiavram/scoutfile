#coding: utf8
from django.conf.urls.defaults import patterns
from scoutfile3.documente.views import CotizatieMembruAdauga

urlpatterns = patterns('scoutfile3.structuri.views',
#     (r'cotizatie/adauga/$', CotizatieAdauga.as_view(), {}, "cotizatie_add"),
    (r'cotizatie/(?P<pk>\d+)/adauga/$', CotizatieMembruAdauga.as_view(), {}, "cotizatie_membru_add"),
#     (r'adeziune/adauga/$', AdeziuneAdauga.as_view(), {}, "adeziune_add"),
#     (r'document/adauga/$', AdeziuneAdauga.as_view(), {}, "document_add"),
    
)
