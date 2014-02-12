# coding: utf-8
'''
Created on Jul 1, 2012

@author: yeti
'''
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.widgets import PasswordInput, Textarea
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from goodies.forms import CrispyBaseForm
from settings import REDMINE_API_KEY
import logging
from django.utils import simplejson
import urllib
import urllib2

logger = logging.getLogger(__name__)

class LoginForm(forms.Form):
    username = forms.CharField(required = True, label = u"Email")
    password = forms.CharField(widget = PasswordInput, required = True, label = "Parolă")
    
    def clean(self):
        user = authenticate(username = self.cleaned_data['username'], password = self.cleaned_data['password'])
        if user is not None:
            if not user.is_active:
                raise ValidationError(u"Contul tău există, dar fie nu l-ai activat, fie a fost blocat de un administrator")
        else:
            raise ValidationError(u"Emailul și parola sunt incorecte. Dacă ți-ai uitat parola poți să folosești link-ul de mai jos ca să o resetezi")
        
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = "auth"
        self.helper.form_method = "post"
        self.helper.form_class = "form-vertical"
        self.helper.add_input(Submit('submit', u'Autentificare', css_class = "btn btn-primary"))

        return super(LoginForm, self).__init__(*args, **kwargs)


class IssueCreateForm(CrispyBaseForm):
    subject = forms.CharField(label = u"Titlu", help_text = u"Un text concis care descrie problema")
    description = forms.CharField(widget = Textarea(), label = u"Descriere", required = False, help_text = u"Descrie pe larg problema, și cum ai ajuns la ea, astfel încât să o putem reproduce și repara")
    category = forms.ChoiceField(label = u"Categorie", required = False)
    
    def __init__(self, *args, **kwargs):
        super(IssueCreateForm, self).__init__(*args, **kwargs)

        values = {"key" : REDMINE_API_KEY}
        data = urllib.urlencode(values)
        url_to_send = "http://yeti.albascout.ro/redmine/projects/1/issue_categories.json" + "?" + data
        try:
            response = urllib2.urlopen(url_to_send)
            json_object = simplejson.loads(response.read())
        except Exception, e:
            logger.error("%s: eroare la obtinerea bug-urilor: %s" % (self.__class__.__name__, e))
        
        json_object['issue_categories'].append({"id" : "", "name" : "---"})
        self.fields['category'].choices = ((a['id'], a['name']) for a in json_object['issue_categories'])