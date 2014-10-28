# coding: utf-8
__author__ = 'yeti'



import re

with open("adrese.txt") as f:
    adrese = f.readlines()


class AdresaPostalaException(Exception):
    pass


class AdresaPostala(object):
    REGEX = r"(B-dul\.|Str\.|P-ța\.|Piața|Calea|Comuna|Sat){1} ([\w \.]+?), (((?:Nr|Bl|Sc|Ap|Et)\.? ?[\w\d]+, )+) ?(?:(\d{6}), +)?([\w ]+)(:?, (:?Comuna|Com\.) ([\w ]+))?(:?, (Jud\.?[\w ]+))?"
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
        "Bl": ["Ap", ],
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
            setattr(self, k, v.strip())
            self.available_data.append(k)

    @classmethod
    def parse_address(cls, str):
        matches = re.findall(cls.REGEX, unicode(str, "utf-8"), re.IGNORECASE | re.UNICODE)
        if len(matches) == 0:
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
                print "ERROR"
                print e
                continue
            kwargs_detaliu[parts[0]] = parts[1]
        adresa = cls(tip_strada=m[0], nume_strada=m[1], cod=m[4], localitate=m[5], comuna=m[8], judet=m[10], **kwargs_detaliu)
        adresa.validate_address()
        return adresa

    def is_adresa_sat(self):
        return "comuna" in self.available_data

    def validate_address(self):
        for data in [d for d in self.DATA_DEPENDENCY.keys() if d in self.available_data]:
            deps = self.DATA_DEPENDENCY.get(data)

            for item in deps:
                d = item.split("|")
                if len(d) > 1:
                    #	optional arg - one or another
                    valid = False
                    for d_item in d:
                        if d_item in self.available_data:
                            valid = True

                elif item not in self.available_data:
                    exception_msg = u"Elementul %s nu este în adresă, deși este cerut de %s" % (item, data)
                    print exception_msg
                    raise AdresaPostalaException(exception_msg)

    def print_details(self):
        for k in self.available_data:
            print "%s: %s" % (self.DATA_HEADINGS.get(k, "ERROR"), getattr(self, k))
        print "Is sat: %s" % self.is_adresa_sat()
        print "\n\n"

if __name__ == "__main__":
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