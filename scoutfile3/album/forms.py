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
from goodies.forms import CrispyBaseModelForm, CrispyBaseForm
from django import forms
from django.forms.widgets import RadioSelect, Textarea, CheckboxSelectMultiple
from django.core.exceptions import ValidationError

from goodies.widgets import BootstrapDateTimeInput, GeoCoordinatesInput, FacebookLinkWidget, TaggitTagsInput
from album.models import FlagReport, FLAG_MOTIVES, RaportEveniment, ParticipareEveniment, \
    CampArbitrarParticipareEveniment, STATUS_PARTICIPARE
from album.models import SetPoze, Eveniment, Imagine, ZiEveniment
from generic.widgets import BootstrapDateTimeInput, BootstrapDateInput


class ReportForm(CrispyBaseModelForm):
    class Meta:
        model = FlagReport
        fields = ("motiv", "alt_motiv")

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.helper.form_class = "form-vertical"
        self.helper.form_id = "raport_form"

    motiv = forms.ChoiceField(widget=RadioSelect, choices=FLAG_MOTIVES, required=True)
    alt_motiv = forms.CharField(widget=Textarea, required=False, label=u"Care?")

    def clean(self):
        if "motiv" in self.cleaned_data and self.cleaned_data['motiv'] == "altul":
            if "alt_motiv" not in self.cleaned_data or len(self.cleaned_data["alt_motiv"].strip()) == 0:
                raise ValidationError(u"Daca ai selectat 'alt motiv' trebuie să spui și care este acesta")

        return self.cleaned_data


class ReportFormNoButtons(ReportForm):
    has_submit_buttons = False

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


class EvenimentParticipareBaseForm(CrispyBaseModelForm):
    class Meta:
        model = ParticipareEveniment
        exclude = ["eveniment", "user_modificare", "membru", "nonmembru"]


    data_sosire = forms.DateTimeField(widget=BootstrapDateTimeInput, label=u"Sosire")
    data_plecare = forms.DateTimeField(widget=BootstrapDateTimeInput, label=u"Plecare")

    def __init__(self, **kwargs):
        self.eveniment = kwargs.pop("eveniment")
        self.request = kwargs.pop("request")
        super(EvenimentParticipareBaseForm, self).__init__(**kwargs)

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


class EvenimentParticipareForm(EvenimentParticipareBaseForm):
    class Meta:
        model = ParticipareEveniment
        exclude = ["eveniment", "user_modificare", "nonmembru"]

    membru = AutoCompleteSelectField("membri", label=u"Cercetaș")

    def __init__(self, **kwargs):
        super(EvenimentParticipareForm, self).__init__(**kwargs)

    def clean_membru(self):
        membru = self.cleaned_data.get("membru")
        if self.eveniment.participareeveniment_set.filter(membru=membru).count() > 0:
            raise ValidationError(u"Membrul există deja în lista de participanți (eventual verificați membrii care au anulat participarea?)")
        return membru


class EvenimentParticipareNonMembruForm(EvenimentParticipareBaseForm):
    nume = forms.CharField(required=True, label=u"Nume")
    prenume = forms.CharField(required=True, label=u"Prenume")
    email = forms.EmailField(required=False, label=u"Email")
    telefon = forms.CharField(required=False, label=u"Telefon")
    adresa_postala = forms.CharField(required=False, label=u"Adresă poștală", widget=Textarea)

    def __init__(self, **kwargs):
        super(EvenimentParticipareNonMembruForm, self).__init__(**kwargs)


class EvenimentParticipareUpdateMixin(object):
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


class EvenimentParticipareUpdateForm(EvenimentParticipareUpdateMixin, EvenimentParticipareForm):
    def clean_membru(self):
        return self.cleaned_data.get("membru", None)


class EvenimentParticipareNonmembruUpdateForm(EvenimentParticipareUpdateMixin, EvenimentParticipareNonMembruForm):
    pass


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


class EvenimentParticipantFilterForm(CrispyBaseForm):
    tip_export = forms.ChoiceField(choices=(), label=u"Export")
    filter_expression = forms.CharField(required=False, label=u"Filtru", help_text=u"Expresie pentru filtrarea participantilor, cu sintaxa camp1=valoare_camp1,camp2=valoare_camp2")
    status_participare = forms.MultipleChoiceField(choices=STATUS_PARTICIPARE, widget=CheckboxSelectMultiple())

    VALORI_BOOL = {"da": True, "nu": False}

    def __init__(self, *args, **kwargs):
        self.export_options = kwargs.pop("export_options", ())
        self.eveniment = kwargs.pop("eveniment")
        super(EvenimentParticipantFilterForm, self).__init__(*args, **kwargs)

        self.fields['tip_export'].choices = ((a[0], a[1]) for a in self.export_options)

    def clean_filter_expression(self):
        filters = self.cleaned_data.get('filter_expression')
        cond = {}
        if filters:
            for i in filters.split(","):
                parts = i.split("=")
                if len(parts) != 2:
                    raise ValidationError(u"Sintaxă greșită, folosește camp=val,camp2=val!")
                cond[parts[0].strip()] = parts[1].strip()

        cond_parsed = {}
        for camp, valoare in cond.items():
            try:
                camp_arbitrar = self.eveniment.camparbitrarparticipareeveniment_set.get(slug__iexact=camp)
                if camp_arbitrar.tip_camp != "bool":
                    raise ValidationError(u"Pentru moment, nu sunt suportate alte câmpuri decât cele de tip bifă! (%s)" % camp_arbitrar.nume)

                if self.VALORI_BOOL.get(valoare.lower(), None) is None:
                    raise ValidationError(u"Valorile câmpurilor pot fi doar 'da' sau 'nu'")

                cond_parsed[camp_arbitrar] = self.VALORI_BOOL.get(valoare, False)
            except CampArbitrarParticipareEveniment.DoesNotExist:
                raise ValidationError(u"Nu există niciun câmp %s!" % camp)

        return cond_parsed