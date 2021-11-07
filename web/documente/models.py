# coding: utf-8
from __future__ import division
from past.utils import old_div
from builtins import object
import datetime
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.urls import reverse
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from scoutfile3.s3utils import LocalStorage

logger = logging.getLogger(__name__)


def upload_to_document_fisier(instance, file_name):
    return "declaratii/%s" % file_name


class Document(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    data_inregistrare = models.DateField(null=True, blank=True)

    titlu = models.CharField(max_length=1024)
    descriere = models.CharField(max_length=2048, null=True, blank=True)

    fisier = models.FileField(upload_to=upload_to_document_fisier, null=True, blank=True, storage=LocalStorage())
    url = models.URLField(max_length=2048, null=True, blank=True)

    version_number = models.IntegerField(default=0)
    root_document = models.ForeignKey("Document", related_name="versions", on_delete=models.SET_NULL, null=True, blank=True)
    folder = models.ForeignKey("Document", on_delete=models.SET_NULL, related_name="fisiere", null=True, blank=True)
    locked = models.BooleanField(default=False)

    is_folder = models.BooleanField(default=False)
    fragment = models.IntegerField(default=0)

    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    tip_document = models.ForeignKey("TipDocument", on_delete=models.CASCADE, null=True, blank=True)

    registru = models.ForeignKey("Registru", on_delete=models.SET_NULL, null=True, blank=True)
    numar_inregistrare = models.PositiveIntegerField(null=True, blank=True)

    #   de folosit pentru cand documentul este in fapt o imagine, care trebuie procesata (thumbnail-uri ...)
    image_storage = models.ForeignKey("album.Imagine", on_delete=models.SET_NULL, null=True, blank=True)
    # rol_in_folder = models.ForeignKey

    def __str__(self):
        return u"%s" % self.titlu

    def referinta(self):
        return "%d / %s" % (self.numar_inregistrare, self.data_inregistrare.strftime("%d.%m.%Y"))

    def edit_link(self):
        return ""

    def save(self, **kwargs):
        if not self.data_inregistrare:
            self.data_inregistrare = self.date_created
        return super(Document, self).save(**kwargs)

    def get_absolute_url(self):
        if hasattr(self, "decizie"):
            if hasattr(self.decizie, "deciziecotizatie"):
                return self.decizie.deciziecotizatie.get_absolute_url()

    def asocieri(self, tip=None, qs=True, **kwargs):
        qs = self.asocieredocument_set.all()
        if tip:
            qs = qs.filter(tip_asociere__slug = tip)

        return qs

    def get_download_url(self):
        if self.fisier:
            return self.fisier
        if self.image_storage:
            return self.image_storage.image.url

    @property
    def source_type(self):
        if self.fisier:
            return ("fisier", u"Fișier")
        if self.image_storage:
            return ("imagine", u"Imagine")
        if self.url:
            return ("link", u"Link")
        return ("necunoscut", u"?")

    @property
    def shortcode_reference(self):
        return "[[doc#%s]]" % self.id

# tagging.register(Document)

class TipAsociereDocument(models.Model):
    nume = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)


class AsociereDocument(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    document_ctype = models.ForeignKey(ContentType, null=True, blank=True, related_name="asociere", on_delete=models.SET_NULL)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    tip_asociere = models.ForeignKey(TipAsociereDocument, on_delete=models.CASCADE, null=True, blank=True)

    moment_asociere = models.DateTimeField(auto_now_add=True)
    responsabil = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None):
        self.document_ctype = ContentType.objects.get_for_model(self.document)
        return super(AsociereDocument, self).save(force_insert=force_insert, force_update=force_update,
                                                  using=using)

    def document_edit_link(self):
        return self.document_ctype.get_object_for_this_type(id=self.document.id).edit_link()

    @classmethod
    def inregistreaza(cls, document=None, to=None, tip=None, responsabil=None):
        tip_asociere, created = TipAsociereDocument.objects.get_or_create(slug=tip)
        if created:
            tip_asociere.save()

        asociere_kwargs = dict(
            document=document,
            content_type=ContentType.objects.get_for_model(to),
            object_id=to.id,
            tip_asociere=tip_asociere,
            responsabil=responsabil
        )

        asociere = cls(**asociere_kwargs)
        asociere.save()
        return asociere


