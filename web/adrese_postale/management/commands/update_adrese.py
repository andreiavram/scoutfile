# coding: utf8
from django.core.management.base import BaseCommand

from adrese_postale.adrese import AdresaPostala
from structuri.models import InformatieContact


class Command(BaseCommand):

    help = (
        "For each membru with an address, check it's postal "
        "code and if it doesn't have one create and save it."
    )

    def handle(self, *args, **kwargs):
        contact_data = InformatieContact.objects.filter(
            tip_informatie__nume__iexact=u'Adresa corespondență')

        self.stdout.write(
            'Found valid contact information '
            'from %d users.\n' % contact_data.count()
        )

        new_codes = 0

        for info in contact_data:
            try:
                adresa = AdresaPostala.parse_address(
                    info.valoare, fail_silently=False)
            except Exception, e:
                self.stdout.write(
                    u'%s\n' % unicode(e))
                continue

            if not adresa.are_cod():
                try:
                    adresa.determine_cod()
                except ValueError, e:
                    self.stdout.write(u'%s\n' % unicode(e))
                    continue

                if not adresa.are_cod():
                    self.stdout.write('Could not determine code\n')
                    continue

                new_codes += 1

            if adresa.__unicode__() != info.valoare:
                info.valoare = adresa.__unicode__()
                info.save()

        self.stdout.write('%d new codes generated\n' % new_codes)
