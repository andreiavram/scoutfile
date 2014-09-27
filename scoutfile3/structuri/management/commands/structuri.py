#coding: utf-8
from django.contrib.contenttypes.models import ContentType

from scoutfile3.structuri.models import Membru, InformatieContact, TipInformatieContact

import logging
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)




class Command(BaseCommand):
    available_commands = ["update_adrese", "oncr_sync"]

    def handle(self, *args, **options):
        if args[0] not in self.available_commands:
            self.stderr.write(u"Command must be one of %s" % ",".join(self.available_commands))

        getattr(self, args[0])(*args[1:], **options)

    def update_adrese(self, *args, **options):
        total = 0
        for membru in Membru.objects.all():
            adrese = InformatieContact.objects.filter(content_type=ContentType.objects.get_for_model(membru), object_id=membru.id,
                                                 tip_informatie__nume__iexact=u"Adresă corespondență", tip_informatie__relevanta="Membru")
            if adrese.count():
                continue

            ic = InformatieContact(content_type=ContentType.objects.get_for_model(membru), object_id=membru.id,
                                   tip_informatie=TipInformatieContact.objects.get(nume__iexact=u"Adresă corespondență", relevanta="Membru"),
                                   valoare=membru.adresa, data_start=datetime.datetime.now())
            ic.save()
            total += 1

        self.stdout.write("total updates %d" % total)

    def oncr_sync(self, *args, **options):
        membri_oncr = Membru.objects.filter(scout_id__isnull=False)

        import requests
        import re

        s = requests.session()
        r1 = s.get("https://www.oncr.ro/login")
        login_data = {"_username": settings.ONCR_USER, "_password": settings.ONCR_PASSWORD}
        regex = 'name="_csrf_token" value="([a-f0-9]*)"'
        csrf = re.findall(regex, r1.text)

        if len(csrf) == 0:
            self.stdout.write("ERROR connecting to ONCR.ro")

        login_data['_csrf_token'] = csrf[0]

        r2 = s.post("https://www.oncr.ro/login_check", login_data)
        # r3 = s.get("https://www.oncr.ro/%s.json", scout_id)

        for membru in membri_oncr:
            r3 = s.get("https://www.oncr.ro/%s.json", membru.scout_id)
            if r3.status_code != 200:
                return

            jdict = r3.json()
            membru.save("oncr_feegood", jdict["feeGood"], 24 * 60 * 60)
            membru.save("oncr_lastpaidquarter", jdict["lastPaidQuarter"], 24 * 60 * 60)