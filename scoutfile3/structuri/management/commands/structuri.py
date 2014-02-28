#coding: utf-8
from django.contrib.contenttypes.models import ContentType

from scoutfile3.structuri.models import Membru, InformatieContact, TipInformatieContact

import logging
import datetime
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)




class Command(BaseCommand):
    available_commands = ["update_adrese"]

    def handle(self, *args, **options):
        if args[0] not in self.available_commands:
            self.stderr.write(u"Command must be one of %s" % ",".join(self.available_commands))

        getattr(self, args[0])(*args[1:], **options)

    def update_adrese(self, *args, **options):
        total = 0
        for membru in Membru.objects.all():
            adrese = InformatieContact.objects.filter(content_type=ContentType.objects.get(membru), object_id=membru.id,
                                                 tip_informatie__nume__iexact=u"adresă corespondență")
            if adrese.count():
                continue

            ic = InformatieContact(content_type=ContentType.objects.get(membru), object_id=membru.id,
                                   tip_infomatie=TipInformatieContact.objects.get(nume__iexact=u"adresă coresponență"),
                                   valoare=membru.adresa, data_start=datetime.datetime.now())
            ic.save()
            total += 1

        self.stdout.write("total updates %d" % total)