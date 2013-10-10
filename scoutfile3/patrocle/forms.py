# coding: utf-8
'''
Created on Sep 25, 2012

@author: yeti
'''
from generic.forms import CrispyBaseForm, CrispyBaseModelForm
from django import forms
from django.forms.widgets import Textarea, HiddenInput
from patrocle.models import Credit
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from crispy_forms.layout import Field, Layout, Div
from django.utils import simplejson
import logging

logger = logging.getLogger(__name__)

class SendSMSForm(CrispyBaseForm):
    destinatari = forms.CharField(widget = HiddenInput(), required = True, label = u"Destinatari")
    mesaj = forms.CharField(widget = Textarea, required = True)
    
    button_label = u"Trimite"
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SendSMSForm, self).__init__(*args, **kwargs)
        
        self.helper.form_class = "form-vertical"
        self.helper.form_id = "sms_send_form"
        self.helper.layout = Layout(Field("mesaj", css_class = "span6"), Div(css_id = "mesaj_count"), Field("destinatari"),)
        

    def clean_mesaj(self):
        data = self.cleaned_data['mesaj']
        if len(data) > 157:
            raise ValidationError(u"Mesajul nu poate fi mai mare de 160 de caractere!")
        
        return data
    
    def clean_destinatari(self):
        from structuri.models import PersoanaDeContact
        data = self.cleaned_data['destinatari']
        
        destinatari = [a for a in simplejson.loads(data) if len(a) > 1]
        
        
        # Verifica accesul utilizatorului curent la trimis SMS-uri la persoana X
        from structuri.models import Membru
        
        error_list = []
        rezervari = []
        for d in destinatari:
            ids = d[1].split(":")
            try:
                if len(ids) == 2:
                    u = Membru.objects.get(id = int(ids[1]))
                    p = PersoanaDeContact.objects.get(id = int(ids[0]))
                    d[1] = [u, p]
                else:
                    u = Membru.objects.get(id = int(ids[0]))
                    d[1] = [u, None]
            except Membru.DoesNotExist:
                error_list.append(u"%s : nu există niciun membru cu acest număr de telefon" % d[0])
                continue
            except PersoanaDeContact.DoesNotExist:
                error_list.append(u"%s : nu există niciun membru de familie cu acest număr de telefon" % d[0])
                continue
        
            # Verifica contul destinatarilor (pot primi SMSuri?)
            rezervare = u.rezerva_credit()
            if not rezervare:
                error_list.append(u"%s : nu există credit pentru acest numar de telefon, nu se pot trimite SMSuri" % d[0])
            else:
                rezervari.append(rezervare)
                    
            # Verifica accesul utilizatorului curent la trimis SMS-uri la persoana X
            if not self.request.user.get_profile().membru.can_sms(u):
                error_list.append(u"%s : utilizatorul tău nu are suficiente drepturi pentru a folosi acest număr de telefon" % d[0])
                
        if len(error_list):
            for r in rezervari:
                r.delete()
            if self._errors.has_key("mesaj"):
                self._errors['mesaj'] += error_list
            else:
                self._errors['mesaj'] = error_list
            raise ValidationError(u'<br />'.join(error_list))
                
        logger.debug("%s: %s" % (self.__class__.__name__, destinatari))
        return destinatari
        
    
class AsociereCreditForm(CrispyBaseModelForm):
    class Meta:
        model = Credit
        fields = ("content_type", "object_id", "credit", "comentarii")
        
    object_id = forms.IntegerField(widget = forms.Select(choices = ()), label = u"Structură")
    
    def __init__(self, *args, **kwargs):
        self.credit_maxim = kwargs.pop("credit_maxim")
        super(AsociereCreditForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].queryset = ContentType.objects.filter(name__in = (u"Centru Local", u"Unitate", u"Patrulă"))
        
    def clean_credit(self):
        if not ("credit" in self.cleaned_data and self.cleaned_data['credit']):
            raise ValidationError(u"Trebuie specificată valoarea creditului")
        
        if self.cleaned_data['credit'] > self.credit_maxim:
            raise ValidationError(u"Creditul total disponibil în sistem (%d) este mai mic decât valoarea cerută" % self.credit_maxim)
        
        return self.cleaned_data['credit']
        
        
        