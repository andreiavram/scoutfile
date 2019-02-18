from collections import defaultdict
from unidecode import unidecode

__author__ = 'yeti'

import requests

from django.conf import settings
from bs4 import BeautifulSoup


class ONCRClient(object):
    URLS = {
        "login_form": "https://www.oncr.ro/login",
        "login_check": "https://www.oncr.ro/login_check",
        "add_activitate": "https://www.oncr.ro/local_center/activitati/new",
        "membru_info": "https://www.oncr.ro/%s.json",
        "list_activitati": "https://www.oncr.ro/local_center/activitati/datatable/%s",
    }

    def __init__(self, user=None, password=None, **kwargs):
        self.user = user if user else settings.ONCR_USER
        self.password = password if password else settings.ONCR_PASSWORD
        self.session = requests.Session()
        self.logged_in = False

    def do_login(self):
        r_auth = self.session.get(self.URLS.get("login_form"))

        soup = BeautifulSoup(r_auth.text, "html.parser")
        csrf_value = soup.find("input", {"name": "_csrf_token"}).attrs.get("value")
        login_data = {"_username": self.user,
                      "_password": self.password,
                      "_csrf_token": csrf_value}

        r_login = self.session.post(self.URLS.get("login_check"), login_data)
        if "Datele introduse sunt incorecte!" in r_login.text:
            self.logged_in = False
        elif r_login.history:
            for resp in r_login.history:
                if resp.status_code == 302 and resp.headers['location'] == "https://www.oncr.ro/":
                    self.logged_in = True

        return self.logged_in

    def python_date_to_mysql(self, date):
        return date.strftime("%Y-%m-%d")

    def add_activitate(self, **kwargs):
        r_activitate = self.session.get(self.URLS.get("add_activitate"))
        soup = BeautifulSoup(r_activitate.text, "html.parser")
        token = soup.find("input", {"name": "activity[_token]"}).attrs.get("value")

        raport_anual_oncr = kwargs.get("raport_anual_oncr", False)
        raport_centru_local = kwargs.get("raport_anual_cl", True)
        published_in = []
        if raport_anual_oncr:
            published_in.append("1")
        if raport_centru_local:
            published_in.append("2")

        activity_type_args = ["aventura", "social", "cultural", "ecologie", "spiritual", "fundraising", "altele"]
        activity_type = [str(2**activity_type_args.index(category_field)) for category_field in activity_type_args if kwargs.get(category_field)]

        data = {
            "activity[published_in][]": published_in,
            "activity[name]": kwargs.get("nume"),
            "activity[category_id]": str(kwargs.get("categorie")),
            "activity[location]": kwargs.get("locatie"),
            "activity[from_date]": self.python_date_to_mysql(kwargs.get("data_inceput")),
            "activity[to_date]": self.python_date_to_mysql(kwargs.get("data_sfarsit")),
            "activity[type][]": activity_type,
            "activity[_token]": token,
            "activity[activityParticipantsNumber][memberYoungGirls]": kwargs.get("numar_participanti", {}).get("fete"),
            "activity[activityParticipantsNumber][memberYoungBoys]": kwargs.get("numar_participanti", {}).get("baieti"),
            "activity[activityParticipantsNumber][memberElderGirls]": kwargs.get("numar_participanti", {}).get("lideri_femei"),
            "activity[activityParticipantsNumber][memberElderBoys]": kwargs.get("numar_participanti", {}).get("lideri_barbati"),

            "activity[activityParticipantsNumber][externYoungGirls]": 0,
            "activity[activityParticipantsNumber][externYoungBoys]": 0,
            "activity[activityParticipantsNumber][externElderGirls]": 0,
            "activity[activityParticipantsNumber][externElderBoys]": 0,

            "activity[short_description]": kwargs.get("descriere"),
            "activity[objectives]": kwargs.get("obiective"),
            "activity[target]": kwargs.get("grup_tinta"),
            "activity[activities]": kwargs.get("activitati"),
            "activity[promotion]": kwargs.get("promovare"),
            "activity[partners]": kwargs.get("parteneri"),
            "activity[budget]": "{}".format(kwargs.get("buget")),
            "activity[beneficiaries]": kwargs.get("beneficiari"),
        }

        photo = kwargs.get("photo", None)
        photo_upload_data = ("", "", "application/octet-stream")
        if photo:
            photo_tmp_path = "/tmp/%s" % unidecode(kwargs.get("nume").replace(" ", ""))
            r = requests.get(photo, stream=True)
            if r.status_code == 200:
                with open(photo_tmp_path, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)

            photo_data = open(photo_tmp_path, "rb")
            photo_upload_data = ("cover.png", photo_data, "application/octet-stream")

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 "
                          "Safari/537.36",
            "Referer": self.URLS.get("add_activitate"),
            "Host": "www.oncr.ro",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

        r_activitate = self.session.post(
            self.URLS.get("add_activitate"),
            data=data,
            files=[("photos[]", photo_upload_data)],
            headers=headers)

        return r_activitate.status_code == 200

    def get_membru_json(self, oncr_id):
        r_data = self.session.get(self.URLS.get("membru_info") % oncr_id)
        if r_data.status_code != 200:
            raise Exception("wrong response for RPC")

        return r_data.json()

    def get_activitati_list(self):
        command_dict = {
            "sEcho": "1", "iColumns": "5", "sColumns": None, "iDisplayStart": "0", "iDisplayLength": "20",
            "mDataProp_0": "0", "mDataProp_1": "1", "mDataProp_2": "2", "mDataProp_3": "3",
            "mDataProp_4": "4", "sSearch": None, "bRegex": "false", "sSearch_0": None, "bRegex_0": "false",
            "bSearchable_0": "true", "sSearch_1": None, "bRegex_1": "false", "bSearchable_1": "true",
            "sSearch_2": None, "bRegex_2": "false", "bSearchable_2": "true", "sSearch_3": None,
            "bRegex_3": "false", "bSearchable_3": "true", "sSearch_4": None, "bRegex_4": "false",
            "bSearchable_4": "true", "iSortCol_0": "0", "sSortDir_0": "desc", "iSortingCols": "1",
            "bSortable_0": "false", "bSortable_1": "true", "bSortable_2": "true", "bSortable_3": "true",
            "bSortable_4": "true",
        }

        r_events = self.session.post(self.URLS.get("list_activitati") % "2", command_dict)

        if r_events.status_code == 200:
            return r_events.json()["aaData"]

        return {}


if __name__ == "__main__":
    client = ONCRClient(user="andrei.avram@albascout.ro", password="")
    client.do_login()
    data = client.get_membru_json("AA147")
    print data