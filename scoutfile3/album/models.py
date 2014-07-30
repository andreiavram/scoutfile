#coding: utf-8
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
from django.db.models.signals import post_init
from django.dispatch.dispatcher import receiver
from photologue.models import ImageModel
from PIL import Image
import datetime
import os
from unidecode import unidecode
from zipfile import ZipFile
import logging
import traceback
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from album.managers import RaportEvenimentManager
from django import forms
from generic.widgets import BootstrapDateInput

from settings import SCOUTFILE_ALBUM_STORAGE_ROOT, STATIC_ROOT, MEDIA_ROOT
from taggit.managers import TaggableManager
import settings


logger = logging.getLogger(__name__)


IMAGINE_PUBLISHED_STATUS = ((1, "Secret"), (2, "Centru Local"), (3, "Organizație"), (4, "Public"))


class ParticipantiEveniment(models.Model):
    eveniment = models.ForeignKey("Eveniment")
    ramura_de_varsta = models.ForeignKey("structuri.RamuraDeVarsta", null=True, blank=True)
    alta_categorie = models.CharField(max_length=255, null=True, blank=True)
    numar = models.IntegerField()


TIPURI_EVENIMENT = (("camp", "Camp"), ("intalnire", u"Întâlnire"), ("hike", "Hike"), ("social", "Proiect social"),
                    ("comunitate", u"Proiect de implicare în comunitate"), ("citychallange", u"City Challange"),
                    ("international", u"Proiect internațional"), ("festival", u"Festival"),
                    ("ecologic", u"Proiect ecologic"), ("alta", u"Alt tip de eveniment"), ("training", u"Stagiu / training"))


STATUS_EVENIMENT = (("propus", u"Propus"), ("confirmat", u"Confirmat"), ("derulare", u"În derulare"), ("terminat", u"Încheiat"))


class TipEveniment(models.Model):
    nume = models.CharField(max_length=255)
    slug = models.SlugField()

    def __unicode__(self):
        return u"%s" % self.nume


