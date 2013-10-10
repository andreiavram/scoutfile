# coding: utf-8
from django.db import models
from structuri.models import InformatieContact, TipInformatieContact,\
    Membru
from django.contrib.contenttypes.models import ContentType
import datetime
from django.db.models.query_utils import Q
import logging
from django.contrib.contenttypes.generic import GenericForeignKey
from settings import SMSLINK_CONNID, SMSLINK_PASSWORD, SMSLINK_URL,\
    DEBUG
import urllib
import urllib2
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)

# Create your models here.

ERROR_CODES = { 1 : ("Insufficient arguments for gateway", "Acest mesaj de eroare atunci cand parametrii trimisi spre gateway, fie ei prin metoda GET sau POST sunt insuficienti. Trebuie sa fiti siguri ca apelarea dumneavoastra contine parametrii connection_id, reprezentand ID-ul conexiunii dumneavoastra pe care il gasiti la sectiunea Configurare cont si password, reprezentand parola pentru acel ID de conectare."),
     2 : ("Connection ID is not approved!", "Acest mesaj de eroare apare atunci cand Connection ID-ul trimis ca argument, connection_id, nu exista. Fiecare IP are un Connectiun ID, iar pentru adaugarea si configurarea unui Connection ID nou / IP nou va rugam accesati sectiunea Configurare serviciu din cadrul SMS Gateway."),
     3 : ("This username is suspended or inactive!", "Acest mesaj apare atunci cand numele de utilizator general al contului este suspendat sau inactiv din diferite motive. In acest context nu este activ nici unul din serviciile SMSLink.ro pentru acest nume de utilizator. In vederea solutionari acestei probleme va rugam sa ne contactati prin e-mail."),
     4 : ("Service is not active for this account!", "Acest mesaj apare atunci cand serviciul SMS Gateway nu a fost activat pentru contul dumneavoastra. In vederea activarii serviciului va rugam accesati optiunea Activare din cadrul SMS Gateway. Activarea se va face de regula in 48 de ore lucratoare de la trimiterea cererii."),
     5 : ("IP address is not allowed!", "Acest mesaj apare atunci cand IP-ul de pe care incercati sa trimiteti mesaje catre SMS Gateway nu este autorizat. Pentru solutionarea problemei este nevoie sa adaugati IP-ul in lista IP-urilor permise in sectiunea Configurare serviciu din cadrul SMS Gateway."),
     6 : ("IP address banned because of failed authentifications!", "Acest mesaj de eroare aparea atunci cand IP-ul dumneavoastra autorizat a fost blocat din cauza autentificarilor gresite repetate. Pentru activarea sa trebuie accesata optiunea Configurare serviciu din cadrul SMS Gateway si urmati pasii de activare."),
     7 : ("Password is not approved!", "Acest mesaj de eroare va aparea atunci cand parola trimisa spre SMS Gateway este incorecta. Introducerea repetata de parole gresite poate duce la blocarea IP-ului de conectare, in functie de setarile din contul dumneavoastra."),
     8 : ("Credit is not availabile!", "Acest mesaj de eroare va aparea atunci cand creditul nu este suficient pentru trimiterea mesajelor. Pentru solutionarea problemei va rugam sa va incarcati creditul contului prin optiunea Cumpara credit disponibila in contul dumneavoastra.."),
     9 : ("Mobile number must have 10 numeric characters!", "Acest mesaj de eroare apare atunci cand numarul de telefon de destinatie trimis prin parametrul to nu contine 10 caractere. Numerele de telefon trebuie introduse in format numeric de 10 caractere, exemplu: 0722123456."),
     10 : ("Receiver number is not a mobile number!", "Acest mesaj de eroare apare atunci cand numarul trimis prin parametrul to nu este un numar valid de mobil. Numerele de mobil trebuie sa inceapa cu prefixul 07 si sa apartina unui operator mobil din Romania, Vodafone, Orange, Cosmote sau Zapp."),
     11 : ("Message cannot be left blank!", "Acest mesaj de eroare apare atunci cand parametrul message are lungimea de 0 caractere. Mesajele SMS trimise trebuie sa contina mai mult de 0 caractere."),
     12 : ("Message is larger than 160 characters!", "Acest mesaj de eroare apare atunci cand parametrul message are lungimea de mai mare de 160 de caractere. Mesajele SMS trimise nu pot avea lungimea mai mare de 160 de caractere."),
     13 : ("Sender ID is not allowed!", "Acest mesaj de eroare apare atunci cand Sender ID-ul trimis prin parametrul sender nu este aprobat. In vederea trimiterii de mesaje cu sender personalizat este nevoie de acordul prealabil al operatorior, iar in acest sens va rugam sa folositi formularul de cerere de sender personalizat din contul dumneavoastra."),
     14 : ("Mode is not known!", "Acest mesaj de eroare apare atunci cand parametrul optional mode nu este cunoscut. In vederea detalierii acestui parametru va rugam sa cititi documentatia."),
     15 : ("Sending timestamp is too close to now!", "Acest mesaj de eroare apare atunci cand trimiteti un mesaj pe care oriti sa il programati la o anumita data iar data programarii este in trecut sau mai aproape de 1 zi de data curenta."),
     16 : ("An error has occured during sending!", "Acest mesaj de eroare apare atunci cand o alta problema este detectata. In vederea solutionarii acestei posibile erori va rugam sa ne contactati prin mijloacele puse la dispozitie pe site.")}



