# coding: utf-8
'''
Created on Sep 27, 2012

@author: yeti
'''
from django.contrib import admin
from scoutfile3.patrocle.models import SMSMessage, Credit
from django.contrib.admin.options import ModelAdmin

class SMSAdmin(ModelAdmin):
    class Meta:
        model = SMSMessage
    
    list_display = ("expeditor", "destinatar", "mesaj", "cod_referinta_smslink", "timestamp_trimitere", "timestamp_confirmare",
                    "confirmat", "eroare_trimitere", "eroare_confirmare", "sender")

class CreditAdmin(ModelAdmin):
    class Meta:
        model = Credit
    
    list_display = ("content_type", "object_id", "content_object", "credit", "timestamp", "creat_de", "comentarii", "get_tip_display")

admin.site.register(SMSMessage, SMSAdmin)
admin.site.register(Credit, CreditAdmin)