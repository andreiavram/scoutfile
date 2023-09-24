# coding: utf-8
from builtins import next
from builtins import str
from builtins import object
import datetime
import logging
import shutil
import traceback
from collections import Counter
from io import BytesIO
from zipfile import ZipFile

import os
from PIL import ExifTags
from PIL import Image
from django import forms
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models import PointField
from django.core.files.base import File, ContentFile
from django.core.mail import send_mail
from django.db.models import IntegerChoices, TextChoices
from django.urls import reverse
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
from django.db.models.signals import post_init
from django.dispatch.dispatcher import receiver
from photologue.models import ImageModel
from taggit.managers import TaggableManager
from unidecode import unidecode

from album.managers import RaportEvenimentManager

logger = logging.getLogger(__name__)

IMAGINE_PUBLISHED_STATUS = ((1, "Secret"), (2, "Centru Local"), (3, "Organizație"), (4, "Public"))


class ParticipantiEveniment(models.Model):
    eveniment = models.ForeignKey("Eveniment", on_delete=models.CASCADE)
    ramura_de_varsta = models.ForeignKey("structuri.RamuraDeVarsta", null=True, blank=True, on_delete=models.CASCADE)
    alta_categorie = models.CharField(max_length=255, null=True, blank=True)
    numar = models.IntegerField()


class TipuriEveniment(TextChoices):
    CAMP = "camp", "Camp"
    INTALNIRE = "intalnire", "Întâlnire"
    INTALNIRE_UNITATE = "intalnire_unitate", "Întâlnire unitate"
    INTALNIRE_PATRULA = "intalnire_patrula", "Întâlnire patrulă"
    INTALNIRE_ORGANIZARE = "intalnire_organizare", "Întâlnire organizare"
    HIKE = "hike", "Hike"
    SOCIAL = "social", "Proiect social"
    COMUNITATE = "comunitate", "Proiect de implicare în comunitate"
    CITY_CHALLENGE = "citychallange", "City Challange"
    INTERNATIONAL = "international", "Proiect internațional"
    FESTIVAL = "festival", "Festival"
    ECOLOGIC = "ecologic", "Proiect ecologic"
    TRAINING = "training", "Stagiu / training"
    OTHER = "alta", "Alt tip de eveniment"


class StatusEveniment(TextChoices):
    PROPOSAL = "propus", "Propus"
    CONFIRMAT = "confirmat", "Confirmat"
    ONGOING = "derulare", "În derulare"
    FINISHED = "terminat", "Încheiat"
    CANCELLED = "anulat", "Anulat"


class RolParticipare(TextChoices):
    PARTICIPANT = "participant", "Participant"
    INSOTITOR = "insotitor", "Lider însoțitor"
    INVITAT = "invitat", "Invitat"
    COORDONATOR = "coordonator", "Coordonator"
    STAFF = "staff", "Membru staff"


class TipEveniment(models.Model):
    nume = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return u"%s" % self.nume


