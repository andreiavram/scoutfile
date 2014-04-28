# coding: utf8
from documente.models import PlataCotizatieTrimestru, ChitantaCotizatie, Registru, Adeziune, DocumentCotizatieSociala, \
    Document
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

admin.site.register(PlataCotizatieTrimestru)
admin.site.register(ChitantaCotizatie)
admin.site.register(Registru)
admin.site.register(Adeziune)
admin.site.register(Document)
admin.site.register(DocumentCotizatieSociala)