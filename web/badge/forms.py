#coding: utf-8
from builtins import object
from ajax_select.fields import AutoCompleteSelectField
from badge.models import Badge
from crispy_forms.layout import Layout, Field, Div, Fieldset, HTML
from django import forms
from django.forms.widgets import Textarea, TextInput
from goodies.forms import CrispyBaseModelForm

from generic.widgets import BootstrapDateInput

__author__ = 'yeti'

from structuri.fields import NonAdminAutoCompleteSelectField


class BadgeForm(CrispyBaseModelForm):
    class Meta(object):
        model = Badge
        exclude = ("owner", "status", "poza_badge")

    nume = forms.CharField(required=True, label=u"Nume", widget=TextInput(attrs={"style": "width: 100%; font-size: 24px; line-height: 28px; padding: 10px 5px"}))
    descriere = forms.CharField(required=False, label=u"Descriere", widget=Textarea(attrs={"style": "width: 100%; height: 80px"}))
    designer_membru = NonAdminAutoCompleteSelectField("membri", label=u"Designer cercetaș", help_text=u"Dacă designerul este un membru, căutați-l aici", required=False)
    data_productie = forms.DateField(label=u"Data producție", help_text=u"Anul e important, dacă nu se știe data exactă", widget=BootstrapDateInput)
    poza = forms.FileField(label=u"Poză", required=False)

    def __init__(self, *args, **kwargs):
        super(BadgeForm, self).__init__(*args, **kwargs)

        self.helper.form_class = "scoutfile-form"
        self.helper.layout = Layout(Field("nume", css_class="input-xlarge"), Field("descriere"),
                                    Div(
                                        Fieldset(u"Tiraj & tip", Field("tip"), Field("tiraj"), Field("tiraj_exact"), Field("data_productie"), Field("disponibil_in"), css_class="span4"),
                                        Fieldset(u"Credite", Field("producator"), Field("designer"), Field("designer_membru"), css_class="span4"),
                                        Fieldset(u"Altele", Field("poza"), HTML("<img src = '%s' class = 'thumbnail'>" % self.instance.poza_badge.get_thumbnail_url() if self.instance.poza_badge else ""), css_class="span4"),
                                        css_class="row-fluid"), )
