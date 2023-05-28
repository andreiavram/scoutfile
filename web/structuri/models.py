#   coding: utf-8

from builtins import range
from builtins import object
import datetime
import json
import logging
from functools import partial

import unidecode
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.urls import reverse
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from patrocle.models import Credit
from patrocle.models import RezervareCredit
from photologue.models import ImageModel

from adrese_postale.adrese import AdresaPostala
from album.models import Imagine
from documente.models import DocumentCotizatieSociala
from documente.models import PlataCotizatieTrimestru, AsociereDocument, ChitantaCotizatie
from documente.models import Trimestru
from utils.models import FacebookSession

logger = logging.getLogger(__name__)
redis_cache = caches["redis"]


class RamuraDeVarsta(models.Model):
    nume = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    varsta_intrare = models.PositiveSmallIntegerField()
    varsta_iesire = models.PositiveSmallIntegerField(null=True, blank=True)
    culoare = models.CharField(max_length=255, null=True, blank=True)
    are_patrule = models.BooleanField(default=True)

    def __str__(self):
        return u"%s" % self.nume


class Structura(models.Model):
    class Meta(object):
        abstract = True

    nume = models.CharField(max_length=255)
    data_infiintare = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    def delete(self, **kwargs):
        AsociereMembruStructura.objects.filter(content_type=ContentType.objects.get_for_model(self),
                                               object_id=self.id).delete()

        return super(Structura, self).delete(**kwargs)

    def ocupant_functie(self, nume_functie=None):
        search_kwargs = dict(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id, tip_asociere__nume=nume_functie,
            moment_incheiere__isnull=True
        )
        cercetasi = AsociereMembruStructura.objects.filter(**search_kwargs).select_related("membru")
        if cercetasi.count():
            return cercetasi[0].membru

        return None

    def cercetasi(self, qs=False, tip_asociere=(u"Membru", u"Membru aspirant", u"Membru suspendat")):
        asociere = AsociereMembruStructura.objects.filter(content_type=ContentType.objects.get_for_model(self),
                                                          object_id=self.id,
                                                          moment_incheiere__isnull=True)
        asociere = asociere.select_related("membru", "tip_asociere", "content_type").prefetch_related("content_object")

        if isinstance(tip_asociere, list) or isinstance(tip_asociere, tuple):
            asociere = asociere.filter(tip_asociere__nume__in=tip_asociere)
        else:
            asociere = asociere.filter(tip_asociere__nume__iexact=tip_asociere)

        if qs:
            return asociere

        return [a.membru for a in asociere]

    def lideri(self, qs=False):
        return self.cercetasi(qs=qs, tip_asociere=["Lider", "Lider asistent"])

    def grad_colectare_cotizatie(self, trimestru=None):
        target_grp_total = self.cercetasi(qs=True).filter(moment_inceput__lte=trimestru.data_inceput).select_related("membru")
        target_grp = [a for a in target_grp_total if a.membru.plateste_cotizatie(trimestru)]
        realizat_cnt = PlataCotizatieTrimestru.objects.filter(trimestru=trimestru, final=True, membru__in=[a.membru for a in target_grp]).count()

        if len(target_grp) == 0:
            if target_grp_total.count():
                return 100
            return 0

        return realizat_cnt * 100. / len(target_grp)

    def grad_colectare_cotizatie_trimestrul_curent(self):
        return self.grad_colectare_cotizatie(trimestru=Trimestru.trimestru_pentru_data(datetime.datetime.now().date()))

    def grad_colectare_cotizatie_trimestrul_anterior(self):
        trimestru = Trimestru.trimestru_pentru_data(datetime.datetime.now().date())
        trimestru = Trimestru.objects.get(ordine_globala=trimestru.ordine_globala-1)
        return self.grad_colectare_cotizatie(trimestru=trimestru)


SPECIFIC_CENTRU_LOCAL = (("catolic", "Catolic"), ("marinaresc", u"Marinăresc"))
STATUT_JURIDIC_CENTRU_LOCAL = (("pj", u"Filală"), ("nopj", u"Sucursală"), ("gi", u"Grup de inițiativă"))
STATUT_DREPTURI_CENTRU_LOCAL = (
    ("depline", "Depline"), ("suspendat", "Suspendat"), ("propus_desfiintare", u"Propus spre desființare"),
    ("gi", "Grup de inițiativă"))
TIPURI_CORESPONDENTA_CENTRU_LOCAL = (("email", "Email"), ("posta", u"Poștă"))


def upload_to_centru_local_logo(instance, filename):
    return "cl/logo-{0}-{1}".format(instance.id, filename)


def upload_to_centru_local_antent(instance, filename):
    return "cl/antet-{0}-{1}".format(instance.id, filename)