class Eveniment(models.Model):
    centru_local = models.ForeignKey("structuri.CentruLocal")
    nume = models.CharField(max_length=1024 , verbose_name=u"Titlu")
    descriere = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(verbose_name=u"Începe pe", help_text=u"Folosește selectorul de date pentru a defini o dată de început")
    end_date = models.DateTimeField(verbose_name=u"Ține până pe", help_text=u"Folosește selectorul de date pentru a defini o dată de sfârșit")
    slug = models.SlugField(max_length=255, unique=True)
    custom_cover_photo = models.ForeignKey("Imagine", null=True, blank=True)

    tip_eveniment_text = models.CharField(default="alta", max_length=255, null=True, blank=True, choices=TIPURI_EVENIMENT)
    tip_eveniment = models.ForeignKey(TipEveniment)
    facebook_event_link = models.URLField(null=True, blank=True, verbose_name=u"Link eveniment Facebook", help_text=u"Folosește copy/paste pentru a lua link-ul din Facebook")
    articol_site_link = models.URLField(null=True, blank=True, verbose_name=u"Link articol site", help_text=u"Link-ul de la articolul de pe site-ul Centrului Local")

    status = models.CharField(max_length=255, null=True, blank=True, choices=STATUS_EVENIMENT)

    locatie_text = models.CharField(max_length=1024, null=True, blank=True, verbose_name = u"Locație")
    #   TODO: implementează situatia în care evenimentul are mai mult de o singură locație
    locatie_geo = models.CharField(max_length=1024)

    #   TODO: add visibility settings to events
    published_status = models.IntegerField(default=2, choices=IMAGINE_PUBLISHED_STATUS, verbose_name=u"Vizibilitate")

    responsabil_raport = models.ForeignKey("structuri.Membru", null=True, blank=True, related_name="evenimente_raport")
    responsabil_articol = models.ForeignKey("structuri.Membru", null=True, blank=True, related_name="evenimente_articol")

    international = models.BooleanField(default=False, help_text=u"Dacă activitatea implică participanți din alte țări sau are loc în străinătate")
    organizator = models.CharField(max_length=255, null=True, blank=True, help_text=u"Dacă organizatorul este altul decât Centrul Local, notați-l aici")
    organizator_cercetas = models.BooleanField(default=True, help_text=u"Dacă organizatorul este un centru local sau ONCR, bifează aici")

    proiect = models.ForeignKey("proiecte.Project", null=True, blank=True)

    class Meta:
        verbose_name = u"Eveniment"
        verbose_name_plural = u"Evenimente"
        ordering = ["-start_date"]

    def __unicode__(self):
        return u"%s" % self.nume

    @property
    def get_ramuri_de_varsta(self):
        totals = self.participantieveniment_set.filter()
        rdvs = {}
        for c in totals:
            key = c.ramura_de_varsta.slug if c.ramura_de_varsta is not None else c.alta_categorie
            rdvs[key] = (c.numar, c)
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
            if zile_eveniment[0].date == self.start_date and zile_eveniment[zile_eveniment.count() - 1].date == self.end_date:
                #   same dates means do nothing
                return retval

            #   delete days outside the current span
            self.zieveniment_set.filter(Q(date__lt = self.start_date) | Q(date__gt = self.end_date)).delete()
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
        rapoarte = self.raporteveniment_set.all()
        if rapoarte.count():
            raport = rapoarte[0]
        else:
            return len(elemente_de_verificat) * -1

        scor = 0
        for field in elemente_de_verificat:
            if getattr(raport, field) is None or len(getattr(raport, field).strip()) == 0:
                scor -= 1

        if self.participantieveniment_set.all().count() == 0 or self.participantieveniment_set.all().aggregate(Sum('numar')) == 0:
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
        return Imagine.objects.filter(Q(data__lt=self.start_date) | Q(data__gt=self.end_date) | Q(data__isnull = True)).filter(set_poze__eveniment=self).count()

    @property
    def has_poze_out_of_bounds(self):
        return self.poze_out_of_bounds > 0

    @property
    def total_participanti(self):
        return self.participantieveniment_set.aggregate(Sum("numar"))['numar__sum']

    def get_visibility_level(self, user=None):
        from structuri.models import TipAsociereMembruStructura
        visibility_level = 4
        if user is None:
            return visibility_level

        #   decide visibility level to go for
        if user is not None and user.is_authenticated():
            visibility_level = 3    #   this means organization level, logged in user
            user_profile = user.get_profile().membru
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
        return self.asociereevenimentstructura_set.filter(**filter_args).count() > 0

    def ramura_de_varsta(self):
        from structuri.models import Unitate
        filter_args = dict(content_type=ContentType.objects.get_for_model(Unitate))
        qs = self.asociereevenimentstructura_set.filter(**filter_args)
        if qs.count() == 1:
            return qs[0].content_object.ramura_de_varsta
        return None

    def creeaza_asociere_structura(self, structura):
        structura_args = dict(eveniment=self,
                              content_type=ContentType.objects.get_for_model(structura),
                              object_id=structura.id)
        AsociereEvenimentStructura.objects.create(**structura_args)

class AsociereEvenimentStructura(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=u"Tip structură")
    object_id = models.PositiveIntegerField(verbose_name=u"Structură")
    content_object = GenericForeignKey()

    eveniment = models.ForeignKey(Eveniment)


class RaportEveniment(models.Model):
    parteneri = models.TextField(help_text=u"Câte unul pe linie, dacă există și un link va fi preluat automat de pe aceeași linie", null=True, blank=True)
    obiective = models.TextField(help_text=u"inclusiv obiective educative", null=True, blank=True)
    grup_tinta = models.TextField(null=True, blank=True)
    activitati = models.TextField(null=True, blank=True, help_text=u"Descriere semi-formală a activităților desfășurate")
    alti_beneficiari = models.TextField(null=True, blank=True)
    promovare = models.TextField(null=True, blank=True, help_text=u"Cum / dacă s-a promovat proiectul")
    buget = models.FloatField(null=True, blank=True, help_text=u"Estimativ, în RON")
    accept_publicare_raport_national = models.BooleanField(default=True, verbose_name="Acord raport ONCR", help_text=u"Dacă se propune această activitate pentru raportul anual al ONCR")

    eveniment = models.ForeignKey(Eveniment)
    is_locked = models.BooleanField(default=False)
    is_leaf = models.BooleanField(default=False)
    editor = models.ForeignKey("structuri.Membru")
    timestamp = models.DateTimeField(auto_now_add=True)

    original_parent = models.ForeignKey("RaportEveniment", null=True, blank=True)
    parent = models.ForeignKey("RaportEveniment", related_name="children", null=True, blank=True)

    objects = RaportEvenimentManager()

    class Meta:
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

        self.id = None
        self.parent = self
        self.user = user
        if self.original_parent is None:
            self.original_parent = self.parent
        self.is_leaf = True
        self.is_locked = False
        self.save(*args, **kwargs)

