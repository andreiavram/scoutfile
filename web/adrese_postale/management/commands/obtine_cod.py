# coding: utf8
from adrese_postale.models import CodPostal
from django.core.management.base import BaseCommand

from adrese_postale.adrese import AdresaPostala


class Command(BaseCommand):

    help = (
        'Get postal code based on address.'
        'Usage ./manage.py obtine_code <address>'
    )

    def add_arguments(self, parser):
            parser.add_argument('address')

    def handle(self, *args, **kwargs):
        if not kwargs.get('address'):
            self.stdout.write(
                'Usage ./manage.py obtine_cod <address>\n')
            return

        cod = CodPostal.get_cod_pentru_adresa(kwargs.get('address'))
        self.stdout.write(str(cod))
