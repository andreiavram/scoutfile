# coding: utf8
from django.urls import path
from patrocle.views import SendSMS, ConfirmSMS, ListConfirmations, \
    PatrocleStats, ListaCredite, AsociazaCredit, ListGrupConfirmations

urlpatterns = [
    path('send/', SendSMS.as_view(), name="send_sms"),
    path('confirm/', ConfirmSMS.as_view(), name="confirm_sms"),
    path('stats/', PatrocleStats.as_view(), name="system_stats"),
    path('home/', ListConfirmations.as_view(), name="home"),
    path('group/<str:cod>/', ListGrupConfirmations.as_view(), name="grup_sms"),

    path('credit/lista/', ListaCredite.as_view(), name="credit_lista"),
    path('credit/asociaza/', AsociazaCredit.as_view(), name="credit_asociaza"),
]
