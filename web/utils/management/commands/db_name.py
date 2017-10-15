# coding: utf-8
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("{}\n".format(settings.DATABASES['default']['NAME']))
