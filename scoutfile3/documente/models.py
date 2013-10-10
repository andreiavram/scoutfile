# coding: utf-8
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
import datetime
from scoutfile3.settings import VALOARE_IMPLICITA_COTIZATIE_NATIONAL, VALOARE_IMPLICITA_COTIZATIE_LOCAL
# from scoutfile3.structuri.models import Membru

# Create your models here.

class Document(models.Model):
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    data_inregistrare = models.DateField(null = True, blank = True)
    numar_inregistrare = models.IntegerField(default=0)

    titlu = models.CharField(max_length = 1024)
    descriere = models.CharField(max_length = 2048, null = True, blank = True)
    
    fisier = models.FileField(upload_to = lambda instance, file_name: "declaratii/%s" % file_name, null = True, blank = True)
    url = models.URLField(max_length = 2048, null = True, blank = True)
    
    version_number = models.IntegerField(default = 0)
    root_document = models.ForeignKey("Document", related_name = "versions", null = True, blank = True)
    folder = models.ForeignKey("Document", related_name = "fisiere", null = True, blank = True)
    locked = models.BooleanField()
    
    is_folder = models.BooleanField()
    fragment = models.IntegerField(default = 0)
    
    uploader = models.ForeignKey(User)
    tip_document = models.ForeignKey("TipDocument", null = True, blank = True)
    
    def __unicode__(self):
        return u"%s" % self.titlu
    
    def referinta(self):
        return "%d / %s" % (self.id, self.data_inregistrare.strftime("%d.%m.%Y"))

    def edit_link(self):
        return ""
    
    def save(self, force_insert=False, force_update=False, using=None):
        if not self.data_inregistrare:
            self.data_inregistrare = self.date_created
        return super(Document, self).save(force_insert = force_insert, force_update = force_update, using = using)
    
# tagging.register(Document)

class TipAsociereDocument(models.Model):
    nume = models.CharField(max_length = 255)
    slug = models.CharField(max_length = 255, unique = True)
    
class AsociereDocument(models.Model):
    document = models.ForeignKey(Document)
    document_ctype = models.ForeignKey(ContentType, null = True, blank = True, related_name = "asociere")
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    tip_asociere = models.ForeignKey(TipAsociereDocument, null = True, blank = True)
    
    moment_asociere = models.DateTimeField(auto_now_add = True)
    responsabil = models.ForeignKey(User)
    
    def save(self, force_insert=False, force_update=False, using=None):
        self.document_ctype = ContentType.objects.get_for_model(self.document)
        return super(AsociereDocument, self).save(force_insert = force_insert, force_update = force_update,
                                                  using = using)
    def document_edit_link(self):
        return self.document_ctype.get_object_for_this_type(id=self.document.id).edit_link()

    @classmethod
    def inregistreaza(cls, document=None, to=None, tip=None, responsabil=None):
        tip_asociere, created = TipAsociereDocument.objects.get_or_create(slug="beneficiar-cotizatie-sociala")
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
    slug = models.CharField(max_length = 255)
    nume = models.CharField(max_length = 255)
    descriere = models.TextField(null = True, blank = True)

    def __unicode__(self):
        return u"{0}".format(self.nume)
    
class Chitanta(Document):
    casier = models.ForeignKey("structuri.Membru")
    serie = models.CharField(max_length = 255)
    numar = models.IntegerField(default = 0)
    suma = models.FloatField(default = 0)
    
    def save(self, force_insert=False, force_update=False, using=None):
        if not self.tip_document:
            self.tip_document = TipDocument.objects.get(slug = "chitanta")
        return super(Chitanta, self).save(force_insert = force_insert, force_update = force_update, using = using)
    
    def referinta(self):
        return "Seria %s, nr. %s / %s" % (self.serie, self.numar, self.date_created.strftime("%d.%m.%Y"))

class Decizie(Document):
    def save(self, force_insert=False, force_update=False, using=None):
        self.tip_document = TipDocument.objects.get(slug = "decizie")
        return super(Decizie, self).save(force_insert = force_insert, force_update = force_update, using = using)
      
class DecizieCotizatie(Decizie):
    cuantum = models.FloatField()
    categorie = models.CharField(max_length = 255, default = "normal")
    
