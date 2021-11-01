# coding: utf8
from django.urls import path
from extra.views import EnciclopedieEntries

urlpatterns = [
    path('enciclopedie/', EnciclopedieEntries.as_view(), name="enciclopedia_temerarilor"),
]
