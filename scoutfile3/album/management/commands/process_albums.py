# coding: utf-8
'''
Created on Sep 8, 2013

@author: yeti
'''


from django.core.management.base import BaseCommand, CommandError
from album.models import SetPoze
import traceback
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        seturi = SetPoze.objects.filter(status=1)
        for set_poze in seturi:
            logger.info("Processing set %d" % set_poze.id)
            try:
                set_poze.process_zip_file()
            except Exception, e:
                logger.error("Management command process_albums crashed: %s %s" % (e, traceback.format_exc()))
                logger.error("Set %d (%s) crashed" % (set_poze.id, set_poze.autor_user))