class Trimestru(models.Model):
    data_inceput = models.DateField()
    data_sfarsit = models.DateField()
    ordine_locala = models.PositiveSmallIntegerField()
    ordine_globala = models.PositiveIntegerField()
    
    @classmethod
    def urmatorul_trimestru(cls, trimestru = None, offset = 1):
        if trimestru:
            try:
                return cls.objects.get(ordine_globala = trimestru.ordine_globala + 1)
            except cls.DoesNotExist:
                #    creaza un nou trimestru, presupunand ca exista un trimestru anterior
                trimestru_nou = Trimestru()
                trimestru_nou.ordine_globala = trimestru.ordine_globala + 1
                trimestru_nou.ordine_locala = trimestru.ordine_locala + 1 if trimestru.ordine_globala < 4 else 1
                
                an_nou = trimestru.data_sfarsit.year
                if trimestru.ordine_locala == 4:
                    an_nou += 1
                    
                #    trimestrul incepe in lunile 1, 4, 7 sau 10
                luna_noua = (trimestru_nou.ordine_locala - 1) * 3 + 1
                #    trimestru incepe in prima zi a primei luni din trimestu
                trimestru_nou.data_inceput = datetime.date(year = an_nou, month = luna_noua, day = 1)
                #    trimestul se termina cu o zi mai devreme decat prima zi a cele-i de-a 4 luni de la inceput
                #    un caz special este trimestrul IV, in care trebuie trecut in 1 ianuaire a anului urmator si scazuta o zi
                trimestru_nou.data_sfarsit = datetime.date(year = an_nou + trimestru_nou.ordine_locala / 4, 
                                                           month = luna_noua + 3 if luna_noua < 10 else 1, 
                                                           day = 1) - datetime.timedelta(days = 1)
                trimestru_nou.save()
                return trimestru_nou

        #    trimestrul de inceput pentru toate record-urile hardcodat aici
        #    pentru primul trimestru cu noua cotizatie (1 octombrie 2011)
        
        if Trimestru.objects.all().count():
            raise ValueError("Metoda __urmatorul trimestru__ trebuie apelata cu un parametru trimestru")
            
        trimestru_nou = Trimestru()
        trimestru_nou.ordine_locala = 4
        trimestru_nou.ordine_globala = 1
        trimestru_nou.data_inceput = datetime.date(year = 2011, month = 10, day = 1)
        trimestru_nou.data_sfarsit = datetime.date(year = 2012, month = 1, day = 1) - datetime.timedelta(days = 1)
        trimestru_nou.save()
        return trimestru_nou
         
    @classmethod
    def trimestru_pentru_data(cls, data):
        try:
            return cls.objects.get(data_inceput__lte = data,
                                         data_sfarsit__gte = data)
        except cls.DoesNotExist:
            return None
    
    def data_in_trimestru(self, data):
        return (self.data_inceput <= data) and (self.data_sfarsit >= data) 
    
    def identifica_cotizatie(self, membru):
        """ Identifica valoarea cotizatiei pentru acest membru,
        pentru acest trimestru
        """
        # TODO: implement this
        
        #    identifica cotizatie globala (ONCR)
        #    identifica cotizatei Centru Local
        #    aplica valori implicite daca nu gasesti
        #    intoarce suma trimestriala
        #    cauta sa vezi daca exista cotizatie redusa
        decizie_kwargs = {"content_type" : ContentType.objects.get_for_model(membru.centru_local) ,
                          "object_id" : membru.centru_local.id,
                          "document__tip_document__slug__iexact" : "decizie-cotizatie" }
        
        asocieri = AsociereDocument.objects.filter(**decizie_kwargs).order_by("-moment_asociere")
        asocieri_ids = [a.id for a in asocieri]
        
        cotizatie_sociala = membru.are_cotizatie_sociala()
        tip = {"id__in" : asocieri_ids,
               "categorie": "social-local" if cotizatie_sociala else "normal-local" }            
        decizii = DecizieCotizatie.objects.filter(**tip).order_by("-data_inregistrare")[:1]
        if decizii.count() == 0:
            valoare_cotizatie_local = VALOARE_IMPLICITA_COTIZATIE_LOCAL
        else:
            valoare_cotizatie_local = decizii[0].cuantum
            
        tip = {"categorie" : "social-national" if cotizatie_sociala else "normal-national"}
        decizii = DecizieCotizatie.objects.filter(**tip).order_by("-data_inregistrare")[:1]
        if decizii.count() == 0:
            valoare_cotizatie_national = VALOARE_IMPLICITA_COTIZATIE_NATIONAL
        else:
            valoare_cotizatie_national = decizii[0].cuantum
        
            
        valoare_lunara = valoare_cotizatie_national / 4. + valoare_cotizatie_local / 4.
        return valoare_lunara

