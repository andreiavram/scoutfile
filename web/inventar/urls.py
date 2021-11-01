# coding: utf8
from django.urls import path, include
from inventar.views import LocatieAccess, LocatieAccessAction

urlpatterns = [
    path('locatie/acces/', LocatieAccess.as_view(), name="locatie_access"),
    path('locatie/acces/action/', LocatieAccessAction.as_view(), name="locatie_access_action"),
]
