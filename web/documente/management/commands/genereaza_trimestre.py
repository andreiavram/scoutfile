#   coding: utf8
from django.core.management.base import BaseCommand

from documente.models import Trimestru

__author__ = 'andrei'

import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if Trimestru.objects.all().count():
            self.stdout.write(u"Există deja trimestre generate, nu pot să regenerez!")
            return

        t = Trimestru(data_inceput = datetime.date(year = 1991, month = 1, day = 1),
                  data_sfarsit = datetime.date(year = 1992, month = 3, day = 31),
                  ordine_locala = 1,
                  ordine_globala = 1)
        t.save()

        while t.data_inceput.year < datetime.date.today().year + 2:
            t = Trimestru.urmatorul_trimestru(trimestru=t)


