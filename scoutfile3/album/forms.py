# coding: utf-8
'''
Created on Aug 31, 2012

@author: yeti
'''
from ajax_select.fields import AutoCompleteSelectField
from crispy_forms.layout import Fieldset, Layout, Field
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from taggit.forms import TagField
from goodies.forms import CrispyBaseModelForm
from django import forms
from django.forms.widgets import RadioSelect, Textarea
from django.core.exceptions import ValidationError

from goodies.widgets import BootstrapDateTimeInput, GeoCoordinatesInput, FacebookLinkWidget, TaggitTagsInput
from album.models import FlagReport, FLAG_MOTIVES, RaportEveniment, ParticipareEveniment, \
    CampArbitrarParticipareEveniment
from album.models import SetPoze, Eveniment, Imagine, ZiEveniment
from generic.widgets import BootstrapDateTimeInput, BootstrapDateInput


class ReportForm(CrispyBaseModelForm):
    class Meta:
        model = FlagReport
        fields = ("motiv", "alt_motiv")

    has_submit_buttons = False

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.helper.form_class = "form-vertical"
        self.helper.form_id = "raport_form"


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
        exclude = ["centru_local", "custom_cover_photo", "ramuri_de_varsta", "activa"]

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

    responsabil_articol = AutoCompleteSelectField("membri", label=u"Responsabil articol", required=False)
    responsabil_raport = AutoCompleteSelectField("lideri", label=u"Responsabil raport", required=False)

    def __init__(self, *args, **kwargs):
        super(EvenimentCreateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout("nume", Field("descriere", style="width:100%"), "status", "tip_eveniment", "start_date", "end_date", "slug",
                                    "facebook_event_link", "articol_site_link", "locatie_text", "locatie_geo",
                                    "organizator", "organizator_cercetas", "international", "published_status", "cover_photo",
                                    Fieldset(u"Responsabili", "responsabil_articol", "responsabil_raport"),
                                    Fieldset(u"Participanți", "lupisori", "temerari", "exploratori", "seniori", "lideri", "adulti"))


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


class EvenimentParticipareForm(CrispyBaseModelForm):
    class Meta:
        model = ParticipareEveniment
        exclude = ["eveniment", "user_modificare"]

    membru = AutoCompleteSelectField("membri", label=u"Cercetaș")
    data_sosire = forms.DateTimeField(widget=BootstrapDateTimeInput, label=u"Sosire")
    data_plecare = forms.DateTimeField(widget=BootstrapDateTimeInput, label=u"Plecare")

    def __init__(self, **kwargs):
        self.eveniment = kwargs.pop("eveniment")
        self.request = kwargs.pop("request")
        super(EvenimentParticipareForm, self).__init__(**kwargs)

        campuri = self.eveniment.camparbitrarparticipareeveniment_set.all()

        for camp in campuri:
            field_args = self.get_field_args(camp)
            self.fields[camp.slug] = camp.get_form_field_class()(**field_args)

    def get_field_args(self, camp):
        field_args = dict(required=not camp.optional,
                          label=camp.nume,
                          help_text=camp.explicatii_suplimentare)

        if camp.tip_camp == "date":
            field_args['widget'] = BootstrapDateInput

        if camp.implicit:
            field_args['initial'] = camp.implicit

        return field_args


class EvenimentParticipareUpdateForm(EvenimentParticipareForm):
    def get_field_args(self, camp):
        field_args = dict(required=not camp.optional,
                          label=camp.nume,
                          help_text=camp.explicatii_suplimentare)

        if camp.tip_camp == "date":
            field_args['widget'] = BootstrapDateInput

        value = camp.get_value(participare=self.instance)
        if value is not None:
            field_args['initial'] = value
        elif camp.implicit:
            field_args['initial'] = camp.implicit

        return field_args


class CampArbitrarForm(CrispyBaseModelForm):
    class Meta:
        model = CampArbitrarParticipareEveniment
        exclude = ["eveniment", "slug"]

    def __init__(self, *args, **kwargs):
        self.eveniment = kwargs.pop("eveniment")
        super(CampArbitrarForm, self).__init__(*args, **kwargs)

    def clean(self):
        if len(self.cleaned_data.get('implicit', "")) > 0 and self.cleaned_data['optional'] is False:
            raise ValidationError(u"Un câmp opțional nu poate avea valoare implicită!")

        cnt = self.eveniment.participareeveniment_set.all().count()
        if self.cleaned_data['optional'] is False and cnt > 0:
            if len(self.cleaned_data.get('implicit', "")) == 0:
                raise ValidationError(u"Un câmp obligatoriu trebuie să aibă valoare implicită când există deja înregistrări de participare!")
            #   daca se adauga un camp nou, obligatoriu dar care nu are valoare implicita e o problema

        return self.cleaned_data