class Eveniment(models.Model):
    CAMPURI_PERMISE = [("telefon", u"Telefon"), ("adresa", u"Adresa poștală"), ("scoutid", u"Scout ID"),
                       ("email", u"Email"), ("status", u"Status"), ("cotizatie", u"Cotizație"), ("buletin", u"Buletin"),
                       ("credit", u"Credit")]

    centru_local = models.ForeignKey("structuri.CentruLocal", on_delete=models.CASCADE)
    nume = models.CharField(max_length=1024, verbose_name=u"Titlu")
    descriere = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(verbose_name=u"Începe pe",
                                      help_text=u"Folosește selectorul de date pentru a defini o dată de început")
    end_date = models.DateTimeField(verbose_name=u"Ține până pe",
                                    help_text=u"Folosește selectorul de date pentru a defini o dată de sfârșit")
    slug = models.SlugField(max_length=255, unique=True)
    custom_cover_photo = models.ForeignKey("Imagine", on_delete=models.CASCADE, null=True, blank=True)

    tip_eveniment_text = models.CharField(default="alta", max_length=255, null=True, blank=True,
                                          choices=TipuriEveniment.choices)
    tip_eveniment = models.ForeignKey(TipEveniment, on_delete=models.CASCADE)
    facebook_event_link = models.URLField(null=True, blank=True, verbose_name=u"Link eveniment Facebook",
                                          help_text=u"Folosește copy/paste pentru a lua link-ul din Facebook")
    articol_site_link = models.URLField(null=True, blank=True, verbose_name=u"Link articol site",
                                        help_text=u"Link-ul de la articolul de pe site-ul Centrului Local")

    status = models.CharField(max_length=255, null=True, blank=True, choices=StatusEveniment.choices)

    locatie_text = models.CharField(max_length=1024, null=True, blank=True, verbose_name=u"Locație")
    #   TODO: implementează situatia în care evenimentul are mai mult de o singură locație
    locatie_geo = models.CharField(max_length=1024)
    locatie = PointField(null=True, blank=True)

    #   TODO: add visibility settings to events
    published_status = models.IntegerField(default=2, choices=IMAGINE_PUBLISHED_STATUS, verbose_name=u"Vizibilitate")

    responsabil_raport = models.ForeignKey("structuri.Membru", null=True, blank=True, related_name="evenimente_raport",
                                           on_delete=models.CASCADE)
    responsabil_articol = models.ForeignKey("structuri.Membru", null=True, blank=True,
                                            related_name="evenimente_articol", on_delete=models.CASCADE)

    international = models.BooleanField(default=False,
                                        help_text=u"Dacă activitatea implică participanți din alte țări sau are loc în străinătate")
    organizator = models.CharField(max_length=255, null=True, blank=True,
                                   help_text=u"Dacă organizatorul este altul decât Centrul Local, notați-l aici")
    organizator_cercetas = models.BooleanField(default=True,
                                               help_text=u"Dacă organizatorul este un centru local sau ONCR, bifează aici")

    proiect = models.ForeignKey("proiecte.Project", null=True, blank=True, on_delete=models.CASCADE)
    campuri_aditionale = models.CharField(max_length=1024, null=True, blank=True)

    oncr_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"ONCR ID")

    frecventa = models.DurationField(null=True, blank=True)
    instanta_anterioara = models.ForeignKey("album.Eveniment", null=True, blank=True, on_delete=models.CASCADE,
                                            related_name="next_occurrences")
    instanta_urmatoare = models.ForeignKey("album.Eveniment", null=True, blank=True, on_delete=models.CASCADE,
                                           related_name="previous_occurrences")
    instante_extra = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

    text_invitatie = models.TextField(blank=True)
    slack_id = models.CharField(max_length=255, null=True, blank=True)
    external_album_link = models.URLField(null=True, blank=True, verbose_name="Link album extern")

    documents = models.ManyToManyField("documente.Document", blank=True, related_name="evenimente")

    class Meta(object):
        verbose_name = u"Eveniment"
        verbose_name_plural = u"Evenimente"
        ordering = ["-start_date"]

    def __str__(self):
        return u"%s" % self.nume

    def get_campuri_aditionale(self):
        if self.campuri_aditionale is None:
            return []

        vals = self.campuri_aditionale.strip(";").split(";")
        return [v for v in self.CAMPURI_PERMISE if v[0] in vals]

    @property
    def get_ramuri_de_varsta(self):
        participari = self.participareeveniment_set.exclude(status_participare=5)

        if self.status in ("terminat",):
            participari = participari.exclude(status_participare__in=(1, 2, 3))
        if participari.exists():
            membri = [p.membru for p in participari if p.membru]
            rdvs = [m.get_ramura_de_varsta(slug=True) for m in membri if m.get_ramura_de_varsta()]
            nonmembri = [p.nonmembru for p in participari if p.nonmembru]
            rdvs = Counter(rdvs)
            rdvs.update({"adulti": rdvs[None], "nonmembri": len(nonmembri)})
            rdvs = dict(rdvs)
        else:
            #   this code is here for events pre-2015
            totals = self.participantieveniment_set.filter()
            rdvs = {}
            for c in totals:
                key = c.ramura_de_varsta.slug if c.ramura_de_varsta is not None else c.alta_categorie
                rdvs[key] = c.numar

        rdvs = list(rdvs.items())

        from structuri.models import RamuraDeVarsta
        def rdv_sorter(item):
            rdv_slug = item[0]
            try:
                return RamuraDeVarsta.objects.get(slug=rdv_slug).varsta_intrare
            except RamuraDeVarsta.DoesNotExist:
                return 999

        rdvs.sort(key=rdv_sorter)
        return rdvs

    @property
    def raport(self):
        if self.raporteveniment_set.all().count():
            return self.raporteveniment_set.all()[0]
        return None

    @property
    def is_one_day(self):
        return self.start_date.date() == self.end_date.date()

    def save(self, *args, **kwargs):
        on_create = False
        if self.id is None:
            on_create = True

        retval = super(Eveniment, self).save(*args, **kwargs)

        if on_create:
            zi_index = 1
            date = self.start_date
            while date <= self.end_date:
                zi_eveniment = ZiEveniment(eveniment=self, date=date, index=zi_index)
                zi_index += 1
                date += datetime.timedelta(days=1)

                zi_eveniment.titlu = u"Ziua %d" % zi_eveniment.index
                zi_eveniment.save()

        else:
            #   check if days have to be recreated
            zile_eveniment = self.zieveniment_set.all().order_by("index")
            if zile_eveniment and zile_eveniment[0].date == self.start_date and zile_eveniment[
                zile_eveniment.count() - 1].date == self.end_date:
                #   same dates means do nothing
                return retval

            #   delete days outside the current span
            self.zieveniment_set.filter(Q(date__lt=self.start_date) | Q(date__gt=self.end_date)).delete()
            zi_index = 1
            date = self.start_date

            #   create only the days that were added by time shift. recreate index for all days
            while date <= self.end_date:
                zi_eveniment, created = ZiEveniment.objects.get_or_create(eveniment=self, date=date)
                date += datetime.timedelta(days=1)
                zi_eveniment.index = zi_index
                zi_index += 1
                zi_eveniment.save()

        return retval

    def scor_raportare(self):
        elemente_de_verificat = ["obiective", "grup_tinta", "activitati"]
        categorii_eveniment = ["aventura", "social", "cultural", "ecologie", "spiritual", "fundraising", "altele"]
        rapoarte = self.raporteveniment_set.all()
        if rapoarte.count():
            raport = rapoarte[0]
        else:
            return len(elemente_de_verificat) * -1

        scor = 0
        for field in elemente_de_verificat:
            if getattr(raport, field) is None or len(getattr(raport, field).strip()) == 0:
                scor -= 1

        if not any([getattr(raport, boolfield) for boolfield in categorii_eveniment]):
            scor -= 1

        if self.total_participanti == 0:
            scor -= 1

        if self.tip_eveniment is None:
            scor -= 1

        if self.locatie_text is None or len(self.locatie_text.strip()) == 0:
            scor -= 1

        if self.descriere is None or len(self.descriere.strip()) == 0:
            scor -= 1

        if raport.buget is None:
            scor -= 1

        return scor

    def scor_calitate(self):
        scor = self.scor_raportare()
        if scor < 0:
            return scor

        if self.articol_site_link:
            scor += 1

        if self.facebook_event_link:
            scor += 1

        if self.locatie_geo:
            scor += 1

        if self.total_poze > 0:
            scor += 1
            if self.total_poze > 100:
                scor += 1

        return scor

    def get_autori(self):
        autori = []
        for set_poze in self.setpoze_set.all():
            if set_poze.autor not in autori:
                autori.append(set_poze.autor)

        return autori

    def cover_photo(self):
        if self.custom_cover_photo:
            return self.custom_cover_photo

        if self.setpoze_set.all().count() == 0:
            return None

        for set_poze in self.setpoze_set.all():
            if set_poze.imagine_set.all().count():
                return set_poze.imagine_set.all()[0]

        return None

    @property
    def total_poze(self):
        return Imagine.objects.filter(set_poze__eveniment=self).count()

    @property
    def poze_out_of_bounds(self):
        return Imagine.objects.filter(
            Q(data__lt=self.start_date) | Q(data__gt=self.end_date) | Q(data__isnull=True)).filter(
            set_poze__eveniment=self).count()

    @property
    def has_poze_out_of_bounds(self):
        return self.poze_out_of_bounds > 0

    @property
    def total_participanti(self):
        list_totals = 0
        if self.participareeveniment_set.exists():
            list_totals = self.participareeveniment_set.filter(status_participare__in=(2, 3, 4)).count()
        manual_override_totals = self.participantieveniment_set.aggregate(Sum("numar"))['numar__sum']
        return max(list_totals, manual_override_totals) if manual_override_totals else list_totals

    def get_visibility_level(self, user=None):
        from structuri.models import TipAsociereMembruStructura
        visibility_level = 4
        if user is None:
            return visibility_level

        #   decide visibility level to go for
        if user and user.is_authenticated:
            visibility_level = 3  # this means organization level, logged in user
            user_profile = user.utilizator.membru
            if user_profile.centru_local == self.centru_local:
                visibility_level = 2
                if user_profile.are_calitate(TipAsociereMembruStructura.objects.get(nume=u"Păstrător al amintirilor"),
                                             self.centru_local):
                    visibility_level = 1

        #   superuser override
        if user.is_superuser:
            visibility_level = 1

        return visibility_level

    def locatie_geo_lat(self):
        if not self.locatie_geo:
            return 0
        return self.locatie_geo.split(";")[0]

    def locatie_geo_long(self):
        if not self.locatie_geo:
            return 0
        return self.locatie_geo.split(";")[1]

    def are_asociere(self, structura):
        filter_args = dict(content_type=ContentType.objects.get_for_model(structura), object_id=structura.id)
        return self.asocieri_structura.filter(**filter_args).count() > 0

    def ramura_de_varsta(self):
        from structuri.models import Unitate
        filter_args = dict(content_type=ContentType.objects.get_for_model(Unitate))
        qs = self.asocieri_structura.filter(**filter_args)
        if qs.count() == 1:
            return qs[0].content_object.ramura_de_varsta
        return None

    def creeaza_asociere_structura(self, structura):
        structura_args = dict(eveniment=self,
                              content_type=ContentType.objects.get_for_model(structura),
                              object_id=structura.id)
        AsociereEvenimentStructura.objects.create(**structura_args)

    def creeaza_participare(self, membru, rol=RolParticipare.PARTICIPANT):
        pe_args = dict(
            eveniment=self,
            membru=membru,
            data_sosire=self.start_date,
            data_plecare=self.end_date,
            status_participare=1,
            rol=rol
        )

        if not ParticipareEveniment.objects.filter(eveniment=self, membru=membru).exists():
            pe = ParticipareEveniment.objects.create(**pe_args)
            return pe
        return None

    def creeaza_participare_bulk(self, members_list, status_participare, rol=RolParticipare.PARTICIPANT):
        pe_args = dict(
            eveniment=self,
            data_sosire=self.start_date,
            data_plecare=self.end_date,
            status_participare=status_participare,
            rol=rol
        )

        existing_members = ParticipareEveniment.objects.filter(
            eveniment=self,
            membru_id__in=[m.id for m in members_list]
        ).values_list("membru_id", flat=True)

        members_to_add = [m for m in members_list if m.id not in existing_members]
        ParticipareEveniment.objects.bulk_create([ParticipareEveniment(membru=m, **pe_args) for m in members_to_add])

    @property
    def default_contribution(self, per_diem=False):
        if self.contribution_options.exists():
            return self.contribution_options.filter(is_default=True, per_diem=per_diem).first()
        return None


