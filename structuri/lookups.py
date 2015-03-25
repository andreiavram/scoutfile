# coding: utf-8
"""
Created on Sep 23, 2012

@author: yeti
"""
from ajax_select import LookupChannel
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.conf import settings

from structuri.models import Membru


class MembriLookup(LookupChannel):
    model = Membru
    search_field = "nume"
    
    def get_query(self, q, request):
        qs = Membru.objects.filter(Q(nume__icontains=q) | Q(prenume__icontains=q))
        membri_centru_local = [m.id for m in qs if m.centru_local == request.user.utilizator.membru.centru_local]
        qs = Membru.objects.filter(id__in=membri_centru_local)
        return qs

    def check_auth(self, request):
        return True
    
    def format_match(self, obj):
        return render_to_string("structuri/membru_for_ajax.html", {"obj": obj, "STATIC_URL": settings.STATIC_URL})
    
    def format_item_display(self, obj):
        return render_to_string("structuri/membru_for_ajax.html", {"obj": obj, "STATIC_URL": settings.STATIC_URL})


class LideriLookup(MembriLookup):
    def get_query(self, q, request):
        qs = Membru.objects.filter(Q(nume__icontains=q) | Q(prenume__icontains=q))
        centru_local = request.user.utilizator.membru.centru_local
        qs = Membru.objects.filter(id__in=[m.id for m in qs if m.are_calitate("Lider", centru_local)])
        return qs