class TipDocument(models.Model):
    slug = models.CharField(max_length=255)
    nume = models.CharField(max_length=255)
    descriere = models.TextField(null=True, blank=True)

    def __str__(self):
        return u"{0}".format(self.nume)

    @classmethod
    def obtine(cls, slug):
        tip, created = cls.objects.get_or_create(slug=slug)
        if created:
            tip.nume = slug.capitalize().replace("_", " ")
            tip.save()

        return tip


class Adeziune(Document):
    class Meta(object):
        proxy = True

    registre_compatibile = ["intern", ]

    def save(self, **kwargs):
        self.tip_document = TipDocument.obtine("adeziune")
        return super(Adeziune, self).save(**kwargs)


class Chitanta(Document):
    casier = models.ForeignKey("structuri.Membru", null=True, blank=True, on_delete=models.SET_NULL)
    #serie = models.CharField(max_length=255)
    #numar = models.IntegerField(default=0)
    suma = models.FloatField(default=0)
    printata = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.tip_document:
            self.tip_document = TipDocument.objects.get(slug="chitanta")
        return super(Chitanta, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def referinta(self):
        return "Seria %s, nr. %s / %s" % (self.registru.serie, self.numar_inregistrare, self.date_created.strftime("%d.%m.%Y"))

    def platitor(self):
        from structuri.models import Membru
        asociere_filter = dict(document=self, content_type=ContentType.objects.get_for_model(Membru), tip_asociere__slug="platitor")
        asociere = AsociereDocument.objects.get(**asociere_filter)
        return asociere.content_object

    def editabila(self):
        return not self.printata

    @classmethod
    def pentru_membru(cls, membru=None, tip_document="chitanta"):
        from structuri.models import Membru
        asociere_filter = dict(content_type=ContentType.objects.get_for_model(Membru),
                               object_id=membru.id,
                               document__tip_document__slug=tip_document,
                               tip_asociere__slug="platitor")
        asocieri = AsociereDocument.objects.filter(**asociere_filter).order_by("moment_asociere")
        return [a.document for a in asocieri]

    def delete(self, **kwargs):
        if not self.editabila():
            raise Exception(u"Chitanța nu este editabilă, nu poate fi ștearsă")
        return super(Chitanta, self).delete(**kwargs)


class Trimestru(models.Model):
    data_inceput = models.DateField()
    data_sfarsit = models.DateField()
    ordine_locala = models.PositiveSmallIntegerField()
    ordine_globala = models.PositiveIntegerField()

    def __json__(self):
        return {"ordine" : self.ordine_locala,
                "ordine_globala" : self.ordine_globala,
                "an" : self.data_inceput.strftime("%Y"),
                "text" : self.__unicode__()}

    @classmethod
    def get_trimestru(cls, year, order):
        if Trimestru.objects.count() == 0:
            call_command('genereaza_trimestre')

        try:
            return Trimestru.objects.get(data_inceput__year = year,
                                         ordine_locala = order)
        except Trimestru.DoesNotExist:
            t = Trimestru.objects.all().order_by("-ordine_globala")[0]
            while t.ordine_locala != order and t.data_inceput.year != year:
                t = Trimestru.urmatorul_trimestru(trimestru = t)
            return t

    @classmethod
    def urmatorul_trimestru(cls, trimestru=None, offset=1):
        if trimestru:
            try:
                return cls.objects.get(ordine_globala=trimestru.ordine_globala + 1)
            except cls.DoesNotExist:
                #    creaza un nou trimestru, presupunand ca exista un trimestru anterior
                trimestru_nou = Trimestru()
                trimestru_nou.ordine_globala = trimestru.ordine_globala + 1
                trimestru_nou.ordine_locala = trimestru.ordine_locala + 1 if trimestru.ordine_locala < 4 else 1

                an_nou = trimestru.data_inceput.year
                if trimestru.ordine_locala == 4:
                    an_nou += 1

                #    trimestrul incepe in lunile 1, 4, 7 sau 10
                luna_noua = (trimestru_nou.ordine_locala - 1) * 3 + 1
                #    trimestru incepe in prima zi a primei luni din trimestu
                trimestru_nou.data_inceput = datetime.date(year=an_nou, month=luna_noua, day=1)
                #    trimestul se termina cu o zi mai devreme decat prima zi a cele-i de-a 4 luni de la inceput
                #    un caz special este trimestrul IV, in care trebuie trecut in 1 ianuaire a anului urmator si scazuta o zi
                trimestru_nou.data_sfarsit = datetime.date(year=an_nou + old_div(trimestru_nou.ordine_locala, 4),
                                                           month=luna_noua + 3 if luna_noua < 10 else 1,
                                                           day=1) - datetime.timedelta(days=1)
                trimestru_nou.save()
                return trimestru_nou

        #    trimestrul de inceput pentru toate record-urile hardcodat aici
        #    pentru primul trimestru cu noua cotizatie (1 octombrie 2011)

        if Trimestru.objects.all().count():
            raise ValueError("Metoda __urmatorul trimestru__ trebuie apelata cu un parametru trimestru")

        call_command('genereaza_trimestre')

        return Trimestru.objects.get(data_inceput = datetime.date(year=2011, month=10, day=1))

    @classmethod
    def trimestru_pentru_data(cls, data):
        try:
            return cls.objects.get(data_inceput__lte=data,
                                   data_sfarsit__gte=data)
        except cls.DoesNotExist:
            t = Trimestru.objects.all().order_by("-ordine_globala")[0]
            while data.year + 1 > t.data_inceput.year:
                t = Trimestru.urmatorul_trimestru(t)
            return Trimestru.trimestru_pentru_data(data)

    def data_in_trimestru(self, data):
        return (self.data_inceput <= data) and (self.data_sfarsit >= data)

    def identifica_cotizatie(self, membru):
        """ Identifica valoarea cotizatiei pentru acest membru, pentru acest trimestru. Foloseste structura de
        DecizieCotizatie pentru obtinerea datelor. Gestiune cotizatiei implicite si a altor probleme are loc acolo
        @see: DecizieCotizatie
        """

        filtru_cotizatii = dict(centru_local=membru.centru_local, trimestru=self, social=membru.are_cotizatie_sociala(trimestru=self))
        pachet_cotizatii = DecizieCotizatie.get_package_for_centru_local(**filtru_cotizatii)
        valoare_trimestriala = (pachet_cotizatii['national'] + pachet_cotizatii['local']) / 4.
        return valoare_trimestriala

    def __str__(self):
        numerals = ["I", "II", "III", "IV"]
        return "trimestrul %s, %s" % (numerals[self.ordine_locala - 1], self.data_inceput.year)

MOTIVE_INREGISTRARE_PLATA_COTIZATIE = (("normal", u"Plată normală"), ("inactiv", "Inactiv"))


class PlataCotizatieTrimestru(models.Model):
    trimestru = models.ForeignKey(Trimestru, on_delete=models.CASCADE)
    partial = models.BooleanField(default=False)
    final = models.BooleanField(default=False)
    suma = models.FloatField()
    membru = models.ForeignKey("structuri.Membru", on_delete=models.CASCADE)
    chitanta = models.ForeignKey("ChitantaCotizatie", on_delete=models.CASCADE, null=True, blank=True)
    index = models.IntegerField()

    tip_inregistrare = models.CharField(max_length=255, choices=MOTIVE_INREGISTRARE_PLATA_COTIZATIE, default="normal")

    def __json__(self):
        return {"trimestru": self.trimestru.__json__(),
                "partial": self.partial,
                "final": self.final,
                "suma": self.suma,
                "membru": u"%s" % self.membru}

    @classmethod
    def calculeaza_necesar(cls, membru):
        trimestru_initial, plati_partiale = membru.get_ultimul_trimestru_cotizatie(return_plati_partiale=True)
        t_current = trimestru_initial
        t_target = Trimestru.trimestru_pentru_data(data=datetime.date.today() + datetime.timedelta(days=15))

        suma_necesara = 0
        while t_current.ordine_globala < t_target.ordine_globala:
            # print t_current, t_target
            if membru.plateste_cotizatie(t_current):
                cotizatie_trimestru_nominal = t_current.identifica_cotizatie(membru)
                cotizatie_trimestru = membru.aplica_reducere_familie(cotizatie_trimestru_nominal, t_current)
            else:
                cotizatie_trimestru = 0
            if plati_partiale:
                suma_colectata = plati_partiale.aggregate(Sum("suma"))['suma__sum']
                suma_necesara += cotizatie_trimestru - suma_colectata
                plati_partiale = None
            else:
                suma_necesara += cotizatie_trimestru

            t_current = Trimestru.urmatorul_trimestru(trimestru=t_current)

        return suma_necesara


    @classmethod
    def calculeaza_acoperire(cls, membru, chitanta=None, suma=0, chitanta_partial=False, commit=False, casa=None, membri_procesati=[]):
        """ Sparge plata de pe o chitanta in asocierile necesare pentru plati 
        trimestriale pentru un membru, cu plati partiale unde este nevoie.
        
        @param membru: membrul pentru care se fac platile
        @param chitanta: chitanta pe baza careia se fac estimarile (posibil sa nu existe la momentul unei simulari)
        @param commit: daca se salveaza sau nu obiectele create (False == simulare)
        @param chitanta_partial: la recalcularea cotizatiei cu parametrul 'incepand_cu', poate fi nevoie sa se refere
                doar anumite pct-uri din chitanta asta, ceea ce inseamna ca suma de impartit poate fi mai mica decat
                suma de pe chitanta
        """

        # gaseste ultimul trimestru inregistrat pentru membru
        trimestru_initial, plati_partiale = membru.get_ultimul_trimestru_cotizatie(return_plati_partiale=True)

        #   inițializări (chitanta poate fi None pentru simulari)
        if chitanta:
            diff = 0
            if chitanta_partial:
                #   calculeaza suma de pe PCT-uri existente si scade-o din chitanta.suma
                suma_dict = PlataCotizatieTrimestru.objects.filter(membru=membru, chitanta=chitanta).aggregate(Sum("suma"))
                diff = suma_dict["suma__sum"]
            suma = chitanta.suma - diff

        logger.debug("calculeaza_acoperire: calcul acoperire start")

        trimestru_curent = trimestru_initial
        trimestru_plata_completa = trimestru_curent
        plati = []
        index = 0

        #   sparge suma pe câte trimestre se poate
        while suma > 0:
            plateste_cotizatia_trimestru = membru.plateste_cotizatie(trimestru_curent)
            if plateste_cotizatia_trimestru:
                cotizatie_trimestru_nominal = trimestru_curent.identifica_cotizatie(membru)
                cotizatie_trimestru = membru.aplica_reducere_familie(cotizatie_trimestru_nominal, trimestru_curent)
            else:
                #   skip calcul pentru trimestrul asta
                trimestru_curent = Trimestru.urmatorul_trimestru(trimestru=trimestru_curent)
                continue

            logger.debug("calculeaza_acoperire: acoperire trimestru pentru %s, nominal %s RON, procesat %s RON" % (membru, cotizatie_trimestru_nominal, cotizatie_trimestru))

            #   suma, final si partial rezolva problemele platilor partiale, in toate scenariile
            #   o singura plata partiala
            #   mai multe plati finale si una potential partiala
            #   o plata finala care completeaza un trimestru

            plata_kwargs = {"trimestru": trimestru_curent,
                            "partial": suma - cotizatie_trimestru < 0,
                            "suma": cotizatie_trimestru if suma >= cotizatie_trimestru else suma,
                            "membru": membru,
                            "chitanta": chitanta,
                            "final": not (suma - cotizatie_trimestru < 0)}

            if plati_partiale:
                suma_colectata = plati_partiale.aggregate(Sum("suma"))['suma__sum']
                if suma >= cotizatie_trimestru - suma_colectata:
                    plata_kwargs['suma'] = cotizatie_trimestru - suma_colectata
                    plata_kwargs['final'] = True
                else:
                    plata_kwargs['suma'] = suma
                    plata_kwargs['final'] = False
                plata_kwargs['partial'] = True
                suma = suma - cotizatie_trimestru + suma_colectata
                plati_partiale = None
            else:
                suma = suma - cotizatie_trimestru

            plata_kwargs['index'] = index
            plata = cls(**plata_kwargs)
            plati.append(plata)
            if plata.final:
                trimestru_plata_completa = trimestru_curent

            trimestru_curent = Trimestru.urmatorul_trimestru(trimestru=trimestru_curent)
            index += 1

        #   verifica status
        today = datetime.date.today()
        trimestru_azi = Trimestru.trimestru_pentru_data(today)

        #   se calculeaza cum va schimba plata statusul membrului fata de datorie
        #   daca am trimestrele 1 2 3 4, 4 - 1 - 1 va fi 0, ceea ce duce la acoperire completa
        diff = trimestru_azi.ordine_globala - trimestru_plata_completa.ordine_globala - 1

        #   daca avem DOAR o plata partiala, inseamna ca nu s-a schimbat de fapt nimic, nu exista
        #   avansare in calculul statusului, deci trebuie compensat
        if trimestru_initial == trimestru_plata_completa and plata and not plata.final:
            diff += 1

        #   implementare pentru perioada de gratie de 15 zile la sfarsitul fiecarui trimestru
        if not trimestru_azi.data_in_trimestru(today - datetime.timedelta(days=15)):
            diff -= 1

        if commit:
            for plata in plati:
                plata.save()

            #   daca exista plati incomplete pentru trimestrul asta de la membri ai familiei
            #   recalculeaza platile pentru trimestru avand in vedere ca s-ar putea sa se fi
            #   modificat pozitia in ierarhia de reduceri pentru unii din ei
            logger.debug("calculeaza_acoperire: recalculez acoperire pentru familie")
            cls.recalculeaza_pentru_familie(membru=membru, plati=plati, membri_procesati=membri_procesati)

        return plati, suma, membru.status_cotizatie(for_diff=diff), diff

    @classmethod
    def recalculeaza_pentru_familie(cls, membru, plati, membri_procesati=[]):
        logger.debug("recalculeaza_pentru_familie: familie: %s" % membri_procesati)
        from structuri.models import AsociereMembruFamilie
        familie = AsociereMembruFamilie.rude_cercetasi(membru, exclude_self=True)
        familie = [m for m in familie if m not in membri_procesati]
        #   exclude de la reducerea de membrii de familie membrii de familie care au cotizatie sociala trimestrul asta
        trimestre = []
        for p in [p for p in plati if p.final is True]: #plati.filter(final=True):
            if p.trimestru not in trimestre:
                trimestre.append(p.trimestru)

        for trimestru in trimestre:
            familie_trimestru = [m for m in familie if not m.are_cotizatie_sociala(trimestru)]
            for m in familie_trimestru:
                plati = PlataCotizatieTrimestru.objects.filter(trimestru=trimestru, membru=m)
                plati_finale = plati.filter(final=True)
                if plati.count() and plati_finale.count() == 0:
                    logger.debug("recalculeaza_pentru_familie: recalculare pentru %s, %s" % (m, trimestru))
                    #   exista plati, dar nu exista o plata finala
                    #   daca suma platilor este mai mare decat datoria
                    #   trebuie reimpartita suma, sau (in caz de egalitate) bifata ca finala ultima inregistrare
                    m.recalculeaza_acoperire_cotizatie(trimestru_start=trimestru, membri_procesati=membri_procesati)

    def __str__(self):
        return u"Plată pentru %s, pe %s, în valoare de %.2f RON" % (self.membru, self.trimestru, self.suma)


class ChitantaCotizatie(Chitanta):
    registre_compatibile = ["chitantier", "intern"]
    predat = models.BooleanField(default=False)
    blocat = models.BooleanField(default=False)

    def save(self, **kwargs):
        self.tip_document, created = TipDocument.objects.get_or_create(slug="cotizatie")
        if created:
            self.tip_document.nume = u"Chitanță cotizație"
            self.tip_document.save()
        return super(ChitantaCotizatie, self).save(**kwargs)

    @classmethod
    def pentru_membru(cls, membru=None, tip_document="cotizatie"):
        return Chitanta.pentru_membru(membru=membru, tip_document=tip_document)

    def editabila(self):
        return not (self.blocat or self.printata)

    def delete(self, **kwargs):
        self.platacotizatietrimestru_set.all().delete()
        return super(ChitantaCotizatie, self).delete(**kwargs)


REGISTRU_MODES = (("auto", u"Automat"), ("manual", u"Manual"))
REGISTRU_TIPURI = (("chitantier", u"Chitanțier"), ("facturier", u"Facturier"), ("io", u"Registru intrări / ieșiri"),
                   ("intern", u"Registru intern"))


class Registru(models.Model):
    centru_local = models.ForeignKey("structuri.CentruLocal", on_delete=models.CASCADE)
    owner = models.ForeignKey("structuri.Membru", null=True, blank=True, on_delete=models.CASCADE)

    mod_functionare = models.CharField(default="auto", max_length=255, choices=REGISTRU_MODES,
                                       verbose_name=u"Tip numerotare",
                                       help_text=u"Registrul cu numerotare automată își gestionează singur numerele de înregistrare")
    tip_registru = models.CharField(max_length=255, choices=REGISTRU_TIPURI)

    #   documentul care a generat crearea registrului, spre exemplu deciziile de atribuire de numar
    document_referinta = models.ForeignKey(Document, null=True, blank=True, related_name="registru_referinta", on_delete=models.SET_NULL)
    serie = models.CharField(max_length=255, null=True, blank=True)

    #   numere inregistrare
    numar_inceput = models.IntegerField(default=1)
    numar_sfarsit = models.IntegerField(null=True, blank=True)
    numar_curent = models.IntegerField()

    valabil = models.BooleanField(default=True)
    editabil = models.BooleanField(default=True)
    data_inceput = models.DateTimeField(auto_now_add=True)
    descriere = models.TextField(null=True, blank=True, help_text=u"Un scurt text de descriere pentru registru")

    def save(self, **kwargs):
        if not self.numar_curent:
            self.numar_curent = self.numar_inceput

        if self.numar_sfarsit and self.numar_curent > self.numar_sfarsit:
            #   TODO: send email to Secretar Centru Local announcing him of this limitation
            self.valabil = False

        return super(Registru, self).save(**kwargs)

    def numere_ramase(self):
        if self.numar_sfarsit:
            return self.numar_sfarsit - self.numar_curent
        return 0

    def get_numar_inregistrare(self):
        if not self.valabil:
            raise ValueError(u"Seria este închisă")

        if self.mod_functionare != "auto":
            raise ValueError(u"Registrul cu numerotare manuală nu poate elibera numere de înregistrare")

        numar_curent = self.numar_curent
        self.numar_curent += 1
        if self.editabil:
            self.editabil = False
        self.save()
        return numar_curent

    def verifica_disponibilitate(self, numar):
        if not self.valabil:
            return False

        filter_kwargs = {"centru_local": self.centru_local,
                         "registru": self,
                         "numar_inregistrare": numar}
        documente_cnt = Document.objects.filter(**filter_kwargs).count()
        if documente_cnt:
            return False
        return True


    def get_document(self, numar):
        try:
            return self.document_set.get(numar_inregistrare=numar)
        except Document.DoesNotExist:
            return None

    # TODO: mai multe registre pot avea aceeasi serie atata vreme cat nu se intersecteaza
    #@classmethod
    #def get_document_cu_serie(cls, serie=None, numar=None):
    #    cls.objects.get(serie=serie).get_document(numar)

    def documente(self, **kwargs):
        documente = self.document_set.filter(**kwargs).order_by("-numar_inregistrare")
        return documente

    def delete(self, **kwargs):
        if not self.editabil:
            #   disallow deletion of
            return
        return super(Registru, self).delete(**kwargs)

    def __str__(self):
        return u"{0}, seria {1} ({2})".format(self.get_tip_registru_display(), self.serie, self.mod_functionare)


class DocumentCotizatieSociala(Document):
    nume_parinte = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"Nume părinte", help_text=u"Lasă gol pentru cercetași adulți") #  poate fi null pentru persoane peste 18 ani
    motiv = models.CharField(max_length=2048, null=True, blank=True)
    este_valabil = models.BooleanField(verbose_name=u"Cerere aprobată?", help_text=u"Bifează doar dacă cererea a fost aprobată de Consiliu", default=False)
    valabilitate_start = models.DateField()
    valabilitate_end = models.DateField(null=True, blank=True)

    registre_compatibile = ['io', ]

    def edit_link(self):
        return reverse("structuri:membru_cotizatiesociala_modifica", kwargs={"pk": self.id})

    def save(self, **kwargs):
        tip_document, created = TipDocument.objects.get_or_create(slug="declaratie-cotizatie-sociala")
        if created:
            tip_document.nume = u"Declarație cotizație socială"
            tip_document.save()
        self.tip_document = tip_document
        return super(DocumentCotizatieSociala, self).save(**kwargs)


