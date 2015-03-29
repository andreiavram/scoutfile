# coding: utf-8
'''
Created on Sep 8, 2013

@author: yeti
'''


from django.core.management.base import BaseCommand, CommandError
from album.models import SetPoze, Imagine
import traceback
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        imgs = Imagine.objects.all().order_by("-id")
        cnt = imgs.count()
        idx = 0
        for img in imgs:
            img.get_large_url()
            img.get_thumbnail_url()
            idx += 1
            if idx % 10 == 0:
                self.stdout.write("%d out of %d processed\n" % (idx, cnt))