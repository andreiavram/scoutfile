# coding: utf-8
'''
Created on Jul 1, 2012

@author: yeti
'''
from future import standard_library
standard_library.install_aliases()
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.widgets import PasswordInput, Textarea
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from goodies.forms import CrispyBaseForm
from django.conf import settings
import logging
import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse

logger = logging.getLogger(__name__)

class LoginForm(forms.Form):
    username = forms.CharField(required = True, label = u"Email")
    password = forms.CharField(widget = PasswordInput, required = True, label = "Parolă")
    
    def clean(self):
        user = authenticate(username = self.cleaned_data['username'], password = self.cleaned_data['password'])
        if user is not None:
            if not user.is_active:
                raise ValidationError(u"Contul tău există, dar fie nu l-api activat, fie a fost blocat de un administrator")
        else:
            raise ValidationError(u"Emailul și parola sunt incorecte. Dacă ți-api uitat parola poți să folosești link-ul de mai jos ca să o resetezi")
        
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = "auth"
        self.helper.form_method = "post"
        self.helper.form_class = "form-vertical"
        self.helper.add_input(Submit('submit', u'Autentificare', css_class = "btn btn-primary"))

        super().__init__(*args, **kwargs)
