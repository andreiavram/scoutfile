# coding: utf-8
'''
Created on Jul 1, 2012

@author: yeti
'''
from builtins import object
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from structuri.models import (RamuraDeVarsta, CentruLocal, Unitate,
                              Patrula, TipAsociereMembruStructura, AsociereMembruStructura, Membru,
                              TipInformatieContact, InformatieContact, AsociereMembruFamilie,
                              TipRelatieFamilie, TipAsociereStructuraStructura, AsociereStructuraStructura, Echipa)

admin.site.register(RamuraDeVarsta)
admin.site.register(CentruLocal)
admin.site.register(Unitate)
admin.site.register(Patrula)
admin.site.register(TipAsociereMembruStructura)
admin.site.register(AsociereMembruStructura)


@admin.register(Membru)
class MembruAdmin(admin.ModelAdmin):
    search_fields = ["nume", "prenume", "email"]


class TipInformatieContactAdmin(ModelAdmin):
    class Meta(object):
        model = TipInformatieContact
    list_display = ("nume", "template_name", "relevanta")

admin.site.register(TipInformatieContact, TipInformatieContactAdmin)
admin.site.register(InformatieContact)

admin.site.register(AsociereMembruFamilie)
admin.site.register(TipRelatieFamilie)

@admin.register(TipAsociereStructuraStructura)
class TipAsociereStructuraAdmin(ModelAdmin):
    list_display = ["nume", ]

@admin.register(AsociereStructuraStructura)
class AsociereStructuraAdmin(ModelAdmin):
    list_display = ["source_structure", "target_structure", "connection_type", "date_start", "date_end"]


@admin.register(Echipa)
class EchipaAdmin(ModelAdmin):
    list_display = ["nume"]
