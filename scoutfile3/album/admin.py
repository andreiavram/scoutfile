# coding: utf-8
'''
Created on Aug 28, 2012

@author: yeti
'''
from django.contrib import admin
from scoutfile3.album.models import Eveniment, ZiEveniment, Imagine, SetPoze,\
    EXIFData

admin.site.register(Eveniment)
admin.site.register(ZiEveniment)
admin.site.register(Imagine)
admin.site.register(SetPoze)
admin.site.register(EXIFData)