ROL_PARTICIPARE = (("participant", u"Participant"), ("coordonator", u"Coordonator"), ("staff", u"Membru staff"))


STATUS_PARTICIPARE = ((1, u"Cu semnul întrebării"), (2, u"Confirmat"), (3, u"Avans plătit"), (4, u"Participare efectivă"),
                      (5, u"Participare anulată"))


class ParticipareEveniment(models.Model):
    membru = models.ForeignKey("structuri.Membru")
    eveniment = models.ForeignKey(Eveniment)
    data_sosire = models.DateTimeField(null=True, blank=True)
    data_plecare = models.DateTimeField(null=True, blank=True)

    status_participare = models.IntegerField(default=1, choices=STATUS_PARTICIPARE)
    detalii = models.TextField(null=True, blank=True)
    rol = models.CharField(max_length=255, default="participant", choices=ROL_PARTICIPARE)

    ultima_modificare = models.DateTimeField(auto_now=True)
    user_modificare = models.ForeignKey("structuri.Membru", null=True, blank=True, related_name="participari_responsabil")

    class Meta:
        ordering = ["-data_sosire"]

    @property
    def is_partiala(self):
        return self.data_sosire > self.eveniment.start_date or self.data_plecare < self.eveniment.end_date



TIPURI_CAMP_PARTICIPARE = (("text", u"Text"), ("number", u"Număr"), ("bool", u"Bifă"), ("date", u"Dată"))


class CampArbitrarParticipareEveniment(models.Model):
    eveniment = models.ForeignKey(Eveniment)
    nume = models.CharField(max_length=255)
    slug = models.SlugField()
    tip_camp = models.CharField(max_length=255, choices=TIPURI_CAMP_PARTICIPARE)
    implicit = models.CharField(max_length=255, null=True, blank=True)
    optional = models.BooleanField(default=True)
    explicatii_suplimentare = models.CharField(max_length=255, null=True, blank=True, help_text=u"Instrucțiuni despre cum să fie completat acest câmp, format, ...")

    tipuri_camp = {"text": forms.CharField,
                   "number": forms.FloatField,
                   "bool": forms.BooleanField,
                   "date": forms.DateField}

    def get_form_field_class(self):
        return self.tipuri_camp[self.tip_camp]

    def get_value(self, participare=None):
        if participare is None:
            return None

        try:
            instanta = self.instante.get(participare=participare)
            if self.tip_camp == "date":
                return datetime.datetime.strptime(instanta.valoare_text, "%d.%m.%Y").date()
            if self.tip_camp == "bool":
                return instanta.valoare_text == "True"
            return instanta.valoare_text
        except InstantaCampArbitrarParticipareEveniment.DoesNotExist, e:
            return None

    def get_translated_value(self, value):
        if self.tip_camp == "bool":
            return True if value == "True" else False

        return value

    def set_value(self, valoare, participare=None):
        if participare is None:
            return

        try:
            instanta = self.instante.get(participare=participare)
        except InstantaCampArbitrarParticipareEveniment.DoesNotExist:
            instanta_args = dict(participare=participare, camp=self)
            instanta = InstantaCampArbitrarParticipareEveniment.objects.create(**instanta_args)

        if self.tip_camp == "date":
            valoare_string = valoare.strftime("%d.%m.%Y")
        else:
            valoare_string = valoare

        instanta.valoare_text = valoare_string
        instanta.save()

    
