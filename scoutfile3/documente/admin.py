# coding: utf8
from documente.models import PlataCotizatieTrimestru, ChitantaCotizatie, Registru
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

admin.site.register(PlataCotizatieTrimestru)
admin.site.register(ChitantaCotizatie)
admin.site.register(Registru)