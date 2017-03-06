# coding: utf-8
'''
Created on Jul 1, 2012

@author: yeti
'''
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from structuri.models import (RamuraDeVarsta, CentruLocal, Unitate,
    Patrula, TipAsociereMembruStructura, AsociereMembruStructura, Membru,
    TipInformatieContact, InformatieContact, AsociereMembruFamilie,
    TipRelatieFamilie)

admin.site.register(RamuraDeVarsta)
admin.site.register(CentruLocal)
admin.site.register(Unitate)
admin.site.register(Patrula)
admin.site.register(TipAsociereMembruStructura)
admin.site.register(AsociereMembruStructura)
admin.site.register(Membru)

class TipInformatieContactAdmin(ModelAdmin):
    class Meta:
        model = TipInformatieContact
    list_display = ("nume", "template_name", "relevanta")

admin.site.register(TipInformatieContact, TipInformatieContactAdmin)
admin.site.register(InformatieContact)

admin.site.register(AsociereMembruFamilie)
admin.site.register(TipRelatieFamilie)