MOTIVE_INREGISTRARE_PLATA_COTIZATIE = (("normal", u"Plată normală"), ("inactiv", "Inactiv"))
class PlataCotizatieTrimestru(models.Model):
    trimestru = models.ForeignKey(Trimestru)
    partial = models.BooleanField()
    final = models.BooleanField()
    suma = models.FloatField()
    membru = models.ForeignKey("structuri.Membru")
    chitanta = models.ForeignKey("ChitantaCotizatie")
    
    tip_inregistrare = models.CharField(max_length = 255, choices = MOTIVE_INREGISTRARE_PLATA_COTIZATIE, default = "normal")
    
    @classmethod
    def calculeaza_acoperire(cls, membru, chitanta = None, suma = None, commit = False):
        """ Sparge plata de pe o chitanta in asocierile necesare pentru plati 
        trimestriale pentru un membru, cu plati partiale unde este nevoie.
        
        @param membru: membrul pentru care se fac platile
        @param chitanta: chitanta pe baza careia se fac estimarile (posibil sa nu existe la momentul unei simulari)
        @param commit: daca se salveaza sau nu obiectele create (False == simulare)
        """

        # gaseste ultimul trimestru inregistrat pentru membru
        plati_membru = membru.platacotizatietrimestru_set.all().order_by("-trimestru__ordine_global")
        plata_partiala = None
        if plati_membru.count() == 0:
            trimestru_initial = membru.get_trimestru_initial_cotizatie()
        elif plati_membru[0].partial and not plati_membru[0].final:
            trimestru_initial = plati_membru[0].trimestru
            plata_partiala = plati_membru[0]
        else:
            trimestru_initial = Trimestru.urmatorul_trimestru(plati_membru[0].trimestru)
        
        if chitanta:
            suma = chitanta.suma
            
        trimestru_curent = trimestru_initial
        plati = []
        while suma > 0:
            cotizatie_trimestru_nominal = trimestru_curent.identifica_cotizatie(membru)
            cotizatie_trimestru = membru.aplica_reducere_familie(cotizatie_trimestru_nominal, trimestru_curent)

            plata_kwargs = {"trimestru" : trimestru_curent,
                            "partial" : suma - cotizatie_trimestru < 0,
                            "suma" : cotizatie_trimestru if suma >= cotizatie_trimestru else suma,
                            "membru" : membru,
                            "chitanta" : chitanta,
                            "final" : not (suma - cotizatie_trimestru < 0) }
                        
            if plata_partiala:
                if suma >= cotizatie_trimestru - plata_partiala.suma:
                    plata_kwargs['suma'] = cotizatie_trimestru - plata_partiala.suma
                    plata_kwargs['final'] = True
                else:
                    plata_kwargs['suma'] = suma
                    plata_kwargs['final'] = False
                plata_kwargs['partial'] = True
                suma = suma - cotizatie_trimestru + plata_partiala.suma
                plata_partiala = None
            else:
                suma = suma - cotizatie_trimestru
            
            plata = cls(**plata_kwargs)
            plati.append(plata)
            
        if commit:
            for plata in plati:
                plata.save()
                
        return plati
        
class ChitantaCotizatie(Chitanta):
    def save(self, force_insert=False, force_update=False, using=None):
        self.tip_document = TipDocument.objects.get(slug = "cotizatie")
        return super(ChitantaCotizatie, self).save(force_insert = force_insert, force_update = force_update, using = using)
    
class SerieDocument(models.Model):
    cod_unic = models.CharField(max_length = 255)
    numar_inceput = models.IntegerField()
    numar_sfarsit = models.IntegerField()
    numar_curent = models.IntegerField(null = True, blank = True)
    
    document_referinta = models.ForeignKey(Document, null = True, blank = True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    deschisa = models.BooleanField(default = True)
    data_inceput = models.DateTimeField(auto_now_add = True)
    
    def save(self, force_insert=False, force_update=False, using=None):
        if not self.numar_curent:
            self.numar_curent = self.numar_inceput
        return super(SerieDocument, self).save(force_insert = force_insert, force_update = force_update,
                                               using = using)
        
    def get_next_item(self):
        if not self.deschisa:
            raise ValueError(u"Seria aceasta este epuizată")
        
        numar_curent = self.numar_curent
        if self.numar_curent == self.numar_sfarsit:
            self.deschisa = False
            self.save()
        return numar_curent
        
class DocumentCotizatieSociala(Document):
    nume_parinte = models.CharField(max_length = 255, null = True, blank = True, verbose_name = u"Nume părinte", help_text = u"Lasă gol pentru cercetași adulți") #  poate fi null pentru persoane peste 18 ani
    motiv = models.CharField(max_length = 2048, null = True, blank = True)
    este_valabil = models.BooleanField(verbose_name = u"Este valabilă?", help_text=u"Bifează doar dacă cererea a fost aprobată de Consiliu")

    def edit_link(self):
        return reverse("structuri:membru_cotizatiesociala_modifica", kwargs={"pk":self.id})

    def save(self, **kwargs):
        self.tip_document, created = TipDocument.objects.get_or_create(slug = "declaratie-cotizatie-sociala")
        if created:
            self.tip_document.save()
        return super(DocumentCotizatieSociala, self).save(**kwargs)

ctype_deciziecotizatie = ContentType.objects.get_for_model(DecizieCotizatie)    