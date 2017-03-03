# coding: utf-8
import re
from django.db import models

from adrese_postale.adrese import AdresaPostala, AdresaPostalaException


class CodPostal(models.Model):
    cod_postal = models.CharField(max_length=6)
    judet = models.CharField(max_length=255)
    localitate = models.CharField(max_length=255)
    tip_strada = models.CharField(max_length=255, null=True, blank=True)
    strada = models.CharField(max_length=255, null=True, blank=True)
    sector = models.IntegerField(null=True, blank=True)
    descriptor = models.CharField(max_length=255, null=True, blank=True)

    SEQUENCE_REGEXS = {
        r"^(\d+)$": 1,
        r"^([a-zA-Z]+)(\d+)$": 2,
        r"^(\d+)([a-zA-Z]*)([a-zA-Z])$": 3,
        r"^([a-zA-Z])*([a-zA-Z])$": 4
    }

    @staticmethod
    def cuvinte_nume_strada(nume_strada):
        return [i for i in nume_strada.strip().split(" ") if i.title() == i]

    @classmethod
    def get_cod_pentru_adresa(cls, adresa):
        """
        Obține cod poștal pentru o adresă
        :param adresa: un obiect de tip adresa postala sau string, care poate fi parsat
        :return: codul postal
        """

        if isinstance(adresa, basestring):
            try:
                a = AdresaPostala.parse_address(adresa, fail_silently=False)
            except AdresaPostalaException, e:
                a = None

        elif isinstance(adresa, AdresaPostala):
            a = adresa
        else:
            raise ValueError(u"Input should either be a string or AdresaPostala")

        if a is None:
            raise AdresaPostalaException("Adresa proasta %s" % adresa)

        #   first look for smaller towns
        codes = CodPostal.objects.filter(judet=a.judet, localitate=a.localitate if not a.is_adresa_sat() else a.comuna)
        if codes.count() == 0:
            raise ValueError(u"Place not found: (%s), (%s). 0 codes returned" % (a.localitate, a.judet))

        if codes.count() == 1:
            #   this is a town with <= 10K inhabitants, only has one code
            return codes[0]

        #   there is more than one code
        # codes = codes.filter(tip_strada=a.tip_strada_title)
        words = cls.cuvinte_nume_strada(a.nume_strada)

        for s in words:
            codes = codes.filter(strada__icontains=s)

        #   cazul in care ai strada Traian, si strada Traian Vuia

        if codes.count() == 0:
            raise ValueError(u"Could not identify any codes matching %s" % words)

        id_exclude = []
        for code in codes:
            nwords = len(cls.cuvinte_nume_strada(code.strada))
            if nwords > len(words):
                id_exclude.append(code.id)

        codes = codes.exclude(id__in=id_exclude)

        if codes.count() == 1:
            return codes[0]

        if codes.filter(descriptor__isnull=False).count() == 0:
            raise ValueError(u"More than one code returned, no descriptors on codes, unclear address")

        for code in codes:
            if code.descriptor is None:
                continue

            data = code.descriptor[3:]
            elms = [elm.strip() for elm in re.split(";|,", data.strip())]

            for e in elms:
                parts = [elm.strip() for elm in e.split("-")]

                if code.descriptor.lower().startswith("nr.") and a.nr_numeric:
                    # variante: 1-T; 2-T; 25-33
                    parts = [re.findall("\d+", p)[0] if p != "T" else "T" for p in parts]
                    if len(parts) == 2:
                        #   two cases: two numbers or one number and T
                        if int(parts[0]) % 2 == a.nr_numeric % 2:
                            #   if the parity is right
                            if parts[1] == "T":
                                if a.nr_numeric >= int(parts[0]):
                                    return code
                            else:
                                if int(parts[0]) <= int(a.nr_numeric) <= int(parts[1]):
                                    return code
                    elif len(parts) == 1 and a.nr_numeric == int(parts[0]):
                        return code
                elif code.descriptor.lower().startswith("bl.") and a.bl:
                    # toate variantele aici sunt cu nume individuale de blocuri
                    # D8B, D7A
                    # sau de secvente de blocuri
                    # 40-42 sau
                    # 32B - 32D (serie litere) sau
                     # A1 - A7 (serie numerica)
                    if len(parts) == 2:
                        try:
                            sequence = cls.determine_sequence_type(parts)
                            if cls.value_in_sequence(sequence, a.bl):
                                return code
                        except ValueError, e:
                            pass
                    elif len(parts) == 1 and a.bl.lower() == parts[0].lower():
                        return code

        # code = codes[0] if codes.count() else None
        return None

    @classmethod
    def determine_sequence_type(cls, sequence):
        if len(sequence) != 2:
            raise ValueError(u"Need a two element list / tuple")

        matches = {0: (), 1: ()}
        for r in cls.SEQUENCE_REGEXS.keys():
            for i in range(2):
                if len(matches[i]):
                    continue

                m = re.findall(r, sequence[i])
                if len(m):
                    matches[i] = (cls.SEQUENCE_REGEXS[r], m[0])

        for i in range(2):
            if len(matches[i]) == 0:
                raise ValueError(u"Could not match address sequence element to any known sequence type (A, 1, A1, 1A)")

        #   ranges like 3 - 3F
        if matches[0][0] != matches[1][0]:
            raise ValueError(u"Sequence types mismatch: %d, %d" % (matches[0][0], matches[1][0]))

        #   ranges like DA - FE or 3DA - 3FE
        if matches[0][0] in (3, 4) and matches[0][1][0] != matches[1][1][0]:
            raise ValueError(u"Sequence range cannot be determined %s, %s" % (matches[0][1], matches[1][1]))

        #   ranges like ACD - AAE
        if matches[0][0] == 3 and matches[0][1][1] != matches[1][1][1]:
            raise ValueError(u"Sequence range cannot be determined %s, %s" % (matches[0][1], matches[1][1]))

        return matches

    @classmethod
    def value_in_sequence(cls, sequence, value):
        if sequence[0][0] == 1:
            return int(sequence[0][1]) <= int(value) <= int(sequence[1][1])
        if sequence[0][0] == 2:
            return value.upper() in [(sequence[0][1][0] + str(v)).upper() for v in range(int(sequence[0][1][1]), int(sequence[1][1][1]) + 1)]
        if sequence[0][0] == 3:
            prefix = sequence[0][1][0] + sequence[0][1][1]
            return value.upper() in cls.char_range(sequence[0][1][2], sequence[1][1][2], prefix=prefix)
        if sequence[0][0] == 4:
            return value.upper() in cls.char_range(sequence[0][1][1], sequence[1][1][1], prefix=sequence[0][1][0])
        return False

    @staticmethod
    def char_range(cls, c1, c2, prefix=""):
        for c in xrange(ord(c1), ord(c2) + 1):
            str = "%s%s" % (prefix, chr(c))
            yield str.upper()

    def __unicode__(self):
        return u"%s" % self.cod_postal