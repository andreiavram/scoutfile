# coding: utf-8
from fabric.tasks import execute
from scoutfile3.fabfile import seed_db

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        execute(seed_db)
