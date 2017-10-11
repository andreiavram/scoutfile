# coding: utf-8

import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from album.models import Eveniment, ParticipareEveniment
from structuri.models import CentruLocal


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            slug = args[0]
            eveniment = Eveniment.objects.get(slug=args[0])
        except IndexError as e:
            self.stderr.write("Need target AG event slug\n")
        except Eveniment.DoesNotExist as e:
            self.stderr.write("Cannot get AG event for slug '%s'" % slug)

        cl = CentruLocal.objects.get(id=settings.CENTRU_LOCAL_IMPLICIT)
        membri = cl.cercetasi(qs=False)
        membri_ag = [m for m in membri if m.drept_vot_teoretic()]

        for m in membri_ag:
            ParticipareEveniment.objects.create(membru=m, eveniment=eveniment, data_sosire=eveniment.start_date, data_plecare=eveniment.end_date,
                                                status_participare=1, detalii=u"adăugat automat")

        self.stdout.write(u"Added %d people to event\n" % len(membri_ag))