class EventCertification(models.Model):
    class RoleOptions(TextChoices):
        REQUIRED_FOR = "required", "Necesar pentru participare la"
        OFFERED_BY = "offered", "Oferit de"

    event = models.ForeignKey("album.Eveniment", on_delete=models.CASCADE, related_name="certificari")
    certification = models.ForeignKey("certificari.CertificationType", on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=RoleOptions.choices)
    limited_for_role = models.CharField(max_length=255, choices=RolParticipare.choices)

    def __str__(self):
        return f"{self.certification} este {self.get_role_display().lower} {self.event.nume}"


class AsociereEvenimentStructura(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=u"Tip structură", on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=u"Structură")
    content_object = GenericForeignKey()

    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE, related_name="asocieri_structura")
    slack_invite_sent_at = models.DateTimeField(null=True, blank=True)


class RaportEveniment(models.Model):
    parteneri = models.TextField(
        help_text=u"Câte unul pe linie, dacă există și un link va fi preluat automat de pe aceeași linie", null=True,
        blank=True)
    obiective = models.TextField(help_text=u"inclusiv obiective educative", null=True, blank=True)
    grup_tinta = models.TextField(null=True, blank=True)
    activitati = models.TextField(null=True, blank=True,
                                  help_text=u"Descriere semi-formală a activităților desfășurate")
    alti_beneficiari = models.TextField(null=True, blank=True)
    promovare = models.TextField(null=True, blank=True, help_text=u"Cum / dacă s-a promovat proiectul")
    buget = models.FloatField(null=True, blank=True, help_text=u"Estimativ, în RON")
    accept_publicare_raport_national = models.BooleanField(default=True, verbose_name="Acord raport ONCR",
                                                           help_text=u"Dacă se propune această activitate pentru raportul anual al ONCR")

    aventura = models.BooleanField(default=False)
    social = models.BooleanField(default=False)
    cultural = models.BooleanField(default=False)
    ecologie = models.BooleanField(default=False)
    spiritual = models.BooleanField(default=False)
    fundraising = models.BooleanField(default=False)
    altele = models.BooleanField(default=False)

    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False)
    is_leaf = models.BooleanField(default=False)
    editor = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    original_parent = models.ForeignKey("RaportEveniment", null=True, blank=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey("RaportEveniment", related_name="children", null=True, blank=True,
                               on_delete=models.SET_NULL)

    objects = RaportEvenimentManager()

    class Meta(object):
        ordering = ["-timestamp"]

    def parteneri_list(self):
        return self.attr_list(self.parteneri)

    def obiective_list(self):
        return self.attr_list(self.obiective)

    def activitati_list(self):
        return self.attr_list(self.activitati)

    def promovare_list(self):
        return self.attr_list(self.promovare)

    def attr_list(self, field):
        if field is None:
            return None
        return [a for a in field.split("\n") if a.strip() != ""]

    def save_new_version(self, user, *args, **kwargs):
        self.is_leaf = False
        self.is_locked = True
        self.save(*args, **kwargs)

        self.parent_id = self.id
        self.id = None
        self.user = user
        if self.original_parent is None:
            self.original_parent_id = self.parent_id
        self.is_leaf = True
        self.is_locked = False
        self.save(*args, **kwargs)


class StatusParticipare(IntegerChoices):
    MAYBE = 1, "Cu semnul întrebării"
    CONFIRMED = 2, "Confirmat"
    REFUSED = 8, "Refuzat invitația"
    DOWNPAYMENT_RECEIVED = 3, "Avans plătit"
    COMPLETED_OLD = 4, "Participare efectivă"
    COMPLETED_REAL = 7, "Participare efectivă (fizic)"
    COMPLETED_ONLINE = 6, "Participare efectivă (online)"
    CANCELLED = 5, "Participare anulată"
    UNKNOWN = 9, "Necunoscut"
    PAYMENT_CONFIRMED = 10, "Plata confirmată"
    INVITED = 11, "Invitat"
    EVENT_CANCELLED = 12, "Eveniment anulat"
    ORGANIZER_REJECTED = 13, "Respins de organizator"


class ParticipantEveniment(models.Model):
    nume = models.CharField(max_length=255)
    prenume = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telefon = models.CharField(max_length=255, blank=True, null=True)
    adresa_postala = models.CharField(max_length=255)

    def get_full_name(self):
        return "%s %s" % (self.prenume, self.nume.upper())

    def __str__(self):
        return self.get_full_name()


class ParticipareEveniment(models.Model):
    # TODO: a better way to implement this relationship needs to exist
    membru = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE, null=True, blank=True)
    nonmembru = models.ForeignKey("album.ParticipantEveniment", on_delete=models.SET_NULL, null=True, blank=True)

    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE)
    data_sosire = models.DateTimeField(null=True, blank=True)
    data_plecare = models.DateTimeField(null=True, blank=True)

    status_participare = models.IntegerField(default=StatusParticipare.UNKNOWN, choices=StatusParticipare.choices)
    detalii = models.TextField(null=True, blank=True)
    participant_notes = models.TextField(null=True, blank=True)
    rol = models.CharField(max_length=255, default=RolParticipare.PARTICIPANT, choices=RolParticipare.choices)

    ultima_modificare = models.DateTimeField(auto_now=True)
    user_modificare = models.ForeignKey("structuri.Membru", on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="participari_responsabil")

    contribution_option = models.ForeignKey("album.EventContributionOption", on_delete=models.SET_NULL, null=True,
                                            blank=True, verbose_name="Tip contribuție")
    contribution_payments = models.ManyToManyField("financiar.PaymentDocument", related_name="payments", blank=True,
                                                   help_text="Plăți contribuție")

    class Meta(object):
        ordering = ["-data_sosire", "status_participare"]
        unique_together = ["eveniment", "membru"]

    @property
    def is_partiala(self):
        return (self.data_sosire > self.eveniment.start_date + datetime.timedelta(seconds=3600 * 4)) or \
            (self.data_plecare < self.eveniment.end_date - datetime.timedelta(seconds=3600 * 4))

    def status_short_form(self):
        short_form_definition = {
            StatusParticipare.MAYBE: ("?", 1),
            StatusParticipare.CONFIRMED: ("C", 1),
            StatusParticipare.REFUSED: ("R", 2),
            StatusParticipare.DOWNPAYMENT_RECEIVED: ("$?", 1),
            StatusParticipare.COMPLETED_OLD: ("P", 0),
            StatusParticipare.COMPLETED_REAL: ("P", 0),
            StatusParticipare.COMPLETED_ONLINE: ("P(o)", 0),
            StatusParticipare.CANCELLED: ("A", 2),
            StatusParticipare.UNKNOWN: ("?", 1),
            StatusParticipare.PAYMENT_CONFIRMED: ("$", 1),
            StatusParticipare.INVITED: ("I", 1),
            StatusParticipare.ORGANIZER_REJECTED: ("X", 2),
            StatusParticipare.EVENT_CANCELLED: ("X", 2),
        }

        return short_form_definition.get(self.status_participare)

    @staticmethod
    def cotizatie_resolution(participare):
        if participare.membru.centru_local:
            return participare.membru.calculeaza_necesar_cotizatie()
        return 0

    @staticmethod
    def statut_cotizatie_resolution(participare):
        if participare.membru.centru_local:
            return participare.membru.status_cotizatie()
        return "n/a"

    def process_camp_aditional(self, camp):
        if self.nonmembru_id:
            resolution = {"telefon": lambda o: o.nonmembru.telefon,
                          "adresa": lambda o: o.nonmembru.adresa_postala,
                          "email": lambda o: o.nonmembru.email}
        elif self.membru_id:
            resolution = {"telefon": lambda o: o.membru.mobil,
                          "adresa": lambda o: o.membru.adresa_postala,
                          "scoutid": lambda o: o.membru.scout_id,
                          "email": lambda o: o.membru.email,
                          "status": ParticipareEveniment.statut_cotizatie_resolution,
                          "cotizatie": ParticipareEveniment.cotizatie_resolution,
                          "buletin": lambda o: o.membru.get_contact(u"Buletin"),
                          "credit": lambda o: o.membru.get_scor_credit_display(),
                          "unitate": lambda o: o.membru.get_unitate(),
                          "ramura_de_varsta": lambda o: o.membru.get_ramura_de_varsta()}
        else:
            return "-"

        val = resolution.get(camp, lambda o: "-")(self)
        return val if val else "-"

    def add_to_custom_field(self, slug, value):
        camp = CampArbitrarParticipareEveniment.objects.get(slug=slug, eveniment=self.eveniment)
        camp.set_value(value, self)

    def delete(self, **kwargs):
        if self.nonmembru:
            self.nonmembru.delete()
        super(ParticipareEveniment, self).delete(**kwargs)

    def ramura_de_varsta_in_eveniment(self):
        if self.membru is None:
            return None

    @property
    def total_payments(self):
        total_value = self.contribution_payments.aggregate(Sum('value'))
        return total_value['value__sum'] or 0

    @property
    def total_cost(self):
        contribution_option = self.contribution_option or self.eveniment.default_contribution
        if contribution_option.per_diem:
            return (self.data_plecare - self.data_sosire).days * contribution_option.value
        else:
            return contribution_option.value

    def payment_due(self):
        return self.total_cost - self.total_payments


