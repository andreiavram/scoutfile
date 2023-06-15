# coding: utf8
from django.contrib import admin

from documente.models import PlataCotizatieTrimestru, ChitantaCotizatie, Registru, Adeziune, DocumentCotizatieSociala, \
    Document, AsociereDocument, TipDocument

admin.site.register(PlataCotizatieTrimestru)
admin.site.register(ChitantaCotizatie)
admin.site.register(Registru)
admin.site.register(Adeziune)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    search_fields = ["titlu", "descriere"]


admin.site.register(DocumentCotizatieSociala)
admin.site.register(AsociereDocument)
admin.site.register(TipDocument)