class CentruLocal(Structura):
    class Meta(object):
        verbose_name = u"Centru Local"
        verbose_name_plural = u"Centre Locale"

        permissions = (
            ("list_centrulocal", u"Poate vedea o listă cu Centrele lui Locale"),
        )

    asocieri_membru = [u"Membru",]

    localitate = models.CharField(max_length=255)
    denumire = models.CharField(max_length=255, null=True, blank=True)
    specific = models.CharField(max_length=255, choices=SPECIFIC_CENTRU_LOCAL, null=True, blank=True)
    statut_juridic = models.CharField(max_length=255, choices=STATUT_JURIDIC_CENTRU_LOCAL, default="nopj")
    statut_drepturi = models.CharField(max_length=255, choices=STATUT_DREPTURI_CENTRU_LOCAL, default="depline")

    preferinte_corespondenta = models.CharField(max_length=255, choices=TIPURI_CORESPONDENTA_CENTRU_LOCAL,
                                                default="email", verbose_name=u"Preferință trimitere corespondență",
                                                help_text=u"Asigurați-vă că ați adăugat informațiile relevante de contact pentru tipul de corespondență ales.")

    moment_initial_cotizatie = models.ForeignKey("documente.Trimestru", null=True, blank=True, on_delete=models.SET_NULL)
    logo = models.ImageField(null=True, blank=True, upload_to=upload_to_centru_local_logo)
    antet = models.ImageField(null=True, blank=True, upload_to=upload_to_centru_local_antent)

    def nume_complet(self):
        if self.denumire is not None and self.denumire != "":
            return u"Centrul Local \"%s\" %s" % (self.denumire, self.localitate)
        return u"Centrul Local %s" % self.localitate

    def __str__(self):
        return u"%s" % self.nume_complet()

    def save(self, *args, **kwargs):
        self.nume = self.nume_complet()
        return super(CentruLocal, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("structuri:cl_detail", kwargs={"pk": self.id})

    def adeziuni_lipsa(self):
        cnt_membri = self.cercetasi(qs=True).count()
        cnt_adeziuni = AsociereDocument.objects.filter(content_type=ContentType.objects.get_for_model(Membru),
                                                       tip_asociere__nume__iexact="subsemnat",
                                                       document__tip_document__slug="adeziune",
                                                       document__registru__centru_local=self).count()
        return cnt_membri - cnt_adeziuni


class Unitate(Structura):
    class Meta(object):
        verbose_name = u"Unitate"
        verbose_name_plural = u"Unități"

    ramura_de_varsta = models.ForeignKey(RamuraDeVarsta, on_delete=models.CASCADE)
    centru_local = models.ForeignKey(CentruLocal, on_delete=models.CASCADE)

    def __str__(self):
        return u"Unitatea %s" % self.nume

    def patrule(self):
        return self.patrula_set.filter(activa=True, moment_inchidere__isnull=True)

    def patrule_inactive(self):
        return self.patrula_set.filter(activa=False, moment_inchidere__isnull=False)

    def total_membri_activi(self):
        return AsociereMembruStructura.objects.filter(content_type=ContentType.objects.get_for_model(self),
                                                      object_id=self.id,
                                                      tip_asociere__content_types__in=(
                                                          ContentType.objects.get_for_model(self), ),
                                                      tip_asociere__nume__icontains=u"Membru",
                                                      moment_inceput__isnull=False,
                                                      moment_incheiere__isnull=True).count()

    def get_absolute_url(self):
        return reverse("structuri:unitate_detail", kwargs={"pk": self.id})


class Patrula(Structura):
    class Meta(object):
        verbose_name = u"Patrulă"
        verbose_name_plural = u"Patrule"

    unitate = models.ForeignKey(Unitate, on_delete=models.CASCADE)
    moment_inchidere = models.DateField(null=True, blank=True)

    @property
    def ramura_de_varsta(self):
        return self.unitate.ramura_de_varsta

    @property
    def centru_local(self):
        return self.unitate.centru_local

    def __str__(self):
        return u"Patrula %s" % self.nume

    def get_absolute_url(self):
        return reverse("structuri:patrula_detail", kwargs={"pk": self.id})


class Echipa(Structura):
    class Meta:
        verbose_name = "Echipă"
        verbose_name_plural = "Echipe"

    centru_local = models.ForeignKey(CentruLocal, on_delete=models.CASCADE, related_name="echipe")


class Utilizator(models.Model):
    user = models.OneToOneField("auth.User", null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    nume = models.CharField(max_length=255)
    prenume = models.CharField(max_length=255)

    hash = models.CharField(max_length=32, null=True, blank=True, unique=True)
    timestamp_registered = models.DateTimeField(null=True, blank=True)
    timestamp_confirmed = models.DateTimeField(null=True, blank=True)
    timestamp_accepted = models.DateTimeField(null=True, blank=True)
    requested_password_reset = models.BooleanField(default=False)

    def nume_complet(self):
        return "%s %s" % (self.prenume.title(), self.nume.upper())

    def __str__(self):
        return self.nume_complet()

    def link_confirmare(self):
        return reverse("structuri:membru_confirm_registration", kwargs={"hash": self.hash})

    def facebook_connected(self):
        #   TODO: add expiration check on facebook session manager
        return FacebookSession.objects.filter(user=self.user).exists()


class ImagineProfil(ImageModel):
    def delete(self):
        self.image.delete()
        # if os.path.exists("%s%s" % (MEDIA_ROOT, self.image)):
        #     os.unlink("%s%s" % (MEDIA_ROOT, self.image))
        return super(ImagineProfil, self).delete()


class TipRelatieFamilie(models.Model):
    nume = models.CharField(max_length=255)
    reverse_relationship = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return u"%s" % self.nume


class PersoanaDeContact(models.Model):
    nume = models.CharField(max_length=255, null=True, blank=True)
    tip_relatie = models.ForeignKey(TipRelatieFamilie, null=True, blank=True, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    implicit = models.BooleanField(default=False)

    job = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"Profesie, loc de muncă")

    note = models.CharField(max_length=1024, null=True, blank=True)
    membru = models.ForeignKey("Membru", on_delete=models.CASCADE)


@receiver(post_save, sender=PersoanaDeContact)
def enforce_default(sender, instance, *args, **kwargs):
    if instance.implicit:
        for contact in PersoanaDeContact.objects.filter(membru=instance.membru, implicit=True).exclude(id=instance.id):
            contact.implicit = False
            contact.save()


class AsociereMembruFamilie(models.Model):
    tip_relatie = models.ForeignKey(TipRelatieFamilie, on_delete=models.CASCADE)
    persoana_sursa = models.ForeignKey("Membru", on_delete=models.CASCADE)
    persoana_destinatie = models.ForeignKey("Membru", related_name="membru_destinatie", on_delete=models.CASCADE)

    @classmethod
    def rude_cercetasi(cls, membru, exclude_self=False):
        """ Intoarce toate persoanele din familie, inclusiv persoana sursa
        
        Se poate folosi pentru calculul diferentiat al cotizatiilor, si a altor taxe
        """
        people = [membru, ]
        for person in people:
            for con in list(cls.objects.filter(Q(persoana_sursa=person) | Q(persoana_destinatie=person))):
                if con.persoana_sursa not in people:
                    people.append(con.persoana_sursa)
                if con.persoana_destinatie not in people:
                    people.append(con.persoana_destinatie)

        if exclude_self:
            people = [p for p in people if p != membru]
        return people


class Membru(Utilizator):
    CALITATI_SCUTITE_COTIZATIE = ("Membru inactiv", "Membru adult", "Alumnus")
    CALITATI_COMUNE = ["Membru suspendat", "Membru aspirant", "Membru inactiv", "Membru Consiliul Centrului Local",
                       "Lider", "Lider asistent", "Membru adult", "Șef Centru Local"]

    cnp = models.CharField(max_length=255, null=True, blank=True, verbose_name="CNP", unique=True)
    telefon = models.CharField(max_length=10, null=True, blank=True)
    adresa = models.CharField(max_length=2048, null=True, blank=True)
    data_nasterii = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=(("m", u"Masculin"), ("f", "Feminin")), null=True, blank=True)

    familie = models.ManyToManyField("self", through=AsociereMembruFamilie, symmetrical=False, blank=True)
    scout_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID ONCR")
    scor_credit = models.IntegerField(default=2, choices=((0, u"Rău"), (1, u"Neutru"), (2, u"Bun")), verbose_name=u"Credit", help_text=u"Această valoare reprezintă încrederea Centrului Local într-un membru de a-și respecta angajamentele financiare (dacă Centrul are sau nu încredere să pună bani pentru el / ea)")

    #TODO: find some smarter way to do this
    poza_profil = models.ForeignKey(ImagineProfil, null=True, blank=True, on_delete=models.SET_NULL)

    def __init__(self, *args, **kwargs):
        super(Membru, self).__init__(*args, **kwargs)
        self._plateste_cotizatie = {}
        self._afilieri = None

    def save(self, *args, **kwargs):
        """
        Asigură la salvare preluarea sexului și a datei nașterii din CNP
        Asigură menținerea centrulu local corect
        """
        #TODO: mută procesarea asta de aici într-o utilitate
        if self.data_nasterii is None:
            sufix_an = self.cnp[1:3]
            luna = self.cnp[3:5]
            ziua = self.cnp[5:7]

            if int(self.cnp[0]) in (1, 2):
                prefix_an = "19"
            elif int(self.cnp[0]) in (5, 6, 7, 8):
                prefix_an = "20"
            else:
                prefix_an = "19"

            self.data_nasterii = datetime.date(year=int("%s%s" % (prefix_an, sufix_an)), month=int(luna), day=int(ziua))

        if self.sex is None:
            if int(self.cnp[0]) % 2 == 0:
                self.sex = "f"
            else:
                self.sex = "m"

        return super(Membru, self).save(*args, **kwargs)

    def create_structuri_cache(self):
        db_data = self.afilieri.all().select_related("tip_asociere").prefetch_related("tip_asociere__content_types")
        data = []
        for item in db_data:
            data.append({
                "id": item.id,
                "membru_id": item.membru_id,
                "content_type": item.content_type_id,
                "object_id": item.object_id,
                "tip_asociere": item.tip_asociere_id,
                "tip_asociere_ctypes": [ctype.id for ctype in item.tip_asociere.content_types.all()],
                "tip_asociere_nume": item.tip_asociere.nume,
                "moment_inceput": item.moment_inceput.strftime("%d.%m.%Y %H:%M:%S") if item.moment_inceput else None,
                "moment_incheiere": item.moment_incheiere.strftime("%d.%m.%Y %H:%M:%S") if item.moment_incheiere else None,
            })

        self.save_to_cache("asocieri", json.dumps(data), timeout=60 * 60 * 24 * 31)
        return data

    def load_structuri_from_cache(self):
        cached_asocieri = self.get_from_cache("asocieri")
        if cached_asocieri is None:
            asocieri_json = self.create_structuri_cache()
        else:
            asocieri_json = json.loads(cached_asocieri)

        for item in asocieri_json:
            item['moment_inceput'] = datetime.datetime.strptime(item['moment_inceput'], "%d.%m.%Y %H:%M:%S") if item['moment_inceput'] else None
            item['moment_incheiere'] = datetime.datetime.strptime(item['moment_incheiere'], "%d.%m.%Y %H:%M:%S") if item['moment_incheiere'] else None

        self._afilieri = asocieri_json


    @property
    def adresa_postala(self):
        adresa = self.get_contact(u"Adresa corespondență")
        return adresa if adresa is not None else self.adresa

    @property
    def mobil(self):
        mobil = self.get_contact(u"Mobil")
        return mobil if mobil is not None else self.telefon

    def get_contact(self, key, just_value=True):
        key_filters = dict(content_type=ContentType.objects.get_for_model(self), object_id=self.id,
                           tip_informatie__nume__iexact=key, tip_informatie__relevanta="Membru")

        data = InformatieContact.objects.filter(**key_filters)
        if data.count() == 0:
            return None
        if just_value:
            return data[0].valoare
        return data

    @property
    def centru_local(self):
        return self.get_centru_local()

    @staticmethod
    def get_afilieri_filter(item, trimestru, content_type_structura=None, rol=None, membru=None, structura=None):
        if not isinstance(rol, (list, tuple)):
            rol = [rol, ]

        conditions = [
            item.get('content_type') != content_type_structura.id,
            content_type_structura.id not in item.get('tip_asociere_ctypes'),
            item.get('tip_asociere_nume') not in rol,
        ]

        if membru:
            conditions.append(item.get('membru_id') != membru.id)

        if structura:
            conditions.append(item.get('object_id') != structura.id)

        if trimestru is None:
            conditions += [
                item.get('moment_inceput') is None,
                item.get('moment_incheiere') is not None
            ]
        else:
            conditions += [
                item.get('moment_incheiere') is not None and (datetime.date(item.get('moment_incheiere')) < trimestru.data_inceput),
                item.get('moment_inceput') is not None and (datetime.date(item.get('moment_inceput')) > trimestru.data_sfarsit)
            ]

        if any(conditions):
            return False
        return True

    def get_structura(self, qs=False, rol=(u"Membru", ), single=True, structura_model=None, trimestru=None):
        if self.is_lider and not single:
            rol = list(rol) + [u"Lider", u"Lider asistent"]

        if self._afilieri is None:
            self.load_structuri_from_cache()

        content_type_structura = ContentType.objects.get_for_model(structura_model)

        filter_asocieri = partial(
            Membru.get_afilieri_filter,
            trimestru=trimestru,
            content_type_structura=content_type_structura,
            rol=rol,
            membru=self
        )

        afilieri = list(filter(filter_asocieri, self._afilieri))
        afilieri.sort(key=lambda item: item.get("moment_inceput"), reverse=True)

        if len(afilieri) == 0:
            return None

        results = {
            (True, True): AsociereMembruStructura.objects.get(pk=afilieri[0].get('id')),
            (True, False): AsociereMembruStructura.objects.filter(pk__in=[a.get('id') for a in afilieri]),
            (False, True): AsociereMembruStructura.objects.get(pk=afilieri[0].get('id')).content_object,
            (False, False): structura_model.objects.filter(id__in=[a.get("object_id") for a in afilieri])
        }

        return results[(qs, single)]

        # kwargs = {"content_type": content_type_structura,
        #           "tip_asociere__nume__in": rol,
        #           "tip_asociere__content_types__in": (content_type_structura, ),
        #           "membru": self}
        #
        # asocieri = AsociereMembruStructura.objects.filter(**kwargs).order_by("-moment_inceput")
        #
        # if trimestru is None:
        #     asocieri = asocieri.filter(moment_inceput__isnull=False, moment_incheiere__isnull=True)
        # else:
        #     asocieri = asocieri.filter(Q(moment_incheiere__isnull=True) | Q(moment_incheiere__gte=trimestru.data_inceput))
        #     asocieri = asocieri.filter(moment_inceput__lte=trimestru.data_sfarsit)
        #
        # if asocieri.exists():
        #     #   switch on qs, single
        #     results = {
        #         (True, True): asocieri[0],
        #         (True, False): asocieri,
        #         (False, True): asocieri[0].content_object,
        #         (False, False): structura_model.objects.filter(id__in=asocieri.values_list("object_id", flat=True).all())
        #     }
        #     return results[(qs, single)]
        #
        # return None
    
    def get_centru_local(self, qs=False, rol=(u"Membru", ), single=True, trimestru=None):
        return self.get_structura(qs=qs, rol=rol, single=single, structura_model=CentruLocal, trimestru=trimestru)

    def get_unitate(self, qs=False, rol=(u"Membru", ), single=True, trimestru=None):
        return self.get_structura(qs=qs, rol=rol, single=single, structura_model=Unitate, trimestru=trimestru)

    def get_patrula(self, qs=False, rol=(u"Membru", ), single=True, trimestru=None):
        return self.get_structura(qs=qs, rol=rol, single=single, structura_model=Patrula, trimestru=trimestru)

    def get_unitati(self, qs=False, rol=(u"Membru", ), trimestru=None):
        return self.get_unitate(qs=qs, rol=rol, single=False, trimestru=trimestru)

    def get_patrule(self, qs=False, rol=(u"Membru", ), trimestru=None):
        return self.get_patrula(qs=qs, rol=rol, single=False, trimestru=trimestru)

    def get_centre_locale_permise(self):
        if self.user.groups.filter(name__iexact=u"Administratori sistem").count():
            return CentruLocal.objects.all()
        return [self.centru_local, ]

    def are_calitate(self, calitate, structura, trimestru=None, qs=False):
        """ determina daca membrul are o calitate intr-un din structurile locale (Centru Local, Unitate, Patrula)
        determinarea se face pentru un trimestru, implicit fiind cel din ziua curenta
        metoda ar trebui sa fie folosita oriunde se incearca determinari de apartenente si calitati
        """
        if isinstance(calitate, (list, tuple)):
            calitate = [calitate, ]

        if not structura:
            return AsociereMembruStructura.objects.none() if qs else False

        if self._afilieri is None:
            self.load_structuri_from_cache()

        content_type_structura = ContentType.objects.get_for_model(structura)


        filter_asocieri = partial(
            Membru.get_afilieri_filter,
            trimestru=trimestru,
            content_type_structura=content_type_structura,
            rol=calitate,
            structura=structura
        )

        afilieri = list(filter(filter_asocieri, self._afilieri))
        return self.afilieri.filter(id__in = [a.id for a in afilieri]) if qs else len(afilieri) != 0

        #
        # ams_filter = dict(content_type=ContentType.objects.get_for_model(structura),
        #                   object_id=structura.id,
        #                   tip_asociere__content_types__in=(ContentType.objects.get_for_model(structura), ),
        #                   tip_asociere__nume__in=calitate,
        #                   membru=self)
        #
        # asocieri = AsociereMembruStructura.objects.filter(**ams_filter)
        # if trimestru is None:
        #     asocieri = asocieri.filter(moment_inceput__isnull=False, moment_incheiere__isnull=True)
        # else:
        #     asocieri = asocieri.filter(Q(moment_incheiere__isnull=True) | Q(moment_incheiere__gte=trimestru.data_inceput))
        #     asocieri = asocieri.filter(moment_inceput__lte=trimestru.data_sfarsit)
        #
        # if qs:
        #     return asocieri
        # return asocieri.count() != 0

    def _proprietati_comune(self):
        if hasattr(self, "_proprietati") and self._proprietati is not None:
            return self._proprietati

        _proprietati = self.get_from_cache("proprietati")
        if _proprietati:
            self._proprietati = _proprietati
            return _proprietati

        if not hasattr(self, "_proprietati") or self._proprietati is None:
            self._proprietati = {}
            for calitate in self.CALITATI_COMUNE:
                self._proprietati[calitate] = False

            if self.centru_local:
                calitati = list(self.are_calitate(self.CALITATI_COMUNE, self.centru_local, qs=True).select_related("tip_asociere"))

                for calitate in calitati:
                    self._proprietati[calitate.tip_asociere.nume] = True

        self.save_to_cache("proprietati", self._proprietati)
        return self._proprietati

    def get_home_link(self):
        if self.is_lider():
            unitate = self.get_unitate(rol=(u"Lider", u"Lider asistent"))
            if unitate:
                return reverse("structuri:unitate_detail", kwargs={"pk": unitate.id})
            return reverse("structuri:cl_detail", kwargs={"pk": self.centru_local.id})
        return reverse("structuri:membru_profil")

    def afilieri_curente(self, end_chain=True, **kwargs):
        qs = self.afilieri.filter(moment_incheiere__isnull=True)
        if end_chain:
            qs = qs.order_by("-moment_inceput")

        return qs

    def afilieri_trecute(self, end_chain=True, **kwargs):
        qs = self.afilieri.filter(moment_incheiere__isnull=False)
        if end_chain:
            qs = qs.order_by("moment_incheiere")
        return qs

    def get_ramura_de_varsta(self, slug=False, moment=None):
        if self.is_lider_generic():
            if slug:
                return "lideri"
            return "Lider"

        trimestru = None
        if moment:
            trimestru = Trimestru.trimestru_pentru_data(moment)

        unitate = self.get_unitate(trimestru=trimestru)
        if unitate:
            rdv = self.get_unitate(trimestru=trimestru).ramura_de_varsta
            if slug:
                return rdv.slug
            return rdv.nume
        return None

    def asociaza(self, rol, structura, data_start=None, data_end=None, confirmata=False, user=None):
        tip_asociere, created = TipAsociereMembruStructura.objects.get_or_create(nume__iexact=rol, content_types__in=[ContentType.objects.get_for_model(structura)])
        if created:
            tip_asociere.save()
            tip_asociere.content_types.add(ContentType.objects.get_for_model(structura))

        asociere = AsociereMembruStructura(membru=self,
                                           content_type=ContentType.objects.get_for_model(structura),
                                           object_id=structura.id,
                                           tip_asociere=tip_asociere,
                                           moment_inceput=data_start,
                                           moment_incheiere=data_end)
        asociere.save()
        if confirmata:
            asociere.confirma(user)
        return asociere

    def get_badges_rdv(self):
        badges = self.get_from_cache("badges_rdv")
        badges = json.loads(badges if badges else "[]")

        if badges:
            return badges

        if self.is_lider_generic():
            badges.append("lider")
        else:
            unitate = self.get_unitate()
            if unitate:
                badges.append(unidecode.unidecode(unitate.ramura_de_varsta.nume.lower()))
        self.save_to_cache("badges_rdv", json.dumps(badges))
        return badges

    def get_extra_badges(self):
        badges = self.get_from_cache("badges_extra")
        badges = json.loads(badges if badges else "[]")

        if badges:
            return badges

        if self.is_sef_centru():
            badges.append("sef-centru")
        if self.is_membru_ccl():
            badges.append("membru-ccl")

        self.save_to_cache("badges_extra", json.dumps(badges))
        return badges

    def get_absolute_url(self):
        return reverse("structuri:membru_detail", {"pk": self.id})

    #    Patrocle specific code
    def rezerva_credit(self):
        credit = Credit.objects.filter(content_type=ContentType.objects.get_for_model(CentruLocal),
                                       object_id=self.centru_local.id,
                                       epuizat=False).order_by("timestamp")
        if credit.count() == 0:
            return False

        credit = credit[0]

        if credit.credit_disponibil() > 0:
            rezervare = RezervareCredit(credit=credit, content_type=ContentType.objects.get_for_model(self),
                                        object_id=self.id)
            rezervare.save()

        return True

    def elibereaza_credit(self):
        rezervari = RezervareCredit.objects.filter(content_type=ContentType.objects.get_for_model(self),
                                                   object_id=self.id)
        if rezervari.count() == 0:
            return False
        rezervare = rezervari[0]
        credit = rezervare.credit
        rezervare.delete()
        return credit

    def can_sms(self, membru):
        allowed = True
        if membru.get_centru_local() != self.centru_local:
            allowed = False
        if self.afilieri_curente().filter(content_type=ContentType.objects.get_for_model(CentruLocal),
                                          object_id=self.centru_local.id,
                                          tip_asociere__nume=u"Lider").count() == 0:
            allowed = False

        return allowed

    def informatie_contact(self, tip):
        data = InformatieContact.objects.filter(content_type=ContentType.objects.get_for_model(self),
                                                object_id=self.id,
                                                tip_informatie__nume__iexact=tip)
        if not data.count():
            return None

        return data

    def clear_cache(self, index_category):
        mapping = {
            "asociere": ["trimestru_initial", "proprietati", "badges_rdv"],
            "cotizatie_sociala": ["are_cotizatie_sociala", "status_cotizatie", "necesar_cotizatie"],
            "cotizatie": ["status_cotizatie", "necesar_cotizatie"],
            "asocieri": ["asocieri"]
        }
        to_clear = mapping.get(index_category, None)
        if to_clear is not None:
            for idx in to_clear:
                redis_cache.delete("m:%d:%s" % (self.id, idx))

    def get_from_cache(self, index):
        val = redis_cache.get("m:%d:%s" % (self.id, index))
        return val

    def save_to_cache(self, index, value, timeout=60 * 60 * 24 * 30):
        redis_cache.delete(f"m:{self.id}:{index}")
        return redis_cache.set(f"m:{self.id}:{index}", value, timeout)

    #    Cotizatie specific code
    def get_trimestru_initial_cotizatie(self):
        """ Obtine primul trimestu din care acest membru ar trebui sa plateasca cotizatie.
        Acesta este dependent de data inscrierii (pentru membri inscrisi dupa momentul 0
        al centrului local) sau este momentul 0 al centrului local (pentru cei inscrisi pana 
        la momentul 0)
        """
        stored_value = self.get_from_cache("trimestru_initial")
        if stored_value:
            return Trimestru.objects.get(id=stored_value)

        #    in mod necesar membrul are macar un centru local asociat
        #    calitatea de membru in ONCR se intampla prin intermediul Centrelor Locale
        filter_kwargs = {"content_type": ContentType.objects.get_for_model(CentruLocal)}
        afilieri = self.afilieri.filter(**filter_kwargs).order_by("moment_inceput")
        if not afilieri.count():
            raise ValueError(u"Cercetașul cu ID-ul %d nu are niciun Centru Local asociat" % self.id)

        moment_initial_membru = afilieri[0].moment_inceput

        trimestru_membru = Trimestru.trimestru_pentru_data(moment_initial_membru)
        if moment_initial_membru != trimestru_membru.data_inceput:
            trimestru_membru = Trimestru.urmatorul_trimestru(trimestru_membru)

        trimestru_centru = self.centru_local.moment_initial_cotizatie

        return_value = max(trimestru_membru, trimestru_centru, key=lambda x: x.ordine_globala)
        self.save_to_cache("trimestru_initial", return_value.id)
        return return_value

    def are_cotizatie_sociala(self, trimestru=None):
        """ Intoarce True daca membrul este in situatia de a plati cotizatie sociala
            Cotizatia sociala e o problema care poate varia în timp (se poate renunța la ea sau poate
            exista la o vreme după ce membrul este deja plătitor de cotizație, deci este necesar de știut despre
            ce trimestru este vorba.
        """

        stored_value = self.get_from_cache("are_cotizatie_sociala")
        if stored_value:
            return stored_value

        filtru_documente = {"content_type": ContentType.objects.get_for_model(self),
                            "object_id": self.id,
                            "document_ctype": ContentType.objects.get_for_model(DocumentCotizatieSociala),
                            "document__documentcotizatiesociala__este_valabil": True}

        qs = AsociereDocument.objects.filter(**filtru_documente)

        if trimestru is None:
            trimestru = Trimestru.trimestru_pentru_data(datetime.date.today())

        qs = qs.filter(Q(document__documentcotizatiesociala__valabilitate_end__isnull=True) | Q(document__documentcotizatiesociala__valabilitate_end__gte=trimestru.data_inceput))
        qs = qs.filter(document__documentcotizatiesociala__valabilitate_start__lte=trimestru.data_sfarsit)

        return_value = qs.count() != 0
        self.save_to_cache("are_cotizatie_sociala", return_value)
        return return_value

    def aplica_reducere_familie(self, valoare, trimestru):
        """ Aplica reducerea de familie pentru cotizatie
        """

        if self.are_cotizatie_sociala(trimestru=trimestru):
            return valoare

        familie = AsociereMembruFamilie.rude_cercetasi(self, exclude_self=True)
        #   exclude de la reducerea de membrii de familie membrii de familie care au cotizatie sociala trimestrul asta
        familie = [m for m in familie if not m.are_cotizatie_sociala(trimestru)]

        #   principiul este ca reducerea se aplica doar dupa ce se fac plati complete, nu si partiale
        #   problema care poate aparea este ca exista plati partiale care trebuie reconsiderate dupa efectuarea unei
        #   plati finale, ceea ce inseamna redistribuirea sumei respective

        #   in recalcularea cotizatiei pentru membrul familiei care plateste mai mult, se vor gasi plati finale
        #   efectuate, dar pentru sumele mai mici, ceea ce inseamna ca cotizatia intoarsa va fi si ea redusa, lucru
        #   eronat. Pentru a evita aceasta situatie, nu doar numarul platilor finale, ci si cuantumul lor trebuie
        #   determinat

        #   afla care sunt membrii familiei care au plati considerate finale
        filter_kwargs = dict(trimestru=trimestru, membru__in=familie, tip_inregistrare="normal")

        plati = PlataCotizatieTrimestru.objects.filter(**filter_kwargs).select_related("membru")

        #   ne intereseaza doar platile facute de membrii care au si plati finale (pentru fiecare trimestru fiecare
        #   membru poate avea o singura plata finala)

        membri_plati_finale = plati.filter(final=True).values_list("membru", flat=True)
        plati_relevante = plati.filter(membru__id__in=membri_plati_finale)
        #   pentru fiecare membru cu plati finale, calculeaza ce plata are facuta
        plati_membri_familie = []
        for m in membri_plati_finale:
            suma_membru = plati_relevante.filter(membru__id = m).aggregate(Sum("suma")).get("suma__sum", 0)
            plati_membri_familie.append((m, suma_membru))

        platitori_cnt = len(plati_membri_familie)
        plati_membri_familie.sort(key=lambda p: p[1], reverse=True)

        quotas = {0: 1, 1: 0.5, 2: 0.25}
        plata_index = 0
        if len(plati_membri_familie):
            for q in list(quotas.items()):
                logger.debug(u"aplica_reducere_familie, verific existență cotizație %s pentru %s, trimestrul %s" % (q[1], self, trimestru))
                found = False

                if valoare * q[1] == plati_membri_familie[plata_index][1]:
                    found = True
                    plata_index += 1

                if found is False or plata_index > len(plati_membri_familie) - 1:
                    break

        quota = quotas.get(plata_index, 0.25)
        return valoare * quota

    def _status_cotizatie(self, force_real=False):
        """ Cotizatia se poate plati pana pe 15 a ultimei luni din trimestru
        """

        stored_value = self.get_from_cache("status_cotizatie")
        if stored_value and not force_real:
            return stored_value

        pct = PlataCotizatieTrimestru.objects.filter(membru=self, final=True).order_by("-trimestru__ordine_globala")[0:1]
        nothing = False
        if pct.count():
            ultimul_trimestru = pct[0].trimestru
        else:
            ultimul_trimestru = self.get_trimestru_initial_cotizatie()
            nothing = True

        today = datetime.date.today()
        trimestru_curent = Trimestru.trimestru_pentru_data(today)

        # -1 vine de la faptul ca cotizatia se plateste in urma, nu in avans, deci trimestrul curent
        # se plateste dupa ce se termina
        diferenta_trimestre = trimestru_curent.ordine_globala - ultimul_trimestru.ordine_globala - 1
        if nothing:
            diferenta_trimestre += 1

        # UPDATED: cotizatia se plateste in urma, dar deadline-ul oficial al Centrului Local este 15 a ultimei luni
        # a trimestrului curent
        if today > (trimestru_curent.data_sfarsit - datetime.timedelta(days=15)):
            diferenta_trimestre += 1

        # daca suntem in perioada de gratie de doua saptamani de la inceputul trimestrului, nici trimestrul
        # trecut nu conteaza
        # UPDATED: perioada de gratie este o chestiune care tine doar de ONCR, la nivel local,
        # nu exista perioada de gratie
        #if not trimestru_curent.data_in_trimestru(today - datetime.timedelta(days = 15)):
        #    diferenta_trimestre -= 1
        trimestru = ultimul_trimestru
        #   schimbat aici pentru a nu mai folosi un loop
        trimestre_scutite = self._trimestre_scutite(trimestru, trimestru_curent)

        diferenta_trimestre -= trimestre_scutite

        return_value = diferenta_trimestre, trimestru_curent, ultimul_trimestru
        self.save_to_cache("status_cotizatie", return_value)
        return return_value

    def _trimestre_scutite(self, trimestru_start, trimestru_end):
        start = trimestru_start.ordine_globala
        end = trimestru_end.ordine_globala
        trimestre = list(range(start, end + 1))

        ctype_centru_local = ContentType.objects.get_for_model(CentruLocal)
        ams_filter = dict(content_type=ctype_centru_local,
                          object_id=self.centru_local.id,
                          tip_asociere__content_types__in=(ctype_centru_local, ),
                          tip_asociere__nume__in=self.CALITATI_SCUTITE_COTIZATIE,
                          membru=self,)

        asocieri = AsociereMembruStructura.objects.filter(**ams_filter)
        if not asocieri.exists():
            return 0

        scutite = 0
        for a in asocieri:
            t_start = Trimestru.trimestru_pentru_data(a.moment_inceput)
            if a.moment_incheiere is None:
                de_scutit = set(range(t_start.ordine_globala, end + 1))
            else:
                t_end = Trimestru.trimestru_pentru_data(a.moment_incheiere)
                de_scutit = set(range(t_start.ordine_globala, t_end.ordine_globala + 1))
            scutite += len(list(set.intersection(de_scutit, set(trimestre))))
            trimestre = set.difference(set(trimestre), de_scutit)

        return scutite

    def status_cotizatie(self, for_diff=None):
        if for_diff is None:
            status, curent, ultimul = self._status_cotizatie()
        else:
            status = for_diff

        trimestru_string = "trimestre" if abs(status) > 1 else "trimestru"
        if status > 0:
            return u"în urmă cu %d %s" % (abs(status), trimestru_string)
        if status == 0:
            return u"la zi"
        if status < 0:
            return u"avans pentru %d %s" % (abs(status), trimestru_string)

    def get_ultimul_trimestru_cotizatie(self, return_plati_partiale=False):
        # TODO: dacă membrul este alumn sau inactiv pentru o anumită perioadă, atunci el nu plătește cotizație
        # TODO: perioadele de inactivitate se pot interacala in perioade de activitate, cazuri care trebuie luate in
        #  considerare
        plati_membru = self.platacotizatietrimestru_set.all().order_by("-trimestru__ordine_globala", "-index")
        plati_partiale = None
        if plati_membru.count() == 0:
            trimestru_initial = self.get_trimestru_initial_cotizatie()
        elif plati_membru[0].partial and not plati_membru[0].final:
            trimestru_initial = plati_membru[0].trimestru
            plati_partiale = self.platacotizatietrimestru_set.filter(trimestru=trimestru_initial)
        else:
            trimestru_initial = Trimestru.urmatorul_trimestru(plati_membru[0].trimestru)

        #   daca membrul este in categorii speciale care sunt scutite de la plata cotizatiei, atunci:
        #   - daca asocierea e in continuare activa, membrul nu datoreaza cotizatie
        #   - daca membrul s-a intors la statutul de membru activ, atunci datoreaza cotizatie pe ultima
        #   perioada de activitate

        afilieri_scutite = self.are_calitate(self.CALITATI_SCUTITE_COTIZATIE, self.centru_local, trimestru=trimestru_initial, qs=True)
        if afilieri_scutite.filter(moment_incheiere__isnull=True).exists():
            trimestru_initial = Trimestru.urmatorul_trimestru(Trimestru.trimestru_pentru_data(datetime.date.today()))

        afilieri_scutite = afilieri_scutite.order_by("-moment_incheiere")
        if afilieri_scutite.exists():
            trimestru_initial = Trimestru.urmatorul_trimestru(Trimestru.trimestru_pentru_data(afilieri_scutite[0].moment_incheiere))

        if return_plati_partiale:
            return trimestru_initial, plati_partiale
        return trimestru_initial

    def calculeaza_necesar_cotizatie(self, force_real=False):
        necesar_cotizatie = self.get_from_cache("necesar_cotizatie")
        if necesar_cotizatie and not force_real:
            return float(necesar_cotizatie)

        necesar_cotizatie = PlataCotizatieTrimestru.calculeaza_necesar(membru=self)
        self.save_to_cache("necesar_cotizatie", necesar_cotizatie)
        return necesar_cotizatie

    def recalculeaza_acoperire_cotizatie(self, trimestru_start=None, membri_procesati=[], reset=False):
        chitanta_partial = False
        pct_filter = dict(membru=self, chitanta__printata=False, chitanta__blocat=False)
        if trimestru_start:
            pct_filter['trimestru__ordine_globala__gte'] = trimestru_start.ordine_globala
            chitanta_partial = True
        pcts = PlataCotizatieTrimestru.objects.filter(**pct_filter)

        if pcts.count() == 0:
            chitante_cotizatie = ChitantaCotizatie.pentru_membru(membru=self)
            chitante_cotizatie = [c.id for c in chitante_cotizatie]
        else:
            chitante_cotizatie = pcts.order_by("trimestru__ordine_globala").values_list("chitanta", flat=True).order_by().distinct()
        chitante_cotizatie = list(ChitantaCotizatie.objects.filter(id__in=chitante_cotizatie))
        pcts.delete()

        if reset:
            return

        logger.debug("recalculeaza_acoperire_cotizatie: Chitante %s" % chitante_cotizatie)

        membri_procesati.append(self)
        for chitanta in chitante_cotizatie:
            logger.debug("recalculeaza_acoperire_cotizatie: procesez document %s %s" % (self, chitanta))
            PlataCotizatieTrimestru.calculeaza_acoperire(self, chitanta, chitanta.suma, chitanta_partial=chitanta_partial, commit=True, membri_procesati=membri_procesati)

    def status_cotizatie_numeric(self):
        status, curent, ultimul = self._status_cotizatie()
        return int(status)

    def are_adeziune(self):
        return self.adeziune(qs=True).exists()

    def adeziune(self, qs=False):
        search = {"document__tip_document__slug": "adeziune",
                  "tip_asociere__slug": "subsemnat",
                  "content_type": ContentType.objects.get_for_model(self),
                  "object_id": self.id}

        asociere = AsociereDocument.objects.filter(**search)
        if qs:
            return asociere
        if asociere.exists():
            return asociere.first().document
        return None

    def is_aspirant(self):
        return self._proprietati_comune().get("Membru aspirant", False)

    def is_suspendat(self):
        return self._proprietati_comune().get("Membru suspendat", False)

    def is_inactiv(self):
        return self._proprietati_comune().get("Membru inactiv", False)

    def is_adult(self):
        return self._proprietati_comune().get("Membru adult", False)

    def is_lider(self):
        return self._proprietati_comune().get("Lider", False)

    def is_alumnus(self):
        return self._proprietati_comune().get("Alumnus", False)

    def is_lider_asistent(self):
        return self._proprietati_comune().get("Lider asistent", False)

    def is_lider_generic(self):
        return self.is_lider() or self.is_lider_asistent()

    def is_membru_ccl(self):
        return self._proprietati_comune().get("Membru Consiliul Centrului Local", False)

    def drept_vot(self):
        #   are drept vot si nu e suspendat pe baza de cotizatie
        drept_vot_teoretic = self.drept_vot_teoretic()
        cotizatie_condition = self._status_cotizatie()[0] <= 1
        return drept_vot_teoretic and cotizatie_condition and (not self.is_suspendat())

    def drept_vot_teoretic(self, date=None):
        #   are minim 16 ani la data evenimentului si are promisiunea depusa
        if date is None:
            date = datetime.date.today()
        age_condition = date.year - self.data_nasterii.year - ((date.month, date.day) < (self.data_nasterii.month, self.data_nasterii.day)) >= 16
        membership_condition = not self.is_aspirant() and not self.is_adult() and not self.is_inactiv()
        return age_condition and membership_condition

    def is_sef_centru(self):
        return self._proprietati_comune().get("Șef Centru Local", False)

    def plateste_cotizatie(self, trimestru=None):
        """ determina daca un membru plateste sau nu cotizatie
        din notele de implementare curente, neplatitori de cotizatie pentru un anumit trimestru sunt
        1) membrii inactivi, marcati ca atare
        2) membrii adulti, marcati ca atare si membrii api unei unitati de adulti
        toate celalalte categorii de membrii sunt platitori de cotizatie
        """

        if trimestru is None:
            trimestru = Trimestru.trimestru_pentru_data(datetime.date.today())

        if trimestru.ordine_globala in self._plateste_cotizatie:
            return self._plateste_cotizatie[trimestru.ordine_globala]

        #   daca exista o relatie de scutire de cotizatie care nu e inca inchisa, putem prepopula de la primul apel
        #   pentru toate trimestrele pana la cel curent relevante
        if self.is_adult() or self.is_inactiv() or self.is_alumnus():
            qs = self.are_calitate(self.CALITATI_SCUTITE_COTIZATIE, self.centru_local, qs=True)
            asociere_deschisa = qs.filter(moment_incheiere__isnull=True).first()
            if asociere_deschisa:
                trimestru_end = Trimestru.trimestru_pentru_data(datetime.date.today()).ordine_globala
                trimestru_curent = Trimestru.trimestru_pentru_data(asociere_deschisa.moment_inceput).ordine_globala
                self._plateste_cotizatie.update({k: False for k in range(trimestru_curent, trimestru_end + 1)})

                if trimestru.ordine_globala in self._plateste_cotizatie:
                    return self._plateste_cotizatie[trimestru.ordine_globala]

        if self.are_calitate(self.CALITATI_SCUTITE_COTIZATIE, self.centru_local, trimestru=trimestru):
            self._plateste_cotizatie[trimestru.ordine_globala] = False
            return False

        self._plateste_cotizatie[trimestru.ordine_globala] = result = True
        return result

    @property
    def oncr_status(self):
        if self.scout_id is None:
            return None

        oncr_data = self.get_from_cache("oncr_feegood"), self.get_from_cache("oncr_lastpaidquarter")

        if oncr_data[0] is None and oncr_data[1] is None:
            return None

        return oncr_data


class TipAsociereMembruStructura(models.Model):
    """
    Tipuri asociere membru la structura. Spre exemplu, un cercetas intr-un centru local este membru,
        sau alumni, in Consiliul Centrului Local este responsabil pe un anumit domeniu samd
        """
    nume = models.CharField(max_length=255)
    content_types = models.ManyToManyField(ContentType, blank=True)

    def __str__(self):
        return u"%s" % self.nume


class AsocierePublicManager(models.Manager):
    def get_queryset(self):
        return super(AsocierePublicManager, self).get_queryset().filter(confirmata=True)


ordine_structuri = {u"Patrulă": u"Unitate", u"Unitate": u"Centru Local"}
campuri_structuri = {u"Patrulă": u"Unitate", u"Unitate": u"centru_local"}


class AsociereMembruStructura(models.Model):
    membru = models.ForeignKey(Membru, related_name="afilieri", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, verbose_name=u"Tip structură", on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=u"Structură")
    content_object = GenericForeignKey()

    tip_asociere = models.ForeignKey(TipAsociereMembruStructura, on_delete=models.CASCADE)

    moment_inceput = models.DateTimeField(null=True, blank=True)
    moment_incheiere = models.DateTimeField(null=True, blank=True)

    confirmata = models.BooleanField(default=False)
    confirmata_pe = models.DateTimeField(null=True, blank=True)
    confirmata_de = models.ForeignKey(Utilizator, null=True, blank=True, related_name="asocieri_confirmate", on_delete=models.SET_NULL)

    objects = AsocierePublicManager()
    all_objects = models.Manager()

    def __str__(self):
        return u"%s - %s - %s" % (self.membru, self.tip_asociere, self.content_object)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.membru.create_structuri_cache()

    def get_structura(self, ctype):
        lookups = {"centrulocal": {"centrulocal": lambda: self.content_object},
                   "unitate": {"centrulocal": lambda: self.content_object.centru_local,
                               "unitate": lambda: self.content_object},
                   "patrula": {"centrulocal": lambda: self.content_object.unitate.centru_local,
                               "unitate": lambda: self.content_object.unitate,
                               "patrula": lambda: self.content_object}}

        if self.content_type.model not in list(lookups.keys()):
            return None

        if ctype.model not in lookups.get(self.content_type.model):
            return None

        return lookups.get(self.content_type.model).get(ctype.model)()

    def confirma(self, user):
        self.confirmata = True
        self.confirmata_pe = datetime.datetime.now()
        self.confirmata_de = user
        self.save()

    def documents(self):
        return AsociereDocument.objects.filter(
            content_object=ContentType.objects.get_for_model(self),
            object_id=self.id
        )

#    def save(self, *args, **kwargs):
#        retval = super(AsociereMembruStructura, self).save(*args, **kwargs)
#
#        if self.content_type.name in ordine_structuri.keys():
#            content_type = self.content_type
#            while content_type != None:
#                try:
#                    content_type = ContentType.objects.get(name = ordine_structuri.get(content_type.name))
#                except Exception, e:
#                    content_type = None
#                    continue
#
#                object_id = getattr(self.content_object, campuri_structuri.get(self.content_type.name)).id
#                if AsociereMembruStructura.objects.filter(membru = self.membru, content_type = content_type, object_id = object_id, tip_asociere = self.tip_asociere,
#                                        moment_inceput__lte = self.moment_inceput, moment_incheiere__isnull = True).count() == 0:
#                    AsociereMembruStructura(membru = self.membru, content_type = content_type, object_id = object.id,
#                                            tip_asociere = self.tip_asociere, moment_inceput = self.moment_inceput,
#                                            confirmata = self.confirmata, confirmata_pe = self.confirmata_pe,
#                                            confirmata_de = self.confirmata_de).save()
#
#        return retval


class TipInformatieContact(models.Model):
    nume = models.CharField(max_length=255)
    template_name = models.CharField(max_length=255, null=True, blank=True)

    descriere = models.CharField(max_length=255, null=True, blank=True)
    relevanta = models.CharField(max_length=255, null=True, blank=True)

    adresa = models.BooleanField(default=False)
    is_sms_capable = models.BooleanField(default=False)

    categorie = models.CharField(max_length=255, default="Contact")

    def __str__(self):
        return u"%s" % self.nume


class InformatieValabilaManager(models.Manager):
    def get_queryset(self):
        return super(InformatieValabilaManager, self).get_queryset().filter(
            Q(data_end__isnull=True) | Q(data_end__lte=datetime.datetime.now()))


class InformatieContact(models.Model):
    tip_informatie = models.ForeignKey(TipInformatieContact, on_delete=models.CASCADE)
    valoare = models.CharField(max_length=1024)

    data_start = models.DateTimeField(null=True, blank=True)
    data_end = models.DateTimeField(null=True, blank=True)

    implicita = models.BooleanField(default=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    obiect_ref_ctype = models.ForeignKey(ContentType, related_name="referit", null=True, blank=True, on_delete=models.CASCADE)
    obiect_ref_id = models.PositiveIntegerField(null=True, blank=True)

    informatii_suplimentare = models.CharField(max_length=1024, null=True, blank=True)

    objects = InformatieValabilaManager()
    all_objects = models.Manager()

    def __str__(self):
        return "%s: %s" % (self.tip_informatie.nume, self.valoare)

    def process_adresa(self):
        try:
            return AdresaPostala.parse_address(self.valoare), None
        except Exception as e:
            return None, e

    def get_cod_postal(self):
        try:
            adresa, err = self.process_adresa()
            if adresa:
                if adresa.are_cod():
                    return adresa.cod

                adresa.determine_cod()

                if adresa.are_cod():
                    return adresa.cod
        except Exception as e:
            return e

        return None


DOMENII_DEZVOLTARE = (("intelectual", "Intelectual"),
                      ("fizic", "Fizic"),
                      ("afectiv", "Afectiv"),
                      ("social", "Social"),
                      ("caracter", "Caracter"),
                      ("spiritual", "Spiritual"))


class ObiectivEducativProgres(models.Model):
    titlu = models.CharField(max_length=2048)
    descriere = models.TextField(null=True, blank=True)
    domeniu = models.CharField(max_length=255, choices=DOMENII_DEZVOLTARE)
    pista = models.CharField(max_length=1024, null=True, blank=True)


class EtapaProgres(models.Model):
    ramura_de_varsta = models.ForeignKey(RamuraDeVarsta, on_delete=models.CASCADE)
    nume = models.CharField(max_length=255)
    logo = models.ForeignKey(Imagine, on_delete=models.SET_NULL, null=True, blank=True)
    ordine = models.PositiveSmallIntegerField(null=True, blank=True)
    slug = models.SlugField()

    reguli = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.nume


class BadgeMerit(models.Model):
    ramura_de_varsta = models.ForeignKey(RamuraDeVarsta, null=True, blank=True, on_delete=models.CASCADE)
    etapa_progres = models.ForeignKey(EtapaProgres, null=True, blank=True, on_delete=models.CASCADE)
    nume = models.CharField(max_length=255)
    descriere = models.TextField(null=True, blank=True)
    logo = models.ForeignKey(Imagine, null=True, blank=True, on_delete=models.SET_NULL)


class TargetEtapaProgres(models.Model):
    titlu = models.CharField(max_length=2048)
    capitol = models.CharField(max_length=2048)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey()


class EtapaProgresMembru(models.Model):
    etapa_progres = models.ForeignKey(EtapaProgres, on_delete=models.CASCADE)
    membru = models.ForeignKey(Membru, related_name="etape_progres", on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Membru, related_name="etape_progres_evaluate", on_delete=models.CASCADE)
    data = models.DateField()
    detalii = models.TextField(null=True, blank=True)


class BadgeMeritMembru(models.Model):
    badge = models.ForeignKey(BadgeMerit, on_delete=models.CASCADE)
    membru = models.ForeignKey(Membru, related_name="badgeuri_merit", on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Membru, related_name="badgeuri_merit_evaluate", on_delete=models.CASCADE)
    data = models.DateField()
    detalii = models.TextField(null=True, blank=True)


class NoteObiectivProgresMembru(models.Model):
    obiectiv = models.ForeignKey(ObiectivEducativProgres, on_delete=models.CASCADE)
    nota = models.TextField()

    membru = models.ForeignKey(Membru, related_name="note_obiective_progres", on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Membru, related_name="note_obiective_progres_evaluate", on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    activitate = models.ForeignKey("album.Eveniment", null=True, blank=True, on_delete=models.SET_NULL)
    obiectiv_atins = models.BooleanField(default=False)
    etapa_progres = models.ForeignKey(EtapaProgres, on_delete=models.CASCADE)


class NotaTargetEtapaProgres(models.Model):
    target = models.ForeignKey(TargetEtapaProgres, on_delete=models.CASCADE)

    membru = models.ForeignKey(Membru, related_name="note_etape_progres", on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Membru, related_name="note_etape_progres_evaluate", on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    target_atins = models.BooleanField(default=False)

    activitate = models.ForeignKey("album.Eveniment", on_delete=models.SET_NULL, null=True, blank=True)




TIPURI_ASOCIERE = TipAsociereMembruStructura.objects.all().select_related("content_types")
