# coding: utf-8
'''
Created on Aug 31, 2012

@author: yeti
'''
from scoutfile3.generic.forms import CrispyBaseModelForm
from scoutfile3.album.models import FlagReport, FLAG_MOTIVES
from django import forms
from album.models import SetPoze
from django.forms.widgets import RadioSelect, Textarea
from django.core.exceptions import ValidationError
from django.forms.fields import CharField

class ReportForm(CrispyBaseModelForm):
    class Meta:
        model = FlagReport
        fields = ("motiv", "alt_motiv")
    
    
    def __init__(self, *args, **kwargs):
        retval = super(ReportForm, self).__init__(*args, **kwargs)
            
        self.helper.form_class = "form-vertical"
        return retval
        
        
    motiv = forms.ChoiceField(widget = RadioSelect, choices = FLAG_MOTIVES, required = True)
    alt_motiv = forms.CharField(widget = Textarea, required = False, label = u"Care?")
    
        
    def clean(self):
        if self.cleaned_data['motiv'] == "altul":
            if "alt_motiv" not in self.cleaned_data or len(self.cleaned_data["alt_motiv"].strip()) == 0:
                raise ValidationError(u"Daca ai selectat 'alt motiv' trebuie să spui și care este acesta")
        
        return self.cleaned_data
        
        
class SetPozeCreateForm(CrispyBaseModelForm):
    class Meta:
        model = SetPoze
        exclude = ["autor_user", "status"]
    

class SetPozeUpdateForm(CrispyBaseModelForm):
    class Meta:
        model = SetPoze
        exclude = ["autor_user", "status", "zip_file", "eveniment"]
        
        