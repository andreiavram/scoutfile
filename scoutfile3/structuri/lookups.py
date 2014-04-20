# coding: utf-8
'''
Created on Sep 23, 2012

@author: yeti
'''
from ajax_select import LookupChannel
from structuri.models import Membru, Structura
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from settings import STATIC_URL


class MembriLookup(LookupChannel):
    model = Membru
    search_field = "nume"
    
    def get_query(self, q, request):
        qs = Membru.objects.filter(Q(nume__icontains=q) | Q(prenume__icontains = q))
        qs = Membru.objects.filter(id__in=[m.id for m in qs if m.centru_local == request.user.utilizator.membru.centru_local])
        return qs

    def check_auth(self, request):
        return True
    
    def format_match(self, obj):
        return render_to_string("structuri/membru_for_ajax.html", {"obj" : obj, "STATIC_URL" : STATIC_URL})
    
    def format_item_display(self, obj):
        return render_to_string("structuri/membru_for_ajax.html", {"obj" : obj, "STATIC_URL" : STATIC_URL})