# coding: utf-8
'''
Created on Sep 8, 2013

@author: yeti
'''
from datetime import datetime

from django.core.management.base import BaseCommand
import logging

from album.models import Eveniment, TipEveniment
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        evenimente = Eveniment.objects.filter(status="confirmat", start_date__lte=datetime.now())
        for e in evenimente:
            if e.end_date <= datetime.now():
                e.status = "derulare"
            else:
                e.status = "terminat"
            e.save()

        evenimente = Eveniment.objects.filter(status="derulare", end_date__gte=datetime.now())
        for e in evenimente:
            e.status = "terminat"
            e.save()

        evenimente = Eveniment.objects.filter(status__isnull=True)
        for e in evenimente:
            if e.start_date > datetime.now():
                if e.end_date <= datetime.now():
                    e.status = "derulare"
                else:
                    e.status = "terminat"

