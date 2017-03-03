#   coding: utf8
from django.core.management.base import BaseCommand

from adrese_postale import CodPostal

__author__ = 'andrei'

from django.conf import settings
import os


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        CodPostal.objects.all().delete()

        with open(os.path.join(settings.BASE_DIR, "scoutfile3", "adrese_postale", "data", "coduri_postale.csv")) as f:
            lines = f.readlines()


        def clean_elm(elm):
            txt = elm.strip().strip("\n")
            if len(txt):
                return txt
            return None

        for l in lines:
            elms = l.split("|")
            cp_dict = {
                "cod_postal": clean_elm(elms[5]),
                "judet": clean_elm(elms[0]),
                "localitate": clean_elm(elms[1]),
                "tip_strada": clean_elm(elms[2]),
                "strada": clean_elm(elms[3]),
                "sector": clean_elm(elms[6]),
                "descriptor": clean_elm(elms[4]),
            }
            CodPostal.objects.create(**cp_dict)