class InstantaCampArbitrarParticipareEveniment(models.Model):
    camp = models.ForeignKey(CampArbitrarParticipareEveniment, related_name="instante")
    participare = models.ForeignKey(ParticipareEveniment)
    valoare_text = models.CharField(max_length=255, null=True, blank=True)
    
    def process_bool(self):
        return True if self.valoare_text.lower() == "true" else False
        
    def process_number(self):
        try:
            return int(self.valoare_text)
        except Exception, e:
            return float(self.valoare_text)
        except Exception, e:
            return 0

    def process_text(self):
        return self.valoare_text

    def process_date(self):
        return datetime.datetime.strptime(self.valoare_text, "%d.%M.%Y")

    
@receiver(post_init, sender=InstantaCampArbitrarParticipareEveniment)
def update_value(sender, instance, **kwargs):
    try:
        instance.valoare = getattr(instance, "process_{0}".format(instance.camp.tip_camp))
    except Exception, e:
        instance.valoare = None


class ZiEveniment(models.Model):
    eveniment = models.ForeignKey(Eveniment)
    date = models.DateField()
    titlu = models.CharField(max_length=255)
    descriere = models.TextField(null=True, blank=True)
    index = models.IntegerField(default=1)

    class Meta:
        verbose_name = u"Zi eveniment"
        verbose_name_plural = u"Zile eveniment"
        ordering = ["index", "date"]

    def __unicode__(self):
        if self.titlu != None and self.titlu != "":
            return self.titlu
        return u"Ziua %d" % self.index

    def filter_photos(self, autor=None, user=None, **kwargs):
        backward_limit = datetime.datetime.combine(self.date, datetime.time(0, 0, 0)) + datetime.timedelta(hours=3)
        forward_limit = datetime.datetime.combine(self.date, datetime.time(3, 0, 0)) + datetime.timedelta(days = 1)
        images = Imagine.objects.filter(set_poze__eveniment=self.eveniment, data__gte=backward_limit,
                                        data__lte=forward_limit)
        if autor is not None:
            images = images.filter(set_poze__autor__icontains=autor)

        if user:
            images = images.exclude(published_status__lt=self.eveniment.get_visibility_level(user))

        if len(kwargs.keys()):
            images = images.filter(**kwargs)
        images = images.order_by("data")
        return images

    def filter_public_photos(self, autor = None, user = None):
        return self.filter_photos(self, autor=autor, user=user, published_status = 4)

    def author_distribution(self):
        authors = {}
        for image in self.filter_photos():
            if image.set_poze.autor.strip() in authors.keys():
                authors[image.set_poze.autor.strip()] += 1
            else:
                authors[image.set_poze.autor.strip()] = 1

        return authors


SET_POZE_STATUSES = (
(0, "Initialized"), (1, "Zip Uploaded"), (2, "Zip queued for processing"), (3, "Zip processed OK"), (4, "Zip error"))


