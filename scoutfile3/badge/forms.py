#coding: utf-8
from ajax_select.fields import AutoCompleteSelectField
from crispy_forms.layout import Layout, Field, Div
from django.forms.widgets import Textarea
from goodies.forms import CrispyBaseModelForm
from badge.models import Badge
from django import forms
from generic.widgets import BootstrapDateInput

__author__ = 'yeti'


class BadgeForm(CrispyBaseModelForm):
    class Meta:
        model = Badge
        exclude = ("owner", "status", "poza_badge")

    designer_membru = AutoCompleteSelectField("membri", label=u"Designer cercetaș", help_text=u"Dacă designerul este un membru, căutați-l aici", required=False)
    data_productie = forms.DateField(label=u"Data producție", widget=BootstrapDateInput)
    descriere = forms.CharField(required=False, widget=Textarea, label=u"Descriere")

    def __init__(self, **kwargs):
        super(BadgeForm, self).__init__(**kwargs)

        self.helper.form_class = "scoutfile-form"
        self.helper.layout = Layout(Field("nume", css_class="input-xlarge"), Field("descriere"))


            # (Field("titlu", css_class="input-xlarge"), Field("descriere"), Field("descriere_joc"),
            #                         Field("obiective_educative"), Field("materiale_necesare"),
            #                         Div(
            #                             Div(Field("min_durata_string"), Field("max_durata_string"), Field("sursa"), css_class="span4"),
            #                             Div(Field("categorie"), Field("min_participanti"), Field("max_participanti"), Field("is_draft"),  css_class="span4"),
            #                             Div( Field("ramuri_de_varsta"), Field("tags"), css_class="span4"),
            #                             css_class="row-fluid"),
            #                         )
