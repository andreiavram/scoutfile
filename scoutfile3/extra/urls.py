#coding: utf8
from django.conf.urls.defaults import patterns
from extra.views import EnciclopedieEntries

urlpatterns = patterns('extra.views',
    (r'enciclopedie/$', EnciclopedieEntries.as_view(), {}, "enciclopedia_temerarilor"),
)