class SMSMessage(models.Model):
    expeditor = models.ForeignKey("structuri.Utilizator")
    destinatar = models.CharField(max_length = 1024)
    mesaj = models.CharField(max_length = 1024, null = True, blank = True)
    
    cod_referinta_smslink = models.IntegerField()
    timestamp_trimitere = models.DateTimeField(null = True, blank = True)
    timestamp_confirmare = models.DateTimeField(null = True, blank = True)
    
    confirmat = models.BooleanField()
    eroare_trimitere = models.CharField(max_length = 1024, null = True, blank = True)
    eroare_confirmare = models.CharField(max_length = 1024, null = True, blank = True)
    
    sender = models.CharField(max_length = 255, null = True, blank = True)
    credit = models.ForeignKey("Credit", null = True, blank = True)
    
    cod_grup = models.CharField(max_length = 255, null = True, blank = True) #    fixes #42
    
    def get_err_data(self):
        if not self.eroare_trimitere:
            return None
        
        try:
            return ERROR_CODES.get(int(self.eroare_trimitere))
        except Exception:
            return None
    
    def resolve_destinatar(self):
        try:
            tip_informatie = TipInformatieContact.objects.filter(nume__icontains = "mobil")
            data = InformatieContact.objects.filter(tip_informatie__in = tip_informatie,
                                             content_type = ContentType.objects.get_for_model(Membru),
                                             valoare = self.destinatar)
            data = data.filter(Q(data_end__isnull = True) | Q(data_end__gte = datetime.datetime.now()))
            
            if data.count():
                return data[0].content_object
        except Exception, e:
            logger.error("%s: Exceptie la resolvarea destinatarului %s" % (self.__class__.__name__, e))
            return None
        
        return None
    
    @classmethod
    def send_message(cls, mode, expeditor = None, destinatar = None, mesaj_text = None, credit = None, grup_id = None):
        #    TODO: perform basic checks
        #    TODO: check msg length
        #    TODO: check number validity
        #    TODO: check if we still have enough credit
    
        if mode not in ("credit", "sms"):
            raise ValueError(u"%s: Parametrul mode trebuie sa fie 'credit' sau 'sms'" % cls.__name__)
        if mode in ("sms", ) and any(x == None for x in (expeditor, destinatar, mesaj_text)):
            raise ValueError(u"%s: Parametrii expeditor, destinatar si mesaj sunt obligatorii in modul 'sms'" % cls.__name__)
            
        values =  {"connection_id" :  SMSLINK_CONNID,
                "password" : SMSLINK_PASSWORD }
        
        if mode == "sms":
            values.update({"message" : mesaj_text,
                "to" : destinatar})
            
        if mode == "credit":
            values.update({"mode" : "credit"})
            
        if DEBUG:
            values.update({"test" : "1"})
        
        data = urllib.urlencode(values)
        url_to_send = SMSLINK_URL + "?" + data
        #logger.debug("%s: url: %s" % (cls.__name__, url_to_send))
        
        try:
            response = urllib2.urlopen(url_to_send)
        except Exception, e:
            logger.error("%s: eroare la trimiterea unui mesaj: %s" % (cls.__name__, e))
            raise Exception(u"Eroare la trimiterea mesajului!")
        
        response_text = response.read()
        response_elements = response_text.split(";")
        
        if mode == "credit": 
            if response_elements[0] == "MESSAGE" and int(response_elements[1]) == 2:
                rezultate = response_elements[3].split(",")
                credit_sms = int(rezultate[0])
                return credit_sms
            else:
                logger.error(u"%s: Probleme la trimiterea mesajului: %s" % (cls.__name__, response_elements))
        mesaj = cls()
        mesaj.cod_grup = grup_id
        success = False
        if response_elements[0] == "MESSAGE":
            if int(response_elements[1]) == 1:
                # Mesaj success
                rezultate = response_elements[3].split(",")
                mesaj.cod_referinta_smslink =  int(rezultate[0])
                mesaj.sender = rezultate[2]
                success = True
        elif response_elements[0] == "ERROR":
            mesaj.eroare_trimitere = int(response_elements[1])
            
        mesaj.expeditor = expeditor
        mesaj.destinatar = destinatar
        mesaj.mesaj = mesaj_text
        mesaj.timestamp_trimitere = datetime.datetime.now()
        if credit:
            mesaj.credit = credit
        mesaj.save()
        
        if success:
            Credit.sync_system_credit()
            
        
        logger.debug("%s: Response: %s" % (cls.__name__, response.read()))
        return mesaj

