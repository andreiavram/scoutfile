#coding: utf8
from django.conf.urls import patterns

from inventar.views import LocatieAccess, LocatieAccessAction

urlpatterns = patterns(
    'inventar.views',
    (r'locatie/acces/$', LocatieAccess.as_view(), {}, "locatie_access"),
    (r'locatie/acces/action/$', LocatieAccessAction.as_view(), {}, "locatie_access_action"),

)