class TipCampParticipare(TextChoices):
    TEXT = "text", "Text"
    NUMBER = "number", "Număr"
    BOOL = "bool", "Bifă"
    DATE = "date", "Dată"
    CHOICE = "choice", "Listă"


class CampArbitrarParticipareEveniment(models.Model):
    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE, related_name="campuri_arbitrare")
    nume = models.CharField(max_length=255)
    slug = models.SlugField()
    tip_camp = models.CharField(max_length=255, choices=TipCampParticipare.choices)
    implicit = models.CharField(max_length=255, null=True, blank=True)
    optional = models.BooleanField(default=True)
    user_fillable = models.BooleanField(default=False)
    explicatii_suplimentare = models.CharField(max_length=255, null=True, blank=True,
                                               help_text=u"Instrucțiuni despre cum să fie completat acest câmp, format, ...")
    afiseaza_sumar = models.BooleanField(default=False, verbose_name=u"Afișează sumar",
                                         help_text=u"Afișează totale la sfârșitul tabelului")

    config = models.JSONField(default=dict, help_text="Configurare adițională, opțională")

    tipuri_camp = {
        "text": forms.CharField,
        "number": forms.FloatField,
        "bool": forms.BooleanField,
        "date": forms.DateField,
        "choice": forms.ChoiceField
    }

    def get_form_field_class(self):
        return self.tipuri_camp[self.tip_camp]

    def _cache_instances(self):
        if hasattr(self, "_instante") and self._instante:
            return

        self._instante = list(self.instante.all())

    def get_instanta(self, participare):
        self._cache_instances()
        return next((a for a in self._instante if a.participare_id == participare.id), None)

    def get_value(self, participare=None, representation=False):
        if participare is None:
            return None

        try:
            instanta = self.get_instanta(participare=participare)
            return instanta.get_value() if not representation else instanta.get_representation()
        except InstantaCampArbitrarParticipareEveniment.DoesNotExist as e:
            return None
        except Exception as e:
            return None

    def get_representation(self, participare=None):
        value = self.get_value(participare, representation=True)
        if value is None:
            return "n/a"
        return value

    # def get_translated_value(self, value):
    #     if self.tip_camp == "bool":
    #         return True if value == "True" else False
    #     if self.tip_camp == "choice":
    #         for option in self.config.get("choices"):
    #             if value == str(option[0]):
    #                 return option[1]
    #         return ""
    #
    #     return value

    def set_value(self, valoare, participare=None):
        if participare is None:
            return

        instanta = self.get_instanta(participare=participare)
        if instanta is None:
            instanta_args = dict(participare=participare, camp=self)
            instanta = InstantaCampArbitrarParticipareEveniment.objects.create(**instanta_args)

        valoare_string = ""
        if self.tip_camp == "date":
            valoare_string = valoare.strftime("%d.%m.%Y")
        else:
            valoare_string = valoare

        instanta.valoare_text = valoare_string
        instanta.save()