@receiver(post_delete, sender=AsociereDocument)
def delete_documentcotizatie(sender, instance, **kwargs):
    if instance.document_ctype == ContentType.objects.get_for_model(DocumentCotizatieSociala):
        document = instance.document
        document.delete()


#   Implementare decizii
class Decizie(Document):
    registre_compatibile = ["intern", ]


    continut = models.TextField(null=True, blank=True)
    centru_local = models.ForeignKey("structuri.CentruLocal", on_delete=models.CASCADE)

    def save(self, **kwargs):
        self.tip_document, created = TipDocument.objects.get_or_create(slug="decizie", nume="Decizie")
        if created:
            self.tip_document.save()
        return super(Decizie, self).save(**kwargs)


CATEGORII_CUANTUM_COTIZATIE = (("local", u"Local"), ("national", u"Național"), ("local-social", u"Local (social)"),
                               ("national-social", u"Național (social)"))


class DecizieCotizatie(Decizie):
    registre_compatibile = ["intern", ]

    cuantum = models.FloatField(help_text=u"Valoare exprimată în RON pentru un an calendaristic (4 trimestre)")
    categorie = models.CharField(max_length=255, default="normal", choices=CATEGORII_CUANTUM_COTIZATIE)
    data_inceput = models.DateField()
    data_sfarsit = models.DateField(null=True, blank=True)

    def save(self, **kwargs):
        self.tip_document, created = TipDocument.objects.get_or_create(slug="decizie-cotizatie")
        if created:
            self.tip_document.nume = u"Decizie cuantum cotizație"
            self.tip_document.save()

        return super(DecizieCotizatie, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("documente:decizie_cuantum_detail", kwargs={"pk": self.id})

    @classmethod
    def get_package_for_centru_local(cls, centru_local=None, trimestru=None, social=False):
        categorii = ["local", "national"] if not social else ["local-social", "national-social"]
        valori_implicite = {"local": settings.VALOARE_IMPLICITA_COTIZATIE_LOCAL,
                            "national": settings.VALOARE_IMPLICITA_COTIZATIE_NATIONAL,
                            "local-social": settings.VALOARE_IMPLICITA_COTIZATIE_LOCAL_SOCIAL,
                            "national-social": settings.VALOARE_IMPLICITA_COTIZATIE_NATIONAL_SOCIAL}
        cuantum = {}
        for categorie in categorii:
            filtru = {"centru_local": centru_local,
                      "categorie": categorie,
                      "data_inceput__lte": trimestru.data_inceput}
            decizii = cls.objects.filter(**filtru).order_by("-data_inceput")
            cuantum[categorie.split("-")[0]] = decizii[0].cuantum if decizii.count() else valori_implicite.get(categorie)

        return cuantum


class DecizieRezervareNumere(Decizie):
    tip_rezervare = models.CharField(max_length=255, choices=REGISTRU_TIPURI)
    automat = models.BooleanField(default=True)
    numar_inceput = models.IntegerField()
    numar_sfarsit = models.IntegerField(null=True, blank=True)
    serie = models.CharField(max_length=255)
