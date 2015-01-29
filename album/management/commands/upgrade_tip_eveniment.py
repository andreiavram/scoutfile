# coding: utf-8
'''
Created on Sep 8, 2013

@author: yeti
'''

from django.core.management.base import BaseCommand
import logging

from album.models import Eveniment, TipEveniment
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for e in Eveniment.objects.all():
            if e.tip_eveniment_text is None:
                e.tip_eveniment_text = "alta"
            tip_eveniment, created = TipEveniment.objects.get_or_create(nume=e.get_tip_eveniment_text_display(), slug=e.tip_eveniment_text)
            if created:
                tip_eveniment.save()

            e.tip_eveniment = tip_eveniment
            e.save()