class SetPoze(models.Model):
    eveniment = models.ForeignKey(Eveniment)
    autor = models.CharField(max_length=255, null=True, blank=True,
                             help_text=u"Lăsați gol dacă încărcați pozele proprii")
    autor_user = models.ForeignKey("structuri.Membru", null=True, blank=True)
    zip_file = models.FilePathField(null=True, blank=True, path="/tmp")
    status = models.IntegerField(default=0, choices=SET_POZE_STATUSES)
    procent_procesat = models.IntegerField(default=0)

    date_uploaded = models.DateTimeField(auto_now=True)
    offset_secunde = models.IntegerField(default=0,
                                         help_text="Numărul de secunde cu care ceasul camerei voastre a fost decalat față de ceasul corect (poate fi și negativ). Foarte util pentru sincronizarea pozelor de la mai mulți fotografi")
    offset_changed = models.BooleanField(default=False, verbose_name = u"Offset-ul a fost modificat")

    class Meta:
        verbose_name = u"Set poze"
        verbose_name_plural = "seturi poze"
        ordering = ["-date_uploaded"]

    def __unicode__(self):
        return u"Set %s (%s)" % (self.autor, self.eveniment)

    def get_autor(self):
        if self.autor:
            return u"%s" % self.autor.strip()
        return u"%s" % self.autor_user

    def process_zip_file(self):
        self.status = 2
        self.save()

        try:
            # TODO: create folders on AWS
            event_path_no_root = os.path.join(SCOUTFILE_ALBUM_STORAGE_ROOT, unicode(self.eveniment.centru_local.id),
                                              unicode(self.eveniment.id), unidecode(self.autor.replace(" ", "_")))
            event_path = os.path.join(MEDIA_ROOT, event_path_no_root)
            if not os.path.exists(os.path.join(MEDIA_ROOT, event_path)):
                # TODO: create folders on AWS
                os.makedirs(os.path.join(MEDIA_ROOT, event_path))

            # TODO: read the zipfile from AWS
            with ZipFile(self.zip_file) as zf:
                total_count = len(zf.infolist())
                current_count = 0
                for f in zf.infolist():
                    logger.debug("SetPoze: fisier extras %s" % f)
                    f.external_attr = 0777 << 16L
                    if f.filename.endswith("/") or os.path.splitext(f.filename)[1].lower() not in (".jpg", ".jpeg", ".png"):
                        logger.debug("SetPoze skipping %s %s %s" % (f, f.filename, os.path.splitext(f.filename)[1].lower()))
                        continue
                    logger.debug("SetPoze: extracting file %s to %s" % (f.filename, event_path))
                    zf.extract(f, event_path)
                    # TODO: do not populate the path to the image field, rather create the StorageFile object so that it uploads to AWS
                    im = Imagine(set_poze=self, titlu=os.path.basename(f.filename),
                                 image=os.path.join(event_path_no_root, f.filename))
                    logger.debug("SetPoze: poza: %s" % im.image)
                    try:
                        im.save()
                    except Exception, e:
                        logger.error("eroare: %s %s" % (e, traceback.format_exc()))
                    current_count += 1
                    current_percent = current_count * 100. / total_count
                    if current_percent - 5 > self.procent_procesat:
                        self.procent_procesat = int(current_percent)
                        self.save()

        except Exception, e:
            self.status = 4
            send_mail(u"Eroare la procesarea fisierului %s" % os.path.basename(self.zip_file),
                      u"Arhiva încărcată de tine în evenimentul {0} nu a putut fi procesată. Eroarea a fost\n{1}".format(
                          self.eveniment, e),
                      settings.SYSTEM_EMAIL,
                      [self.autor_user.email, ])
            self.save()
            os.unlink(self.zip_file)
            logger.error(
                "SetPoze: error extracting files: %s (%s), deleting uploaded file" % (e, traceback.format_exc()))
            return

        self.procent_procesat = 100
        self.status = 3
        self.save()

        send_mail(u"Arhivă procesată cu succes %s" % os.path.basename(self.zip_file),
                  u"Arhiva încărcată de tine în evenimentul {0} a fost procesată cu succes și este disponibilă pe ScoutFile.".format(
                      self.eveniment),
                  settings.SYSTEM_EMAIL,
                  [self.autor_user.email, ])
        os.unlink(self.zip_file)


