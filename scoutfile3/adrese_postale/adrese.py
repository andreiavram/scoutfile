# coding: utf-8
__author__ = 'yeti'


import re


class AdresaPostalaException(Exception):
    pass


class AdresaPostala(object):
    REGEX = r"(B-dul\.|Str\.|P-ța\.|Piața|Calea|Intr.|Comuna|Sat) ([\w \.]+?), (((?:Nr|Bl|Sc|Ap|Et)\.? ?[\w\d]+, )+) ?(?:(\d{6}), +)?([\w ]+)(:?, (:?Comuna|Com\.) ([\w ]+))?(:?, (Jud\.?[\w ]+))?"
    DATA_HEADINGS = {
        "tip_strada": u"Tip stradă",
        "nume_strada": u"Nume stradă",
        "cod": u"Cod postal",
        "localitate": u"Localitate",
        "judet": u"Judet",
        "comuna": u"Comuna",
        "Nr": u"Numar",
        "Bl": u"Bloc",
        "Et": u"Etaj",
        "Sc": u"Scara",
        "Ap": u"Apartament"
    }

    STRADA_HEADINGS = {
        "Str": "Strada",
        "Bd": "Bulevardul",
        "B-dul": "Bulevardul",
        "Al": "Aleea",
        "Intr": "Intrarea",
        "Calea": u"Calea",
        "Sat": u"Sat",
        u"P-ța": u"Piața",
        u"Piața": u"Piața"
    }

    DEFAULT_DATA_ORDER = ["Nr", "Bl", "Sc", "Et", "Ap"]

    DATA_DEPENDENCY = {
        "Nr" : [],
        "Bl": ["Ap"],
        "Sc": ["Nr|Bl", "Ap"],
        "Et": ["Nr|Bl", "Ap"],
        "Ap": [],
    }

    def __init__(self, *args, **kwargs):
        if kwargs.get("tip_strada", "").lower() in ["sat", "comuna"]:
            if kwargs.get("tip_strada").lower() == "comuna":
                kwargs['comuna'] = kwargs['nume_strada']
            else:
                kwargs['comuna'] = kwargs['localitate'].strip("Comuna").strip("Com.").strip("comuna").strip("com.")
            kwargs['localitate'] = kwargs['nume_strada']
        if kwargs.get("judet", "") != "":
            kwargs['judet'] = kwargs.get("judet").strip("Jud.").strip("jud.").strip("Jud").strip("jud")

        self.available_data  = []
        for k, v in kwargs.items():
            if len(v.strip()) == 0:
                continue
            setattr(self, k.lower(), v.strip())
            self.available_data.append(k)

    @classmethod
    def parse_address(cls, str_address, fail_silently=True):
        if isinstance(str_address, str):
            ustr = unicode(str_address, "utf-8")
        elif isinstance(str_address, unicode):
            ustr = str_address
        else:
            raise ValueError("Address needs to be string")

        matches = re.findall(cls.REGEX, ustr, re.IGNORECASE | re.UNICODE)
        if len(matches) == 0:
            if not fail_silently:
                raise AdresaPostalaException(u"REGEX mismatch %s" % ustr)
            return None

        m = matches[0]
        bloc_detaliu = m[2]
        kwargs_detaliu = {}
        elem = bloc_detaliu.split(", ")
        for e in elem:
            if len(e.strip()) <= 0:
                continue
            separators = [". ", ".", " "]
            parts = []
            for sep in separators:
                parts = e.split(sep)
                if len(parts) == 2:
                    break
            if len(parts) < 2:
                if not fail_silently:
                    raise AdresaPostalaException(u"Element invalid, nu e de forma nume. valoare sau nume valoare")
                continue
            kwargs_detaliu[parts[0]] = parts[1]

        judet = m[10] if len(m[10].strip()) != 0 else "Alba"
        adresa_obj = cls(tip_strada=m[0], nume_strada=m[1], cod=m[4], localitate=m[5], comuna=m[8], judet=judet, **kwargs_detaliu)

        try:
            adresa_obj.validate_address()
        except AdresaPostalaException, e:
            if not fail_silently:
                raise e
            return None

        return adresa_obj

    def is_adresa_sat(self):
        return "comuna" in self.available_data

    def are_cod(self):
        return "cod" in self.available_data

    def set_cod(self, cod):
        self.cod = cod
        if not "cod" in self.available_data:
            self.available_data.append("cod")

    def determine_cod(self):
        from adrese_postale.models import CodPostal
        cod = CodPostal.get_cod_pentru_adresa(self)
        if cod:
            self.set_cod(cod.cod_postal)

    @property
    def nr_numeric(self):
        try:
            a_nr = re.findall(r"\d+", self.nr)[0]
            a_nr = int(a_nr)
        except Exception, e:
            a_nr = None
        return a_nr

    @property
    def tip_strada_title(self):
        return self.STRADA_HEADINGS.get(self.tip_strada, u"Strada")

    def validate_address(self):
        for data in [d for d in self.DATA_DEPENDENCY.keys() if d in self.available_data]:
            deps = self.DATA_DEPENDENCY.get(data)

            for item in deps:
                d = item.split("|")
                if len(d) > 1:
                    #	optional arg - one or another
                    valid_opt = False
                    for d_item in d:
                        if d_item in self.available_data:
                            valid_opt = True

                    if not valid_opt:
                        exception_msg = u"Lipseste unul din elementele din %s, cerut de %s" % (d, data)
                        raise AdresaPostalaException(exception_msg)
                elif item not in self.available_data:
                    exception_msg = u"Elementul %s nu este în adres, desi este cerut de %s" % (item, data)
                    raise AdresaPostalaException(exception_msg)

        #   daca e sat trebuie sa aiba strada, sat, comuna
        #   daca nu e sat trebuie sa aiba strada
        #   indiferent ce e trebuie sa aiba localitate si judet
        if "localitate" not in self.available_data:
            raise ValueError(u"Trebuie să existe localitatea")
        if "judet" not in self.available_data:
            raise ValueError(u"Trebuie să existe județul")

    def print_details(self):
        for k in self.available_data:
            print "%s: %s" % (self.DATA_HEADINGS.get(k, "ERROR"), getattr(self, k.lower()))
        print "Is sat: %s" % self.is_adresa_sat()
        print "\n\n"

    def __unicode__(self):
        if self.is_adresa_sat():
            pass
        adresa = ""
        elms = [self.tip_strada, self.nume_strada]

        adresa += self.tip_strada + " "
        adresa += self.nume_strada + ", "

        for e in [a for a in self.DEFAULT_DATA_ORDER if a.lower() in self.available_data]:
            adresa += e + ". " + getattr(self, e.lower()) + ", "

        if self.tip_strada.lower() != "comuna" and self.is_adresa_sat():
            adresa += u"%s" % self.localitate.title() + ", "
            if self.are_cod():
                adresa += self.cod + ", "
            adresa += u"Comuna %s" % self.comuna
        else:
            if self.are_cod():
                adresa += self.cod + ", "
            adresa += self.localitate

        adresa += ", jud. %s" % self.judet
        return adresa


if __name__ == "__main__":
    with open("adrese.txt") as f:
        adrese = f.readlines()

    cnt = 0
    for a in adrese:
        if len(a) < 15:
            continue
        try:
            adresa = AdresaPostala.parse_address(a)
        # if adresa is not None:
        # 	adresa.print_details()
        except AdresaPostalaException, e:
            print "Eroare validare la %s" % a
            cnt += 1
            adresa.print_details()
    print cnt