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
        self.user = user # if user else settings.ONCR_USER
        self.password = password # if password else settings.ONCR_PASSWORD
        self.session = requests.session()
        self.logged_in = False

    def do_login(self):
        r_auth = self.session.get(self.URLS.get("login_form"))

        soup = BeautifulSoup(r_auth.text)
        csrf_value = soup.find("input", {"name": "_csrf_token"}).attrs.get("value")
        login_data = {"_username": self.user,
                      "_password": self.password,
                      "_csrf_token": csrf_value}

        r_login = self.session.post(self.URLS.get("login_check"), login_data)

        if r_login.status_code == 302 and r_login.headers['location'] == "https://www.oncr.ro/":
            self.logged_in = True

        return self.logged_in

    def add_activitate(self, **kwargs):
        r_activitate = self.session.get(self.URLS.get("add_activitate"))
        soup = BeautifulSoup(r_activitate.text)
        token = soup.find("input", {"name": "activity[_token]"}).attrs.get("value")

        data = {"activity[published_in][]": ['1', '2'],
                "activity[name]": "test1",
                "activity[category_id]": "2",
                "activity[location]": "test_locatie",
                "activity[from_date]": "2014-03-01",
                "activity[to_date]": "2014-03-03",
                "activity[type][]": ["2", "4"],
                "activity[participants_number]": "23",
                "activity[_token]": token,
                "activity[short_description]": "testdescription",
                "activity[objectives]": "testobjectives",
                "activity[target]": "testtargetgroup",
                "activity[activities]": "testactivites",
                "activity[promotion]": "testpromotion",
                "activity[partners]": "tespartnerst",
                "activity[budget]": "7000",
                "activity[beneficiaries]": "testbeneficiaries",
                }

        r_activitate = self.session.post(self.URLS.get("add_activitate"),
                    data=data,
                    files=[("photos[]", ("", "", "application/octet-stream"))],
                    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",
                             "Referer": self.URLS.get("add_activitate"),
                             "Host": "www.oncr.ro",
                             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})

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
            return r_events.json()

        return {}


if __name__ == "__main__":
    client = ONCRClient()
    client.do_login()
    events = client.get_activitati_list()
    print events