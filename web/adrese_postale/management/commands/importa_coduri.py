# coding: utf8
import os
import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.six.moves import input

from adrese_postale.models import CodPostal


class Command(BaseCommand):
    """Management command to delete existing postal codes and load
    new ones from file.

    WARNING: This management command deletes all existing postal codes!
    Postal codes should be located in a file whose name is specified in
    settings POSTAL_CODES_FILENAME and should be located at the root
    directory.
    """

    help = (
        'Delete existing postal codes and load new ones from csv file.')

    def handle(self, *args, **kwargs):
        user_response = input(
            'Running this command will delete all '
            'postal codes! Are you sure? y/n'
        )
        if user_response.lower() != 'y':
            return

        CodPostal.objects.all().delete()

        postal_codes_file = os.path.join(
            settings.BASE_DIR, settings.POSTAL_CODES_FILENAME)
        with open(postal_codes_file, 'rb') as f:
            csv_reader = csv.reader(f, delimiter='|')
            lines = []
            for row in csv_reader:
                lines.append([x.strip() for x in row])

        for line in lines:
            cod_postal_dict = {
                'judet': line[0],
                'localitate': line[1],
                'tip_strada': line[2],
                'strada': line[3],
                'descriptor': line[4],
                'cod_postal': line[5],
                'sector': line[6],
            }
            CodPostal.objects.create(**cod_postal_dict)
