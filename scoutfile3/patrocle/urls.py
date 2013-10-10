#coding: utf8
from django.conf.urls.defaults import patterns
from patrocle.views import SendSMS, ConfirmSMS, ListConfirmations,\
    PatrocleStats, ListaCredite, AsociazaCredit, ListGrupConfirmations

urlpatterns = patterns('patrocle.views',
    (r'send/$', SendSMS.as_view(), {}, "send_sms"),
    (r'confirm/$', ConfirmSMS.as_view(), {}, "confirm_sms"),
    (r'stats/$', PatrocleStats.as_view(), {}, "system_stats"), 
    (r'home/$', ListConfirmations.as_view(), {}, "home"),
    (r'group/(?P<cod>[0-9a-zA-Z\-]+)/$', ListGrupConfirmations.as_view(), {}, "grup_sms"),
    
    (r'credit/lista/$', ListaCredite.as_view(), {}, "credit_lista"),
    (r'credit/asociaza/$', AsociazaCredit.as_view(), {}, "credit_asociaza"),
)
