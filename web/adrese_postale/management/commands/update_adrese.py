#   coding: utf8
from django.core.management.base import BaseCommand

from adrese_postale.adrese import AdresaPostala
from structuri import InformatieContact

__author__ = 'andrei'

import codecs, locale


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout = codecs.getwriter(locale.getpreferredencoding())(self.stdout)
        #   pentru fiecare membru care are adresa
        #   prelucreaza adresa, vezi daca-i ok
        #   daca nu are cod, cauta-i codul, adauga si salveaza (?)
        infos = InformatieContact.objects.filter(tip_informatie__nume__iexact=u"Adresa corespondență")
        self.stdout.write("%d infos\n" % infos.count())

        new_codes = 0

        for info in infos:
            try:
                adresa = AdresaPostala.parse_address(info.valoare, fail_silently=False)
            except Exception, e:
                # self.stdout.write(u"%s" % unicode(e).encode('utf-8', 'ignore') + u"\n")
                continue

            if not adresa.are_cod():
                try:
                    adresa.determine_cod()
                except ValueError, e:
                    self.stdout.write(unicode(e) + u"\n")
                    continue

                if adresa.are_cod():
                    info.valoare = adresa.__unicode__()
                    info.save()
                    # self.stdout.write(u"info to save: %s\n" % unicode(info.valoare).encode("utf-8"))
                    new_codes += 1
                else:
                    self.stdout.write("could not determine code\n")
            else:
                if adresa.__unicode__() != info.valoare:
                    info.valoare = adresa.__unicode__()
                    info.save()


        self.stdout.write("%d new codes\n" % new_codes)

