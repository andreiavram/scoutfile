n# coding: utf-8
import datetime
from django.core.management.base import BaseCommand
from album.models import SetPoze
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        i = 0
        for set_poze in SetPoze.objects.filter(offset_changed = True):
            set_poze.offset_changed = False
            set_poze.save()

            for imagine in set_poze.imagine_set.all():
                imagine.data = datetime.datetime.strptime(imagine.exifdata_set.get(key = "DateTimeOriginal").value, "%Y:%m:%d %H:%M:%S") + datetime.timedelta(seconds = set_poze.offset_secunde)
                imagine.save()
                i += 1
                if i % 100 == 0:
                    self.stdout.write("Currently processing %dth photo\n" % i)
