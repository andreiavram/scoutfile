#   coding: utf8
from django.core.management.base import BaseCommand
import traceback
from adrese_postale.adrese import AdresaPostalaException, AdresaPostala
from adrese_postale.models import CodPostal
from structuri.models import Membru

__author__ = 'andrei'

import datetime
from django.conf import settings
import os


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # if len(args) < 1:
        #     self.stdout.write("Usage ./manage.py obtine_cod <address>\n")
        #     return

        cod = CodPostal.get_cod_pentru_adresa(u"Str. Cornișei, bl. GA9, Slatina, jud. Olt")
        adrs = [#"Str. Principala, nr. 25, sat teleac, com. ciugud, jud. alba",
                #"B-dul. Transilvaniei, nr. 25, bl. 3CD, sc. 1, ap. 22, Alba Iulia, jud. Alba",
                #"Str. Octavian Goga, nr. 12, Alba Iulia, jud. Alba",
                #"Str. Traian, Nr. 27C, Alba Iulia, jud. Alba",
                #"Str. Alexandru Ioan Cuza, Nr. 6A, Alba Iulia, jud. Alba",
                "Sat Drâmbar, Nr. 106, comuna Ciugud, jud. Alba",
                "Str. Republicii, Nr. 22A, Ap. 5, Cluj-Napoca, jud. Cluj",
                u"Calea Moţilor, Nr. 99, Bl. M2, Sc. C, Ap. 17, Alba Iulia"]
        for a in adrs:
            adr = AdresaPostala.parse_address(a)
            adr.set_cod(CodPostal.get_cod_pentru_adresa(adr).cod_postal)
            print u"%s" % adr
            print u"%s" % adr.__unicode__()

        # self.stdout.write("%s\n" % cod)

        # coduri_valide = 0
        # l = [m for m in Membru.objects.all() if m.centru_local and m.centru_local.id == 1]
        # for m in l:
        #     try:
        #         cod = CodPostal.get_cod_pentru_adresa(m.adresa_postala)
        #     except AdresaPostalaException, e:
        #         # print u"ADRESA GRESITA"
        #         cod = None
        #     except Exception, e:
        #         cod = None
        #         print u"%s / %s" % (e, traceback.format_exc())
        #
        #     if cod is not None:
        #         coduri_valide += 1
        #         # self.stdout.write("%s\n" % cod)
        #
        # self.stdout.write("%d coduri valide din %d \n\n" % (coduri_valide, len(l)))
