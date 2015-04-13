# coding: utf-8
import logging
import tablib
from django.http import HttpResponse
logger = logging.getLogger(__name__)

__author__ = 'yeti'


class TabularExport(object):
    @classmethod
    def generate_xlsx(cls, qs):
        data = cls.get_tablib_data(qs)
        response = HttpResponse(content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename="export_participanti.xlsx"'
        response.write(data.xlsx)
        return response

    @classmethod
    def generate_json(cls, qs):
        data = cls.get_tablib_data(qs)
        response = HttpResponse(content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename="export_participanti.json"'
        response.write(data.json)
        return response

    @classmethod
    def get_tablib_data(cls, qs):
        headers = [u"Nume", u"Prenume", u"Telefon", u"Email", u"ScoutID", u"Unitate", u"RDV",
                  u"Status", u"Data sosire", u"Data plecare", u"Rol", u"Complet"]

        all_data = []
        for participare in qs:
            if participare.membru:
                nume = participare.membru.nume
                prenume = participare.membru.prenume
            else:
                nume = participare.nonmembru.nume
                prenume = participare.nonmembru.prenume

            data = [nume, prenume]
            for e in ["telefon", "email", "scoutid", "unitate", "ramura_de_varsta"]:
                data.append(u"%s" % participare.process_camp_aditional(e))

            data.append(participare.get_status_participare_display())
            data.append(participare.data_sosire.strftime("%d.%m.%Y - %H:%M"))
            data.append(participare.data_plecare.strftime("%d.%m.%Y - %H:%M"))
            data.append(participare.get_rol_display())
            data.append(u"Complet" if participare.is_partiala else u"Parțial")

            all_data.append(data)

        data = tablib.Dataset(*all_data, headers=headers)
        return data
