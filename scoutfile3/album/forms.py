# coding: utf-8
'''
Created on Aug 31, 2012

@author: yeti
'''
from crispy_forms.layout import Fieldset, Layout, Field
from django.core.urlresolvers import reverse
from taggit.forms import TagField
from goodies.forms import CrispyBaseModelForm
from django import forms
from django.forms.widgets import RadioSelect, Textarea
from django.core.exceptions import ValidationError

from goodies.widgets import BootstrapDateTimeInput, GeoCoordinatesInput, FacebookLinkWidget, TaggitTagsInput
from album.models import FlagReport, FLAG_MOTIVES, RaportEveniment
from album.models import SetPoze, Eveniment, Imagine, ZiEveniment


class ReportForm(CrispyBaseModelForm):
    class Meta:
        model = FlagReport
        fields = ("motiv", "alt_motiv")


    def __init__(self, *args, **kwargs):
        retval = super(ReportForm, self).__init__(*args, **kwargs)

        self.helper.form_class = "form-vertical"
        return retval


    motiv = forms.ChoiceField(widget=RadioSelect, choices=FLAG_MOTIVES, required=True)
    alt_motiv = forms.CharField(widget=Textarea, required=False, label=u"Care?")


    def clean(self):
        if self.cleaned_data['motiv'] == "altul":
            if "alt_motiv" not in self.cleaned_data or len(self.cleaned_data["alt_motiv"].strip()) == 0:
                raise ValidationError(u"Daca ai selectat 'alt motiv' trebuie să spui și care este acesta")

        return self.cleaned_data


class SetPozeCreateForm(CrispyBaseModelForm):
    class Meta:
        model = SetPoze
        exclude = ["autor_user", "status", "zip_file", "procent_procesat"]


class SetPozeUpdateForm(CrispyBaseModelForm):
    class Meta:
        model = SetPoze
        exclude = ["procent_procesat", "autor_user", "status", "zip_file", "eveniment"]


class EvenimentCreateForm(CrispyBaseModelForm):
    class Meta:
        model = Eveniment
        exclude = ["centru_local", "custom_cover_photo", "ramuri_de_varsta"]

    descriere = forms.CharField(required=False, widget=Textarea(attrs={"cols": 400}))
    start_date = forms.DateTimeField(required=True, widget=BootstrapDateTimeInput(), label=u"Data început")
    end_date = forms.DateTimeField(required=True, widget=BootstrapDateTimeInput(), label=u"Data sfârșit")
    locatie_geo = forms.CharField(widget=GeoCoordinatesInput, required=False, label=u"Geolocație",
                                  help_text=u"Folosiți harta pentru a alege o locație")
    facebook_event_link = forms.URLField(widget=FacebookLinkWidget, required=False, label=u"Link eveniment Facebook")
    cover_photo = forms.FileField(label=u"Cover photo", required=False)

    lupisori = forms.IntegerField(required=True)
    temerari = forms.IntegerField(required=True)
    exploratori = forms.IntegerField(required=True)
    seniori = forms.IntegerField(required=True)
    lideri = forms.IntegerField(required=True)
    adulti = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super(EvenimentCreateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout("nume", Field("descriere", style="width:100%"), "tip_eveniment", "start_date", "end_date", "slug",
                                    "facebook_event_link", "articol_site_link", "locatie_text", "locatie_geo",
                                    "published_status", "cover_photo", Fieldset(u"Participanți", "lupisori", "temerari",
                                                        "exploratori", "seniori", "lideri", "adulti"))


class EvenimentUpdateForm(EvenimentCreateForm):
    class Meta:
        model = Eveniment
        exclude = ["centru_local", "custom_cover_photo", "ramuri_de_varsta"]


class PozaTagsForm(CrispyBaseModelForm):
    class Meta:
        model = Imagine
        fields = ["tags", "titlu", "descriere", "published_status"]

    tags = TagField(required=False, widget=TaggitTagsInput, label=u"Tag-uri")


class ZiForm(CrispyBaseModelForm):
    class Meta:
        model = ZiEveniment
        fields = ["titlu", "descriere"]


class RaportEvenimentForm(CrispyBaseModelForm):
    class Meta:
        model = RaportEveniment
        fields = ["parteneri", "obiective", "grup_tinta", "activitati", "alti_beneficiari",
                  "promovare", "buget", "accept_publicare_raport_national"]