class InstantaCampArbitrarParticipareEveniment(models.Model):
    camp = models.ForeignKey(CampArbitrarParticipareEveniment, related_name="instante", on_delete=models.CASCADE)
    participare = models.ForeignKey(ParticipareEveniment, on_delete=models.CASCADE)
    valoare_text = models.CharField(max_length=255, null=True, blank=True)

    def process_bool(self):
        return True if self.valoare_text.lower() == "true" else False

    def process_number(self):
        try:
            return int(self.valoare_text)
        except Exception as e:
            return float(self.valoare_text)
        except Exception as e:
            return 0

    def process_text(self):
        return self.valoare_text

    def process_date(self):
        return datetime.datetime.strptime(self.valoare_text, "%d.%M.%Y")

    def process_choice(self):
        for option in self.camp.config.get("choices", ()):
            if self.valoare_text == str(option[0]):
                return option[1]
        return self.valoare_text

    def get_value(self):
        if self.camp.tip_camp == "date":
            return datetime.datetime.strptime(self.valoare_text, "%d.%m.%Y").date()
        if self.camp.tip_camp == "bool":
            return self.valoare_text == "True"
        return self.valoare_text

    def get_representation(self):
        if self.camp.tip_camp == "choice":
            for options in self.camp.config.get("choices", {}):
                if self.valoare_text == str(options[0]):
                    return options[1]

        return self.get_value()

@receiver(post_init, sender=InstantaCampArbitrarParticipareEveniment)
def update_value(sender, instance, **kwargs):
    try:
        tip_camp = instance._tip_camp if hasattr("_tip_camp", instance) else instance.camp.tip_camp
        instance.valoare = getattr(instance, "process_{0}".format(tip_camp))
    except Exception as e:
        instance.valoare = None


class ZiEveniment(models.Model):
    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE)
    date = models.DateField()
    titlu = models.CharField(max_length=255)
    descriere = models.TextField(null=True, blank=True)
    index = models.IntegerField(default=1)

    class Meta(object):
        verbose_name = "Zi eveniment"
        verbose_name_plural = "Zile eveniment"
        ordering = ["index", "date"]

    def __str__(self):
        if self.titlu is not None and self.titlu != "":
            return self.titlu
        return "Ziua %d" % self.index

    def filter_photos(self, autor=None, user=None, **kwargs):
        backward_limit = datetime.datetime.combine(self.date, datetime.time(0, 0, 0)) + datetime.timedelta(hours=3)
        forward_limit = datetime.datetime.combine(self.date, datetime.time(3, 0, 0)) + datetime.timedelta(days=1)
        images = Imagine.objects.filter(set_poze__eveniment=self.eveniment, data__gte=backward_limit,
                                        data__lte=forward_limit)
        if autor is not None:
            images = images.filter(set_poze__autor__icontains=autor)

        if user:
            images = images.exclude(published_status__lt=self.eveniment.get_visibility_level(user))

        if len(list(kwargs.keys())):
            images = images.filter(**kwargs)
        images = images.order_by("data")
        return images

    def filter_public_photos(self, autor=None, user=None):
        return self.filter_photos(autor=autor, user=user, published_status=4)

    def author_distribution(self):
        authors = {}
        for image in self.filter_photos():
            if image.set_poze.autor.strip() in list(authors.keys()):
                authors[image.set_poze.autor.strip()] += 1
            else:
                authors[image.set_poze.autor.strip()] = 1

        return authors


