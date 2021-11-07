# coding: utf-8
'''
Created on Sep 27, 2012

@author: yeti
'''
from builtins import object
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from patrocle.models import SMSMessage, Credit


class SMSAdmin(ModelAdmin):
    class Meta(object):
        model = SMSMessage
    
    list_display = ("expeditor", "destinatar", "mesaj", "cod_referinta_smslink", "timestamp_trimitere", "timestamp_confirmare",
                    "confirmat", "eroare_trimitere", "eroare_confirmare", "sender")

class CreditAdmin(ModelAdmin):
    class Meta(object):
        model = Credit
    
    list_display = ("content_type", "object_id", "content_object", "credit", "timestamp", "creat_de", "comentarii", "get_tip_display")

admin.site.register(SMSMessage, SMSAdmin)
admin.site.register(Credit, CreditAdmin)