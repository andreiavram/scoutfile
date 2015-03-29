#coding: utf-8
from django.contrib.contenttypes.models import ContentType

from structuri.models import Membru, InformatieContact, TipInformatieContact

import logging
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.oncr_client import ONCRClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    available_commands = ["update_adrese", "oncr_sync", "oncr_sync_ids"]

    def handle(self, *args, **options):
        if args[0] not in self.available_commands:
            self.stderr.write(u"Command must be one of %s" % ",".join(self.available_commands))
            return

        getattr(self, args[0])(*args[1:], **options)

    def update_adrese(self, *args, **options):
        total = 0
        for membru in Membru.objects.all():
            adrese = InformatieContact.objects.filter(content_type=ContentType.objects.get_for_model(membru),
                                                      object_id=membru.id,
                                                      tip_informatie__nume__iexact=u"Adresă corespondență",
                                                      tip_informatie__relevanta="Membru")
            if adrese.count():
                continue

            tip_informatie = TipInformatieContact.objects.get(nume__iexact=u"Adresă corespondență", relevanta="Membru")
            ic = InformatieContact(content_type=ContentType.objects.get_for_model(membru), object_id=membru.id,
                                   tip_informatie=tip_informatie,
                                   valoare=membru.adresa, data_start=datetime.datetime.now())
            ic.save()
            total += 1

        self.stdout.write("total updates %d" % total)

    def oncr_sync_ids(self, *args, **options):
        import os
        file_name = os.path.join(settings.BASE_DIR, "importdata", "oncr_ids.csv")
        with open(file_name) as f:
            lines = f.readlines()

        nf = 0
        for line in lines:
            line = line.split(",")

            nume = line[1].split()[0]
            prenume = " ".join(line[1].split()[1:])

            membru = Membru.objects.filter(nume__iexact=nume, prenume__icontains=prenume)
            if membru.count():
                membru = membru[0]
                membru.scout_id = line[0]
                self.stdout.write("SCOUTID: %s\n" % membru.scout_id)
                membru.save()
            else:
                self.stdout.write("NOT FOUND: nume %s, prenume %s\n" % (nume, prenume))
                nf += 1

        self.stdout.write("%d not found\n" % nf)
        return

    def oncr_sync(self, *args, **options):
        membri_oncr = Membru.objects.filter(scout_id__isnull=False).exclude(scout_id="")

        oncr_client = ONCRClient()

        for membru in membri_oncr:
            try:
                jdict = oncr_client.get_membru_json(membru.scout_id)
                membru.save_to_cache("oncr_feegood", jdict["feeGood"], 24 * 60 * 60)
                membru.save_to_cache("oncr_lastpaidquarter", jdict["lastPaidQuarter"], 24 * 60 * 60)
            except Exception, e:
                self.stdout.write("Error getting %s: %s\n" % (membru.scout_id, e))