class Imagine(ImageModel):
    set_poze = models.ForeignKey(SetPoze, null=True, blank=True)
    data = models.DateTimeField(null=True, blank=True)
    titlu = models.CharField(max_length=1024, null=True, blank=True)
    descriere = models.TextField(null=True, blank=True)
    resolution_x = models.IntegerField(null=True, blank=True)
    resolution_y = models.IntegerField(null=True, blank=True)

    score = models.IntegerField(default=0)
    is_deleted = models.BooleanField()
    is_flagged = models.BooleanField()
    is_face_processed = models.BooleanField()

    published_status = models.IntegerField(default=2, choices=IMAGINE_PUBLISHED_STATUS, verbose_name=u"Vizibilitate")

    tags = TaggableManager()

    class Meta:
        verbose_name = u"Imagine"
        verbose_name_plural = u"Imagini"
        ordering = ["date_taken", ]

    def rotate(self, direction="cw"):
        im = Image.open(self.image)

        angle = -90
        if direction == "cw":
            angle = -90
        else:
            angle = 90

        im = im.rotate(angle)
        im.save("%s%s" % (MEDIA_ROOT, self.image))

        if os.path.exists(self.get_large_filename()):
            os.unlink(self.get_large_filename())
        if os.path.exists(self.get_thumbnail_filename()):
            os.unlink(self.get_thumbnail_filename())
        if os.path.exists(self.get_profile_filename()):
            os.unlink(self.get_profile_filename())

        return

    def get_day(self):
        #   compensation for (0, 3 AM) interval
        data = self.data
        ltime = datetime.time(data.hour, data.minute, data.second)
        magic_time = datetime.time(3, 0 ,0)
        if ltime < magic_time:
            data = self.data - datetime.timedelta(days = 1)
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
        return self.exifdata_set.filter(key__in=("Model", ))

    def save(self, *args, **kwargs):
        im = None
        if self.resolution_x is None or self.resolution_y is None:
            logger.debug("Imagine.save: opening file: %s" % os.path.join(MEDIA_ROOT, "%s" % self.image))
            im = Image.open(os.path.join(MEDIA_ROOT, "%s" % self.image))
            self.resolution_x, self.resolution_y = im.size

        on_create = False
        if self.id is None:
            on_create = True
            if im is None:
                im = Image.open(self.image)
            try:
                info = im._getexif()
            except Exception, e:
                info = None


            exif_data = {}

            #    get current EXIF data
            if info is not None:
                for tag, value in info.items():
                    from PIL import ExifTags

                    decoded = ExifTags.TAGS.get(tag, tag)
                    if decoded == u"Maker Note":
                        continue

                    if decoded == u"DateTimeOriginal":
                        self.data = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

                    exif_data[decoded] = value

        retval = super(Imagine, self).save(*args, **kwargs)

        if not self.is_face_processed:
            if not on_create:
                #    delete any existing faces, thus allowing detected face reset by
                #    switching the is_face_processed flag
                self.detectedface_set.all().delete()
            self.find_faces()
            self.is_face_processed = True

        if on_create:
            #    clear currently EXIF data
            self.exifdata_set.all().delete()

            for key, value in exif_data.items():
                exif = EXIFData(imagine=self, key=key, value=value)
                try:
                    exif.save()
                except Exception, e:
                    continue

        return retval

    def vote_photo(self, score):
        self.score += score
        self.save()

    def find_faces(self):
        import cv

        imcolor = cv.LoadImage("%s/%s" % (MEDIA_ROOT, self.image)) #@UndefinedVariable
        detectors = ["haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"]
        for detector in detectors:
            haarFace = cv.Load(os.path.join(STATIC_ROOT, detector))  # @UndefinedVariable
            storage = cv.CreateMemStorage() #@UndefinedVariable
            detectedFaces = cv.HaarDetectObjects(imcolor, haarFace, storage, min_size=(200, 200)) #@UndefinedVariable
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
            "titlu": u"%s - %s" % (self.set_poze.eveniment.nume, self.titlu),
            "descriere": self.descriere or "",
            "autor": self.set_poze.get_autor(),
            "data": self.data.strftime("%d %B %Y %H:%M:%S"),
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
    imagine = models.ForeignKey(Imagine)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = u"EXIFData"
        verbose_name_plural = u"EXIFData"

    def __unicode__(self):
        return "%s: %s" % (self.key, self.value)


FLAG_MOTIVES = (("personal", u"Sunt în poză și nu sunt de acord să apară aici"),
                ("ofensa", "Consider că poza este ofensatoare"),
                ("nonscout", "Poza conține un comportament necercetășesc și nu ar trebui listată aici"),
                ("calitateslaba", u"Poza este de calitate slabă și nu merită păstrată"),
                ("altul", "Alt motiv"))


class FlagReport(models.Model):
    imagine = models.ForeignKey(Imagine)
    motiv = models.CharField(max_length=1024, choices=FLAG_MOTIVES)
    alt_motiv = models.CharField(max_length=1024, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u"Raport poză"
        verbose_name_plural = u"Rapoarte poze"
        ordering = ["-timestamp", "motiv"]

    def __unicode__(self):
        return "Raport de %s la #%d (%s)" % (self.motiv, self.imagine.id, self.imagine.set_poze.eveniment)


class DetectedFace(models.Model):
    imagine = models.ForeignKey(Imagine)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()