class Credit(models.Model):
    content_type = models.ForeignKey(ContentType, null = True, blank = True, verbose_name = "Clasă")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    credit = models.IntegerField()
    epuizat = models.BooleanField()
    
    timestamp = models.DateTimeField(auto_now_add = True)
    creat_de = models.ForeignKey("structuri.Utilizator", null = True, blank = True)
    comentarii = models.TextField(null = True, blank = True)
    
    tip = models.CharField(max_length  = 2, choices = ((1, "Real"), (2, "Intern")))
    
    def credit_ramas(self):
        credit_consumat = self.smsmessage_set.all().count()
        return self.credit - credit_consumat
    
    def credit_rezervat(self):
        return self.rezervarecredit_set.all().count()
    
    def credit_disponibil(self):
        return self.credit_ramas() - self.credit_rezervat() 
    
    @classmethod
    def set_system_credit(cls, new_credit):
        try:
            credit = cls.objects.get(content_type__isnull = True, tip = 1)
            if credit.credit != new_credit:
                credit.credit = new_credit
                credit.save()
        except cls.DoesNotExist:
            credit = cls()
            credit.credit = new_credit
            credit.tip = 1
            credit.object_id = 0
            credit.save()
        except cls.MultipleObjectsReturned:
            cls.objects.filter(content_type__isnull = True, tip = 1).delete()
            cls.sync_system_credit()
    
    @classmethod
    def sync_system_credit(cls):
        credit = SMSMessage.send_message("credit")
        cls.set_system_credit(credit)
        return credit
    
    @classmethod
    def get_system_credit(cls):
        try:
            return cls.objects.get(content_type__isnull = True, tip = 1).credit
        except cls.DoesNotExist:
            return cls.sync_system_credit()
        except cls.MultipleObjectsReturned:
            cls.objects.filter(content_type__isnull = True, tip = 1).delete()
            return cls.sync_system_credit()
        except Exception, e:
            logger.error("%s: get_system_credit : %s" % (cls.__name__, e))
            return 0

        
@receiver(post_save, sender = SMSMessage)
def check_credit_epuizat(sender, instance, **kwargs):
    if all([instance.credit, instance.credit.credit_ramas() == 0, not instance.credit.epuizat]):
        instance.credit.epuizat = True
        instance.credit.save()
        
class RezervareCredit(models.Model):
    credit = models.ForeignKey(Credit)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    timestamp = models.DateTimeField(auto_now_add = True)        
    