SET_POZE_STATUSES = (
    (0, "Initialized"), (1, "Zip Uploaded"), (2, "Zip queued for processing"), (3, "Zip processed OK"),
    (4, "Zip error"))


class SetPoze(models.Model):
    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE)
    autor = models.CharField(max_length=255, null=True, blank=True,
                             help_text=u"Lăsați gol dacă încărcați pozele proprii")
    autor_user = models.ForeignKey("structuri.Membru", on_delete=models.SET_NULL, null=True, blank=True)
    zip_file = models.FilePathField(null=True, blank=True, path="/tmp")
    status = models.IntegerField(default=0, choices=SET_POZE_STATUSES)
    procent_procesat = models.IntegerField(default=0)

    date_uploaded = models.DateTimeField(auto_now=True)
    offset_secunde = models.IntegerField(default=0,
                                         help_text=u"Numărul de secunde cu care ceasul camerei voastre a fost decalat față de ceasul corect (poate fi și negativ). Foarte util pentru sincronizarea pozelor de la mai mulți fotografi")

    offset_changed = models.BooleanField(default=False, verbose_name=u"Offset-ul a fost modificat")
    default_visibility_level = models.IntegerField(default=-1, choices=IMAGINE_PUBLISHED_STATUS, null=True, blank=True)

    class Meta(object):
        verbose_name = "Set poze"
        verbose_name_plural = "seturi poze"
        ordering = ["-date_uploaded"]

    def __str__(self):
        return "Set %s (%s)" % (self.autor, self.eveniment)

    def get_autor(self):
        if self.autor:
            return "%s" % self.autor.strip()
        return "%s" % self.autor_user

    def process_zip_file(self):
        self.status = 2
        self.save()

        try:
            #   folder creation is not required on AWS
            event_path_no_root = os.path.join(settings.SCOUTFILE_ALBUM_STORAGE_ROOT,
                                              str(self.eveniment.centru_local.id),
                                              str(self.eveniment.id), unidecode(self.autor.replace(" ", "_")))

            # event_path = os.path.join(settings.MEDIA_DIRECTORY, event_path_no_root)
            # path creation is not a thing with S3
            # if not os.path.exists(os.path.join(settings.LOCAL_MEDIA_ROOT, event_path)):
            #     # TODO: create folders on AWS
            #     os.makedirs(os.path.join(settings.LOCAL_MEDIA_ROOT, event_path))

            #   setup temp path to unzip in
            import hashlib
            tmp_album_path = hashlib.sha224(event_path_no_root).hexdigest()
            tmp_album_path = os.path.join("/tmp", tmp_album_path)
            if os.path.exists(tmp_album_path):
                shutil.rmtree(tmp_album_path)
            os.makedirs(tmp_album_path)

            with ZipFile(self.zip_file) as zf:
                total_count = len(zf.infolist())
                current_count = 0
                for f in zf.infolist():
                    logger.debug("SetPoze: fisier extras %s" % f)

                    f.external_attr = 0o777 << 16
                    if f.filename.endswith("/") or os.path.splitext(f.filename)[1].lower() not in (
                    ".jpg", ".jpeg", ".png") or os.path.basename(f.filename).startswith(".") or f.filename.startswith(
                            "__"):
                        logger.debug(
                            "SetPoze skipping %s %s %s" % (f, f.filename, os.path.splitext(f.filename)[1].lower()))
                        continue

                    logger.debug("SetPoze: extracting file %s to S3:%s" % (f.filename, event_path_no_root))
                    zf.extract(f, tmp_album_path)

                    published_status = 2 if self.default_visibility_level < 0 else self.default_visibility_level
                    im = Imagine(set_poze=self, titlu=os.path.basename(f.filename), published_status=published_status)
                    file_handler = open(os.path.join(tmp_album_path, f.filename))
                    im.image.save(os.path.join(event_path_no_root, f.filename), File(file_handler), save=False)

                    try:
                        im.save(file_handler=file_handler, local_file_name=os.path.join(tmp_album_path, f.filename))
                    except Exception as e:
                        logger.error("eroare: %s %s" % (e, traceback.format_exc()))

                    #   Creating thumbnail and large urls without setting the actual flag on photosize
                    im.get_thumbnail_url()
                    im.get_large_url()

                    current_count += 1
                    current_percent = current_count * 100. / total_count
                    if current_percent - 5 > self.procent_procesat:
                        self.procent_procesat = int(current_percent)
                        self.save()

        except Exception as e:
            self.status = 4
            send_mail(u"Eroare la procesarea fisierului %s" % os.path.basename(self.zip_file),
                      "Arhiva încărcată de tine în evenimentul {0} nu a putut fi procesată. Eroarea a fost\n{1}".format(
                          self.eveniment, e),
                      settings.SYSTEM_EMAIL,
                      [self.autor_user.email, ])
            self.save()
            os.unlink(self.zip_file)
            shutil.rmtree(tmp_album_path)
            logger.error(
                "SetPoze: error extracting files: %s (%s), deleting uploaded file" % (e, traceback.format_exc()))
            return

        self.procent_procesat = 100
        self.status = 3
        self.save()

        send_mail(u"Arhivă procesată cu succes %s" % os.path.basename(self.zip_file),
                  "Arhiva încărcată de tine în evenimentul {0} a fost procesată cu succes și este disponibilă pe ScoutFile.".format(
                      self.eveniment),
                  settings.SYSTEM_EMAIL,
                  [self.autor_user.email, ])
        os.unlink(self.zip_file)
        shutil.rmtree(tmp_album_path)


