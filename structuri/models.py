#   coding: utf-8

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Sum
import logging
import datetime
from django.db.models import permalink
from photologue.models import ImageModel
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
import unidecode
from adrese_postale.adrese import AdresaPostala
from album.models import Imagine
from documente.models import PlataCotizatieTrimestru, AsociereDocument, Trimestru, ChitantaCotizatie
from utils.models import FacebookSession
from django.core import cache

logger = logging.getLogger(__name__)
redis_cache = cache.get_cache("redis")


class RamuraDeVarsta(models.Model):
    nume = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    varsta_intrare = models.PositiveSmallIntegerField()
    varsta_iesire = models.PositiveSmallIntegerField(null=True, blank=True)
    culoare = models.CharField(max_length=255, null=True, blank=True)
    are_patrule = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s" % self.nume


class Structura(models.Model):
    class Meta:
        abstract = True

    nume = models.CharField(max_length=255)
    data_infiintare = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    def delete(self, using=None):
        AsociereMembruStructura.objects.filter(content_type=ContentType.objects.get_for_model(self),
                                               object_id=self.id).delete()

        return super(Structura, self).delete(using)

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

        if isinstance(tip_asociere, type([])):
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
    class Meta:
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

    moment_initial_cotizatie = models.ForeignKey("documente.Trimestru", null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to=upload_to_centru_local_logo)
    antet = models.ImageField(null=True, blank=True, upload_to=upload_to_centru_local_antent)

    def nume_complet(self):
        if self.denumire is not None and self.denumire != "":
            return u"Centrul Local \"%s\" %s" % (self.denumire, self.localitate)
        return u"Centrul Local %s" % self.localitate

    def __unicode__(self):
        return u"%s" % self.nume_complet()

    def save(self, *args, **kwargs):
        self.nume = self.nume_complet()
        return super(CentruLocal, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ("structuri:cl_detail", [], {"pk": self.id})

    def adeziuni_lipsa(self):
        cnt_membri = self.cercetasi(qs=True).count()
        cnt_adeziuni = AsociereDocument.objects.filter(content_type=ContentType.objects.get_for_model(Membru),
                                                       tip_asociere__nume__iexact="subsemnat",
                                                       document__tip_document__slug="adeziune",
                                                       document__registru__centru_local=self).count()
        return cnt_membri - cnt_adeziuni



class Unitate(Structura):
    class Meta:
        verbose_name = u"Unitate"
        verbose_name_plural = u"Unități"

    ramura_de_varsta = models.ForeignKey(RamuraDeVarsta)
    centru_local = models.ForeignKey(CentruLocal)

    def __unicode__(self):
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
    @models.permalink
    def get_absolute_url(self):
        return ("structuri:unitate_detail", [], {"pk": self.id})


class Patrula(Structura):
    class Meta:
        verbose_name = u"Patrulă"
        verbose_name_plural = u"Patrule"

    unitate = models.ForeignKey(Unitate)
    moment_inchidere = models.DateField(null=True, blank=True)

    @property
    def ramura_de_varsta(self):
        return self.unitate.ramura_de_varsta

    @property
    def centru_local(self):
        return self.unitate.centru_local

    def __unicode__(self):
        return u"Patrula %s" % self.nume

    @models.permalink
    def get_absolute_url(self):
        return ("structuri:patrula_detail", [], {"pk": self.id})


class Utilizator(models.Model):
    user = models.OneToOneField("auth.User", null=True, blank=True)
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

    def __unicode__(self):
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
    reverse_relationship = models.ForeignKey("self", null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.nume


class PersoanaDeContact(models.Model):
    nume = models.CharField(max_length=255, null=True, blank=True)
    tip_relatie = models.ForeignKey(TipRelatieFamilie, null=True, blank=True)
    telefon = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    implicit = models.BooleanField(default=False)

    job = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"Profesie, loc de muncă")

    note = models.CharField(max_length=1024, null=True, blank=True)
    membru = models.ForeignKey("Membru")


@receiver(post_save, sender=PersoanaDeContact)
def enforce_default(sender, instance, *args, **kwargs):
    if instance.implicit:
        for contact in PersoanaDeContact.objects.filter(membru=instance.membru, implicit=True).exclude(id=instance.id):
            contact.implicit = False
            contact.save()


class AsociereMembruFamilie(models.Model):
    tip_relatie = models.ForeignKey(TipRelatieFamilie)
    persoana_sursa = models.ForeignKey("Membru")
    persoana_destinatie = models.ForeignKey("Membru", related_name="membru_destinatie")

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
    cnp = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"CNP", unique=True)
    telefon = models.CharField(max_length=10, null=True, blank=True)
    adresa = models.CharField(max_length=2048, null=True, blank=True)
    data_nasterii = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=(("m", u"Masculin"), ("f", "Feminin")), null=True, blank=True)

    familie = models.ManyToManyField("self", through=AsociereMembruFamilie, symmetrical=False, null=True, blank=True)
    scout_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID ONCR")
    scor_credit = models.IntegerField(default=2, choices=((0, u"Rău"), (1, u"Neutru"), (2, u"Bun")), verbose_name=u"Credit", help_text=u"Această valoare reprezintă încrederea Centrului Local într-un membru de a-și respecta angajamentele financiare (dacă Centrul are sau nu încredere să pună bani pentru el / ea)")

    #TODO: find some smarter way to do this
    poza_profil = models.ForeignKey(ImagineProfil, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Asigură la salvare preluarea sexului și a datei nașterii din CNP
        Asigură menținerea centrulu local corect
        """

        if self.data_nasterii == None:
            sufix_an = self.cnp[1:3]
            luna = self.cnp[3:5]
            ziua = self.cnp[5:7]

            if int(self.cnp[0]) in (1, 2):
                prefix_an = "19"
            elif int(self.cnp[0]) in (5, 6):
                prefix_an = "20"
            else:
                prefix_an = "19"

            self.data_nasterii = datetime.date(year=int("%s%s" % (prefix_an, sufix_an)), month=int(luna), day=int(ziua))

        if self.sex == None:
            if int(self.cnp[0]) % 2 == 0:
                self.sex = "f"
            else:
                self.sex = "m"

        return super(Membru, self).save(*args, **kwargs)

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

    def get_centru_local(self, qs=False, tip_asociere=[]):
        if len(tip_asociere) == 0:
            tip_asociere = CentruLocal.asocieri_membru

        asocieri_filter = dict(membru=self,
                               content_type=ContentType.objects.get_for_model(CentruLocal),
                               tip_asociere__nume__in=tip_asociere,
                               moment_incheiere__isnull=True)
        asocieri = AsociereMembruStructura.objects.filter(**asocieri_filter).order_by("-moment_inceput", )

        if qs:
            return asocieri

        if asocieri.count():
            return asocieri[0].content_object

        return None

    def get_structura(self, qs=False, rol=[u"Membru", ], single=True, structura_model=None, trimestru=None):
        if self.is_lider and not single:
            rol = rol + [u"Lider", u"Lider asistent"]

        kwargs = {"content_type": ContentType.objects.get_for_model(structura_model),
                  "tip_asociere__nume__in": rol,
                  "tip_asociere__content_types__in": (ContentType.objects.get_for_model(structura_model), ),
                  "membru": self}

        asocieri = AsociereMembruStructura.objects.filter(**kwargs).order_by("-moment_inceput")

        if trimestru is None:
            # trimestrul curent, vorbim despre prezent
            asocieri = asocieri.filter(moment_inceput__isnull=False, moment_incheiere__isnull=True)
        else:
            asocieri = asocieri.filter(Q(moment_incheiere__isnull=True) | Q(moment_incheiere__gte=trimestru.data_inceput))
            asocieri = asocieri.filter(moment_inceput__lte=trimestru.data_sfarsit)

        if asocieri.count():
            if qs:
                if single:
                    return asocieri[0]
                else:
                    return asocieri
            else:
                if single:
                    return asocieri[0].content_object
                else:
                    return [a.content_object for a in asocieri]

        return None

    def get_unitate(self, qs=False, rol=[u"Membru", ], single=True, trimestru=None):
        return self.get_structura(qs=qs, rol=rol, single=single, structura_model=Unitate, trimestru=trimestru)

    def get_patrula(self, qs=False, rol=[u"Membru", ], single=True, trimestru=None):
        return self.get_structura(qs=qs, rol=rol, single=single, structura_model=Patrula, trimestru=trimestru)

    def get_unitati(self, qs=False, rol=[u"Membru", ], trimestru=None):
        return self.get_unitate(qs=qs, rol=rol, single=False, trimestru=trimestru)

    def get_patrule(self, qs=False, rol=[u"Membru", ], trimestru=None):
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
        if not isinstance(calitate, type([])):
            calitate = [calitate, ]

        if not structura:
            if qs:
                return AsociereMembruStructura.objects.none()
            return False

        ams_filter = dict(content_type=ContentType.objects.get_for_model(structura),
                          object_id=structura.id,
                          tip_asociere__content_types__in=(ContentType.objects.get_for_model(structura), ),
                          tip_asociere__nume__in=calitate,
                          membru=self)

        asocieri = AsociereMembruStructura.objects.filter(**ams_filter)
        if trimestru is None:
            asocieri = asocieri.filter(moment_inceput__isnull=False, moment_incheiere__isnull=True)
        else:
            asocieri = asocieri.filter(Q(moment_incheiere__isnull=True) | Q(moment_incheiere__gte=trimestru.data_inceput))
            asocieri = asocieri.filter(moment_inceput__lte=trimestru.data_sfarsit)

        if qs:
            return asocieri

        return asocieri.count() != 0

    CALITATI_COMUNE = ["Membru suspendat", "Membru aspirant", "Membru inactiv", "Membru Consiliul Centrului Local",
                       "Lider", "Lider asistent", "Membru adult", u"Șef Centru Local"]

    def _proprietati_comune(self):
        _proprietati = self.get_from_cache("proprietati")
        if _proprietati:
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

    @permalink
    def get_home_link(self):
        if self.is_lider():
            unitate = self.get_unitate(rol=(u"Lider", u"Lider asistent"))
            if unitate:
                return ("structuri:unitate_detail", [], {"pk": unitate.id})
            return ("structuri:cl_detail", [], {"pk": self.centru_local.id})
        return ("structuri:membru_profil", [], {})

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

    def get_ramura_de_varsta(self):
        if self.is_lider_generic():
            return "Lider"

        unitate = self.get_unitate()
        if unitate:
            return self.get_unitate().ramura_de_varsta.nume
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
        import json
        badges = self.get_from_cache("badges_rdv")
        badges = json.loads(badges if badges else "[]")

        if badges:
            return badges
        badges = []

        if self.is_lider_generic():
            badges.append("lider")
        else:
            unitate = self.get_unitate()
            if unitate:
                badges.append(unidecode.unidecode(unitate.ramura_de_varsta.nume.lower()))
        self.save_to_cache("badges_rdv", json.dumps(badges))
        print "SAED TO CACHE %s" % badges
        return badges

    def get_extra_badges(self):
        import json
        badges = self.get_from_cache("badges_extra")
        badges = json.loads(badges if badges else "[]")

        if badges:
            return badges
        badges = []

        if self.is_sef_centru():
            badges.append("sef-centru")
        if self.is_membru_ccl():
            badges.append("membru-ccl")

        self.save_to_cache("badges_extra", json.dumps(badges))
        return badges

    @models.permalink
    def get_absolute_url(self):
        return ("structuri:membru_detail", [], {"pk": self.id})

    #    Patrocle specific code
    def rezerva_credit(self):
        from patrocle.models import Credit

        credit = Credit.objects.filter(content_type=ContentType.objects.get_for_model(CentruLocal),
                                       object_id=self.centru_local.id,
                                       epuizat=False).order_by("timestamp")
        if credit.count() == 0:
            return False

        credit = credit[0]

        if credit.credit_disponibil() > 0:
            from patrocle.models import RezervareCredit

            rezervare = RezervareCredit(credit=credit, content_type=ContentType.objects.get_for_model(self),
                                        object_id=self.id)
            rezervare.save()

        return True

    def elibereaza_credit(self):
        from patrocle.models import RezervareCredit

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

    def clear_cache(self, index):
        mapping = {"asociere": ["trimestru_initial", "proprietati", "badges_rdv"],
                   "cotizatie_sociala": ["are_cotizatie_sociala", "status_cotizatie"],
                   "cotizatie": ["status_cotizatie", ],}
        to_clear = mapping.get(index, None)
        if to_clear is not None:
            for idx in to_clear:
                redis_cache.delete("m:%d:%s" % (self.id, idx))

    def get_from_cache(self, index):
        val = redis_cache.get("m:%d:%s" % (self.id, index))
        return val

    def save_to_cache(self, index, value, timeout=0):
        return redis_cache.set("m:%d:%s" % (self.id, index), value, timeout)

    #    Cotizatie specific code
    def get_trimestru_initial_cotizatie(self):
        """ Obtine primul trimestu din care acest membru ar trebui sa plateasca cotizatie.
        Acesta este dependent de data inscrierii (pentru membri inscrisi dupa momentul 0
        al centrului local) sau este momentul 0 al centrului local (pentru cei inscrisi pana 
        la momentul 0)
        """
        stored_value = self.get_from_cache("trimestru_initial")
        if stored_value:
            from documente.models import Trimestru
            return Trimestru.objects.get(id=stored_value)

        #    in mod necesar membrul are macar un centru local asociat
        #    calitatea de membru in ONCR se intampla prin intermediul Centrelor Locale
        filter_kwargs = {"content_type": ContentType.objects.get_for_model(CentruLocal)}
        afilieri = self.afilieri.filter(**filter_kwargs).order_by("moment_inceput")
        if not afilieri.count():
            raise ValueError(u"Cercetașul cu ID-ul %d nu are niciun Centru Local asociat" % self.id)

        moment_initial_membru = afilieri[0].moment_inceput
        from documente.models import Trimestru

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

        from documente.models import DocumentCotizatieSociala, AsociereDocument

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
            for q in quotas.items():
                logger.debug(u"aplica_reducere_familie, verific existență cotizație %s pentru %s, trimestrul %s" % (q[1], self, trimestru))
                found = False

                if valoare * q[1] == plati_membri_familie[plata_index][1]:
                    found = True
                    plata_index += 1

                if found is False or plata_index > len(plati_membri_familie) - 1:
                    break

        quota = quotas.get(plata_index, 0.25)
        return valoare * quota

    def _status_cotizatie(self):
        """ Cotizatia se poate plati pana pe 15 a ultimei luni din trimestru
        """

        stored_value = self.get_from_cache("status_cotizatie")
        if stored_value:
            return stored_value

        pct = PlataCotizatieTrimestru.objects.filter(membru=self, final=True).order_by("-trimestru__ordine_globala")[0:1]
        nothing = False
        if pct.count():
            ultimul_trimestru = pct[0].trimestru
        else:
            ultimul_trimestru = self.get_trimestru_initial_cotizatie()
            nothing = True

        from documente.models import Trimestru
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
        trimestre_scutite = 0
        while trimestru.ordine_globala < trimestru_curent.ordine_globala:
            if not self.plateste_cotizatie(trimestru=trimestru):
                trimestre_scutite += 1
            trimestru = trimestru.urmatorul_trimestru(trimestru)

        diferenta_trimestre -= trimestre_scutite

        return_value = diferenta_trimestre, trimestru_curent, ultimul_trimestru
        self.save_to_cache("status_cotizatie", return_value, 60 * 60 * 6)
        return return_value

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
        from documente.models import Trimestru

        plati_membru = self.platacotizatietrimestru_set.all().order_by("-trimestru__ordine_globala", "-index")
        plati_partiale = None
        if plati_membru.count() == 0:
            trimestru_initial = self.get_trimestru_initial_cotizatie()
        elif plati_membru[0].partial and not plati_membru[0].final:
            trimestru_initial = plati_membru[0].trimestru
            plati_partiale = self.platacotizatietrimestru_set.filter(trimestru=trimestru_initial)
        else:
            trimestru_initial = Trimestru.urmatorul_trimestru(plati_membru[0].trimestru)

        if return_plati_partiale:
            return trimestru_initial, plati_partiale
        return trimestru_initial

    def calculeaza_necesar_cotizatie(self):
        return PlataCotizatieTrimestru.calculeaza_necesar(membru=self)

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
        return self.adeziune(qs=True).count() > 0

    def adeziune(self, qs=False):
        search = {"document__tip_document__slug" : "adeziune",
                  "tip_asociere__slug" : "subsemnat",
                  "content_type" : ContentType.objects.get_for_model(self),
                  "object_id" : self.id}

        asociere = AsociereDocument.objects.filter(**search)
        if qs:
            return asociere
        if asociere.count():
            return asociere.document
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

    def is_lider_asistent(self):
        return self._proprietati_comune().get("Lider asistent", False)

    def is_lider_generic(self):
        return self.is_lider() or self.is_lider_asistent()

    def is_membru_ccl(self):
        return self._proprietati_comune().get("Membru Consiliul Centrului Local", False)

    def is_sef_centru(self):
        return self._proprietati_comune().get(u"Șef Centru Local", False)

    def plateste_cotizatie(self, trimestru=None):
        """ determina daca un membru plateste sau nu cotizatie
        din notele de implementare curente, neplatitori de cotizatie pentru un anumit trimestru sunt
        1) membrii inactivi, marcati ca atare
        2) membrii adulti, marcati ca atare si membrii ai unei unitati de adulti
        toate celalalte categorii de membrii sunt platitori de cotizatie
        """

        if trimestru is None:
            trimestru = Trimestru.trimestru_pentru_data(datetime.date.today())

        if self.are_calitate(["Lider", "Lider asistent"], self.centru_local, trimestru=trimestru):
            return True

        # unitate = self.get_unitate(trimestru=trimestru)
        # if unitate is None:
        #     #   orice membru care nu este in nicio unitate este un caz special care va fi tratat ca platitor
        #     #   nu ar trebui sa existe un asemenea caz
        #     logger.info("Membru: membru care nu este lider, si nu apartine niciunei unitati %s" % self)
        #     return True

        if self.are_calitate(["Membru inactiv", "Membru adult"], self.centru_local, trimestru=trimestru):
            return False

        # if unitate.ramura_de_varsta.slug == "adulti" and self.are_calitate("Membru adult", self.centru_local, trimestru=trimestru):
        #     return False

        return True

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
    content_types = models.ManyToManyField(ContentType, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.nume


class AsocierePublicManager(models.Manager):
    def get_queryset(self):
        return super(AsocierePublicManager, self).get_queryset().filter(confirmata=True)


ordine_structuri = {u"Patrulă": u"Unitate", u"Unitate": u"Centru Local"}
campuri_structuri = {u"Patrulă": u"Unitate", u"Unitate": u"centru_local"}


class AsociereMembruStructura(models.Model):
    membru = models.ForeignKey(Membru, related_name="afilieri")

    content_type = models.ForeignKey(ContentType, verbose_name=u"Tip structură")
    object_id = models.PositiveIntegerField(verbose_name=u"Structură")
    content_object = GenericForeignKey()

    tip_asociere = models.ForeignKey(TipAsociereMembruStructura)

    moment_inceput = models.DateTimeField(null=True, blank=True)
    moment_incheiere = models.DateTimeField(null=True, blank=True)

    confirmata = models.BooleanField(default=False)
    confirmata_pe = models.DateTimeField(null=True, blank=True)
    confirmata_de = models.ForeignKey(Utilizator, null=True, blank=True, related_name="asocieri_confirmate")

    objects = AsocierePublicManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return u"%s - %s - %s" % (self.membru, self.tip_asociere, self.content_object)

    def get_structura(self, ctype):
        lookups = {"centrulocal": {"centrulocal": lambda: self.content_object},
                   "unitate": {"centrulocal": lambda: self.content_object.centru_local,
                               "unitate": lambda: self.content_object},
                   "patrula": {"centrulocal": lambda: self.content_object.unitate.centru_local,
                               "unitate": lambda: self.content_object.unitate,
                               "patrula": lambda: self.content_object}}

        if self.content_type.model not in lookups.keys():
            return None

        if ctype.model not in lookups.get(self.content_type.model):
            return None

        return lookups.get(self.content_type.model).get(ctype.model)()

    def confirma(self, user):
        self.confirmata = True
        self.confirmata_pe = datetime.datetime.now()
        self.confirmata_de = user
        self.save()

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

    def __unicode__(self):
        return u"%s" % self.nume


class InformatieValabilaManager(models.Manager):
    def get_queryset(self):
        return super(InformatieValabilaManager, self).get_queryset().filter(
            Q(data_end__isnull=True) | Q(data_end__lte=datetime.datetime.now()))


class InformatieContact(models.Model):
    tip_informatie = models.ForeignKey(TipInformatieContact)
    valoare = models.CharField(max_length=1024)

    data_start = models.DateTimeField(null=True, blank=True)
    data_end = models.DateTimeField(null=True, blank=True)

    implicita = models.BooleanField(default=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    obiect_ref_ctype = models.ForeignKey(ContentType, related_name="referit", null=True, blank=True)
    obiect_ref_id = models.PositiveIntegerField(null=True, blank=True)

    informatii_suplimentare = models.CharField(max_length=1024, null=True, blank=True)

    objects = InformatieValabilaManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return "%s: %s" % (self.tip_informatie.nume, self.valoare)

    def process_adresa(self):
        try:
            return AdresaPostala.parse_address(self.valoare), None
        except Exception, e:
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
        except Exception, e:
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
    ramura_de_varsta = models.ForeignKey(RamuraDeVarsta)
    nume = models.CharField(max_length=255)
    logo = models.ForeignKey(Imagine)
    ordine = models.PositiveSmallIntegerField(null=True, blank=True)
    slug = models.SlugField()

    reguli = models.CharField(max_length=1024, null=True, blank=True)

    def __unicode__(self):
        return self.nume


class BadgeMerit(models.Model):
    ramura_de_varsta = models.ForeignKey(RamuraDeVarsta, null=True, blank=True)
    etapa_progres = models.ForeignKey(EtapaProgres, null=True, blank=True)
    nume = models.CharField(max_length=255)
    descriere = models.TextField(null=True, blank=True)
    logo = models.ForeignKey(Imagine, null=True, blank=True)


class TargetEtapaProgres(models.Model):
    titlu = models.CharField(max_length=2048)
    capitol = models.CharField(max_length=2048)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey()


class EtapaProgresMembru(models.Model):
    etapa_progres = models.ForeignKey(EtapaProgres)
    membru = models.ForeignKey(Membru, related_name="etape_progres")
    evaluator = models.ForeignKey(Membru, related_name="etape_progres_evaluate")
    data = models.DateField()
    detalii = models.TextField(null=True, blank=True)


class BadgeMeritMembru(models.Model):
    badge = models.ForeignKey(BadgeMerit)
    membru = models.ForeignKey(Membru, related_name="badgeuri_merit")
    evaluator = models.ForeignKey(Membru, related_name="badgeuri_merit_evaluate")
    data = models.DateField()
    detalii = models.TextField(null=True, blank=True)


class NoteObiectivProgresMembru(models.Model):
    obiectiv = models.ForeignKey(ObiectivEducativProgres)
    nota = models.TextField()

    membru = models.ForeignKey(Membru, related_name="note_obiective_progres")
    evaluator = models.ForeignKey(Membru, related_name="note_obiective_progres_evaluate")
    timestamp = models.DateTimeField()

    activitate = models.ForeignKey("album.Eveniment", null=True, blank=True)
    obiectiv_atins = models.BooleanField(default=False)
    etapa_progres = models.ForeignKey(EtapaProgres)


class NotaTargetEtapaProgres(models.Model):
    target = models.ForeignKey(TargetEtapaProgres)

    membru = models.ForeignKey(Membru, related_name="note_etape_progres")
    evaluator = models.ForeignKey(Membru, related_name="note_etape_progres_evaluate")

    timestamp = models.DateTimeField(auto_now_add=True)
    target_atins = models.BooleanField(default=False)

    activitate = models.ForeignKey("album.Eveniment", null=True, blank=True)