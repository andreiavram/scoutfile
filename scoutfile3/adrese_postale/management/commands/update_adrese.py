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
        #   pentru fiecare membru care are adresa
        #   prelucreaza adresa, vezi daca-i ok
        #   daca nu are cod, cauta-i codul, adauga si salveaza (?)
        pass