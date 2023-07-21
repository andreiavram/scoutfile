# coding: utf-8
'''
Created on Aug 28, 2012

@author: yeti
'''
from django.contrib import admin

from album.models import Eveniment, ZiEveniment, Imagine, SetPoze, \
    EXIFData, DetectedFace, TipEveniment, FlagReport, ProgramEveniment, TrackEveniment, EventContributionOption, \
    LinkType, EventURL, EventGPXTrack
from documente.models import Document


class EvenimentDocumentsInline(admin.StackedInline):
    model = Eveniment.documents.through


class EvenimentGPXTrackInline(admin.StackedInline):
    model = EventGPXTrack


@admin.register(Eveniment)
class EvenimentAdmin(admin.ModelAdmin):
    search_fields = ["nume", ]
    inlines = [EvenimentDocumentsInline, EvenimentGPXTrackInline]


admin.site.register(ZiEveniment)
admin.site.register(Imagine)
admin.site.register(SetPoze)
admin.site.register(EXIFData)
admin.site.register(DetectedFace)
admin.site.register(TipEveniment)
admin.site.register(FlagReport)

admin.site.register(ProgramEveniment)
admin.site.register(TrackEveniment)
admin.site.register(EventContributionOption)
admin.site.register(LinkType)
admin.site.register(EventURL)