class Imagine(ImageModel):
    set_poze = models.ForeignKey(SetPoze, on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateTimeField(null=True, blank=True)
    titlu = models.CharField(max_length=1024, null=True, blank=True)
    descriere = models.TextField(null=True, blank=True)
    resolution_x = models.IntegerField(null=True, blank=True)
    resolution_y = models.IntegerField(null=True, blank=True)

    score = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    is_face_processed = models.BooleanField(default=False)

    published_status = models.IntegerField(default=2, choices=IMAGINE_PUBLISHED_STATUS, verbose_name=u"Vizibilitate")

    tags = TaggableManager()

    class Meta(object):
        verbose_name = "Imagine"
        verbose_name_plural = "Imagini"
        ordering = ["date_taken", ]

    #   override for the original method of getting the filename
    # def _get_SIZE_filename(self, size):
    #     photosize = PhotoSizeCache().sizes.get(size)
    #     generator = PhotologueSpec(photo=self, photosize=photosize)
    #     return generator.cachefile_name

    def rotate(self, direction="cw"):
        try:
            im = Image.open(self.image.storage.open(self.image.name))
        except IOError:
            return

        im_format = im.format

        if direction == "cw":
            angle = -90
        else:
            angle = 90

        im = im.rotate(angle)
        im_buffer = BytesIO()
        im.save(im_buffer, im_format)
        buffer_contents = ContentFile(im_buffer.getvalue())
        self.image.storage.delete(self.image.name)
        self.image.storage.save(self.image.name, buffer_contents)

        try:
            self.clear_cache()
        except Exception as e:
            logger.debug("%s: deleted cached sizes (does this even work on S3?): %s, %s" % (
            self.__class__.__name__, e, traceback.format_exc()))

        return

    def get_day(self):
        #   compensation for (0, 3 AM) interval
        data = self.data
        ltime = datetime.time(data.hour, data.minute, data.second)
        magic_time = datetime.time(3, 0, 0)
        if ltime < magic_time:
            data = self.data - datetime.timedelta(days=1)
        return self.set_poze.eveniment.zieveniment_set.get(date=data)

    def get_next_photo(self, autor=None, user=None):
        photo = Imagine.objects.filter(published_status__gte=self.set_poze.eveniment.get_visibility_level(user=user),
                                       set_poze__eveniment=self.set_poze.eveniment,
                                       data__gt=self.data,
                                       data__lte=self.get_day().date + datetime.timedelta(days=1))
        if autor != None:
            photo = photo.filter(set_poze__autor__icontains=autor)

        photo = photo.order_by("data")

        if photo.count():
            return photo[0]
        return None

    def get_prev_photo(self, autor=None, user=None):
        backward_limit = datetime.datetime.combine(self.get_day().date, datetime.time(0, 0, 0)) + datetime.timedelta(
            hours=3)
        photo = Imagine.objects.filter(published_status__gte=self.set_poze.eveniment.get_visibility_level(user=user),
                                       set_poze__eveniment=self.set_poze.eveniment,
                                       data__lt=self.data, data__gte=backward_limit)
        if autor is not None:
            photo = photo.filter(set_poze__autor__icontains=autor)
        photo = photo.order_by("-data")

        if photo.count():
            return photo[0]
        return None

    def interesting_exifdata(self):
        return self.exifdata_set.filter(key__in=("Model",))

    def save(self, file_handler=None, local_file_name=None, *args, **kwargs):
        logger.debug("Calling Image.save with fh %s and lfn %s" % (file_handler, local_file_name))
        im = None
        if (self.resolution_x is None or self.resolution_y is None) and local_file_name is not None:
            logger.debug("Imagine.save: opening file: %s" % local_file_name)
            im = Image.open(local_file_name)
            self.resolution_x, self.resolution_y = im.size
            logger.debug("Imagine resolution: %d, %d" % (self.resolution_x, self.resolution_y))

        exif_data = {}
        on_create = False
        if self.id is None:
            on_create = True
            try:
                if im is None:
                    im = Image.open(local_file_name)
                info = im._getexif()
            except Exception as e:
                logger.debug("%s: %s, %s" % (self.__class__.__name__, e, traceback.format_exc()))
                info = None

            #  get current EXIF data
            try:
                if info is not None:
                    for tag, value in list(info.items()):
                        decoded = ExifTags.TAGS.get(tag, tag)
                        if decoded == "Maker Note":
                            continue

                        if decoded == "DateTimeOriginal":
                            self.data = datetime.datetime.strptime(value[0], "%Y:%m:%d %H:%M:%S")

                        exif_data[decoded] = value[0] if len(value) else None
            except Exception as e:
                logger.error("%s - %s" % (e, traceback.format_exc()))
        retval = super(Imagine, self).save(*args, **kwargs)

        if not self.is_face_processed:
            if not on_create:
                #    delete any existing faces, thus allowing detected face reset by
                #    switching the is_face_processed flag
                self.detectedface_set.all().delete()
            self.find_faces(local_file_name)
            self.is_face_processed = True

        if on_create:
            # clear currently EXIF data
            self.exifdata_set.all().delete()

            for key, value in list(exif_data.items()):
                value = value.decode("utf-8", errors="replace").replace("\x00", "\uFFFD")
                exif = EXIFData(imagine=self, key=key, value=value)
                try:
                    exif.save()
                except Exception as e:
                    continue

        if im is not None:
            del im
        return retval

    def vote_photo(self, score):
        self.score += score
        self.save()

    def find_faces(self, file_name=None):
        try:
            import cv
        except ImportError:
            return

        if file_name is None:
            return

        logger.debug("%s: %s" % (self.__class__.__name__, file_name))

        imcolor = cv.LoadImage(file_name)  # @UndefinedVariable
        detectors = ["haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"]
        for detector in detectors:
            haarFace = cv.Load(os.path.join(settings.STATIC_ROOT, detector))  # @UndefinedVariable
            storage = cv.CreateMemStorage()  # @UndefinedVariable
            detectedFaces = cv.HaarDetectObjects(imcolor, haarFace, storage, min_size=(200, 200))  # @UndefinedVariable
            if detectedFaces:
                for face in detectedFaces:
                    fata = DetectedFace(imagine=self, x=face[0][0], y=face[0][1], width=face[0][2], height=face[0][3])
                    fata.save()

        self.is_face_processed = True
        self.save()

    def check_visibility(self, user):
        if self.set_poze and self.set_poze.eveniment:
            return self.published_status >= self.set_poze.eveniment.get_visibility_level(user)
        return self.published_status == 4

    @classmethod
    def filter_visibility(cls, qs, eveniment=None, user=None):
        visibility_level = 4
        if eveniment and user:
            visibility_level = eveniment.get_visibility_level(user)
        elif user:
            qs = qs.select_related("set_poze__eveniment")
            return cls.objects.filter(id__in=[i.id for i in qs if i.check_visibility(user)])
        return qs.exclude(published_status__lt=visibility_level)

    def has_flags(self):
        return self.flagreport_set.all().count() > 0

    def to_json(self, dict=True):
        json_dict = {
            "id": self.id,
            "url_thumb": self.get_thumbnail_url(),
            "url_detail": reverse("album:poza_detail", kwargs={"pk": self.id}),
            "url_detail_img": self.get_large_url(),
            "titlu": "%s - %s" % (self.set_poze.eveniment.nume, self.titlu),
            "descriere": self.descriere or "",
            "autor": self.set_poze.get_autor(),
            "data": self.data.strftime("%d %B %Y %H:%M:%S") if self.data else datetime.datetime.now().strftime(
                "%d %B %Y %H:%M:%S"),
            "tags": [t for t in self.tags.names()[:10]],
            "rotate_url": reverse("album:poza_rotate", kwargs={"pk": self.id}),
            "published_status_display": self.get_published_status_display(),
            "flag_url": reverse("album:poza_flag", kwargs={"pk": self.id}),
            "score": self.score,
            "has_flags": self.has_flags()
        }

        if dict:
            return json_dict

        import json
        return json.dumps(json_dict)


# tagging.register(Imagine)


class EXIFData(models.Model):
    imagine = models.ForeignKey(Imagine, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta(object):
        verbose_name = "EXIFData"
        verbose_name_plural = "EXIFData"

    def __str__(self):
        return "%s: %s" % (self.key, self.value)


FLAG_MOTIVES = (("personal", "Sunt în poză și nu sunt de acord să apară aici"),
                ("ofensa", "Consider că poza este ofensatoare"),
                ("nonscout", "Poza conține un comportament necercetășesc și nu ar trebui listată aici"),
                ("calitateslaba", "Poza este de calitate slabă și nu merită păstrată"),
                ("altul", "Alt motiv"))


class FlagReport(models.Model):
    imagine = models.ForeignKey(Imagine, on_delete=models.CASCADE)
    motiv = models.CharField(max_length=1024, choices=FLAG_MOTIVES)
    alt_motiv = models.CharField(max_length=1024, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name = "Raport poză"
        verbose_name_plural = "Rapoarte poze"
        ordering = ["-timestamp", "motiv"]

    def __str__(self):
        return "Raport de %s la #%d (%s)" % (self.motiv, self.imagine.id, self.imagine.set_poze.eveniment)


class DetectedFace(models.Model):
    imagine = models.ForeignKey(Imagine, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()


class EventContributionOption(models.Model):
    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE, related_name="contribution_options")
    value = models.FloatField(verbose_name="Valoare")
    description = models.TextField(blank=True, verbose_name="Descriere",
                                   help_text="Explicație pentru situațiile în care se aplică această contribuție")
    is_default = models.BooleanField(default=False, verbose_name="Implicit")
    config = models.JSONField(default=dict, null=True, blank=True)
    per_diem = models.BooleanField(default=False, verbose_name="Pe zi")

    def save(self, *args, **kwargs):
        try:
            option = self.eveniment.contribution_options.get(is_default=True, per_diem=self.per_diem)
        except EventContributionOption.DoesNotExist:
            option = None

        delayed_option_save = False
        if self.is_default is False and option is None:
            self.is_default = True
        if self.is_default and option is not None and option.id != self.id:
            option.is_default = False
            delayed_option_save = True
        super().save(*args, **kwargs)

        if option and delayed_option_save:
            option.save()

    def __str__(self):
        value = f"{self.value}"
        if self.per_diem:
            value += " / pe zi"
        if self.description:
            value += f" ({self.description})"
        if self.is_default:
            value += " - implicit"
        return value


class TrackEveniment(models.Model):
    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE)
    titlu = models.CharField(max_length=255)
    color = models.CharField(max_length=6, default="FFFFFF")

    responsabil = models.ForeignKey("structuri.Membru", null=True, blank=True, on_delete=models.SET_NULL)


class ProgramEveniment(models.Model):
    titlu = models.CharField(max_length=255)
    descriere = models.TextField()
    color = models.CharField(max_length=6, default="FFFFFF")

    tracks = models.ManyToManyField(TrackEveniment)
    parent = models.ForeignKey("album.ProgramEveniment", null=True, blank=True, on_delete=models.CASCADE)
    moment_inceput = models.DateTimeField()
    moment_sfarsit = models.DateTimeField()

    materiale = models.TextField()
    responsabil = models.ForeignKey("structuri.Membru", null=True, blank=True, on_delete=models.SET_NULL)


class LinkType(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class EventURL(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255, null=True, blank=True)
    role = models.ForeignKey(LinkType, null=True, blank=True, on_delete=models.SET_NULL)
    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE, related_name="external_links")

    def __str__(self):
        if self.title:
            return f"URL {self.title}: {self.url}"
        return f"URL {self.role}: {self.url}"


class EventGPXTrack(models.Model):
    eveniment = models.ForeignKey(Eveniment, on_delete=models.CASCADE, related_name="gpx_tracks")
    track = models.ForeignKey("locuri.GPXTrack", on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    parent = models.ForeignKey("album.EventGPXTrack", null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="executed")
    membri = models.ManyToManyField("structuri.Membru", blank=True)

    def __str__(self):
        return f"{self.title} - {self.eveniment}"
