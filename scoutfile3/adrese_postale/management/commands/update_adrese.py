#   coding: utf8
from django.core.management.base import BaseCommand
import traceback
from adrese_postale.adrese import AdresaPostalaException, AdresaPostala
from adrese_postale.models import CodPostal
from structuri.models import Membru, InformatieContact

__author__ = 'andrei'

import datetime
from django.conf import settings
import os


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        #   pentru fiecare membru care are adresa
        #   prelucreaza adresa, vezi daca-i ok
        #   daca nu are cod, cauta-i codul, adauga si salveaza (?)
        infos = InformatieContact.objects.filter(tip_informatie__nume__iexact=u"Adresa corespondență")

        new_codes = 0

        for info in infos:
            try:
                adresa = AdresaPostala.parse_address(info.valoare, fail_silently=False)
            except Exception, e:
                continue

            if not adresa.are_cod():
                adresa.determine_cod()

                if adresa.are_cod():
                    info.valoare = adresa.__unicode__()
                    # self.stdout.write(u"info to save: %s\n" % info.valoare)
                    new_codes += 1
                else:
                    self.stdout.write("could not determine code\n")


        self.stdout.write("%d new codes\n" % new_codes)

