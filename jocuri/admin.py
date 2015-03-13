from django.contrib.admin.options import ModelAdmin
from jocuri.models import CategorieFiseActivitate

__author__ = "andrei"

from django.contrib import admin


class CategorieAdmin(ModelAdmin):
    list_display = ("nume", )


admin.site.register(CategorieFiseActivitate, CategorieAdmin)