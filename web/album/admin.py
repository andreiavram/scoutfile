# coding: utf-8
'''
Created on Aug 28, 2012

@author: yeti
'''
from django.contrib import admin

from album.models import Eveniment, ZiEveniment, Imagine, SetPoze,\
    EXIFData, DetectedFace, TipEveniment, FlagReport

admin.site.register(Eveniment)
admin.site.register(ZiEveniment)
admin.site.register(Imagine)
admin.site.register(SetPoze)
admin.site.register(EXIFData)
admin.site.register(DetectedFace)
admin.site.register(TipEveniment)
admin.site.register(FlagReport)