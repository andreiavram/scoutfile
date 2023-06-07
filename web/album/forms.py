# coding: utf-8
'''
Created on Aug 31, 2012

@author: yeti
'''
from builtins import object

from crispy_forms.layout import Fieldset, Layout, Field
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import RadioSelect, Textarea, CheckboxSelectMultiple
from taggit.forms import TagField

from album.models import FlagReport, FLAG_MOTIVES, RaportEveniment, ParticipareEveniment, \
    CampArbitrarParticipareEveniment, StatusParticipare
from album.models import SetPoze, Eveniment, Imagine, ZiEveniment
from generic.widgets import BootstrapDateTimeInput, BootstrapDateInput
from goodies.forms import CrispyBaseModelForm, CrispyBaseForm
from goodies.widgets import GeoCoordinatesInput, FacebookLinkWidget, TaggitTagsInput
from structuri.fields import NonAdminAutoCompleteSelectField


class ReportForm(CrispyBaseModelForm):
    class Meta(object):
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
                raise ValidationError(u"Daca api selectat 'alt motiv' trebuie să spui și care este acesta")

        return self.cleaned_data


class ReportFormNoButtons(ReportForm):
    has_submit_buttons = False


class SetPozeCreateForm(CrispyBaseModelForm):
    class Meta(object):
        model = SetPoze
        exclude = ["autor_user", "status", "zip_file", "procent_procesat"]


class SetPozeUpdateForm(CrispyBaseModelForm):
    class Meta(object):
        model = SetPoze
        exclude = ["procent_procesat", "autor_user", "status", "zip_file", "eveniment"]


class EvenimentCreateForm(CrispyBaseModelForm):
    class Meta(object):
        model = Eveniment
        exclude = ["centru_local", "custom_cover_photo", "ramuri_de_varsta", "activa", "slug"]

    descriere = forms.CharField(required=False, widget=Textarea(attrs={"cols": 400}))
    start_date = forms.DateTimeField(required=True, widget=BootstrapDateTimeInput(), label=u"Data început")
    end_date = forms.DateTimeField(required=True, widget=BootstrapDateTimeInput(), label=u"Data sfârșit")
    locatie_geo = forms.CharField(widget=GeoCoordinatesInput, required=False, label=u"Geolocație",
                                  help_text=u"Folosiți harta pentru a alege o locație")
    facebook_event_link = forms.URLField(widget=FacebookLinkWidget, required=False, label=u"Link eveniment Facebook")
    cover_photo = forms.FileField(label=u"Cover photo", required=False)

    responsabil_articol = NonAdminAutoCompleteSelectField("membri", label=u"Responsabil articol", required=False)
    responsabil_raport = NonAdminAutoCompleteSelectField("lideri", label=u"Responsabil raport", required=False)

    adauga_persoane = forms.BooleanField(required=False, label=u"Adaugă membri la eveniment?")
    adauga_lideri = forms.BooleanField(required=False, label=u"Adaugă liderii la eveniment?")

    def __init__(self, *args, **kwargs):
        super(EvenimentCreateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout("nume", Field("descriere", style="width:100%"), "status", "tip_eveniment", "start_date", "end_date",
                                    "facebook_event_link", "articol_site_link", "locatie_text", "locatie_geo",
                                    "organizator", "organizator_cercetas", "international", "published_status", "cover_photo",
                                    Fieldset(u"Responsabili", "responsabil_articol", "responsabil_raport"),
                                    Fieldset(u"Altele", "oncr_id"), Fieldset(u"Participați impliciți", "adauga_persoane", "adauga_lideri"))


class EvenimentUpdateForm(EvenimentCreateForm):
    class Meta(object):
        model = Eveniment
        exclude = ["centru_local", "custom_cover_photo", "ramuri_de_varsta"]


class PozaTagsForm(CrispyBaseModelForm):
    class Meta(object):
        model = Imagine
        fields = ["tags", "titlu", "descriere", "published_status"]

    tags = TagField(required=False, widget=TaggitTagsInput, label=u"Tag-uri")


class ZiForm(CrispyBaseModelForm):
    class Meta(object):
        model = ZiEveniment
        fields = ["titlu", "descriere"]


class RaportEvenimentForm(CrispyBaseModelForm):
    class Meta(object):
        model = RaportEveniment
        fields = ["parteneri", "obiective", "grup_tinta", "activitati", "alti_beneficiari",
                  "promovare", "buget", "accept_publicare_raport_national", "aventura",
                  "social", "cultural", "ecologie", "spiritual", "fundraising", "altele"]


class EvenimentParticipareBaseForm(CrispyBaseModelForm):
    class Meta(object):
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
        field_args = dict(required=(not camp.optional) if camp.tip_camp != "bool" else False,
                          label=camp.nume,
                          help_text=camp.explicatii_suplimentare)

        if camp.tip_camp == "date":
            field_args['widget'] = BootstrapDateInput

        if camp.implicit:
            field_args['initial'] = camp.implicit

        return field_args


class EvenimentParticipareForm(EvenimentParticipareBaseForm):
    class Meta(object):
        model = ParticipareEveniment
        exclude = ["eveniment", "user_modificare", "nonmembru"]

    membru = NonAdminAutoCompleteSelectField("membri", label=u"Cercetaș")

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
        field_args = dict(required=(not camp.optional) if camp.tip_camp != "bool" else False,
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
    class Meta(object):
        model = CampArbitrarParticipareEveniment
        exclude = ["eveniment", "slug"]

    def __init__(self, *args, **kwargs):
        self.eveniment = kwargs.pop("eveniment")
        super(CampArbitrarForm, self).__init__(*args, **kwargs)

    def clean(self):
        if len(self.cleaned_data.get('implicit', "")) > 0 and self.cleaned_data['optional'] is True:
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
    status_participare = forms.MultipleChoiceField(choices=StatusParticipare.choices, widget=CheckboxSelectMultiple())

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
        for camp, valoare in list(cond.items()):
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
