__author__ = 'yeti'

import requests
import re

import httplib as http_client
import logging

from requests_toolbelt import MultipartEncoder

http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class settings:
    ONCR_USER = "andrei.avram@albascout.ro"
    ONCR_PASSWORD = "yetiRulz1_"


s = requests.session()
r1 = s.get("https://www.oncr.ro/login")
login_data = {"_username": settings.ONCR_USER, "_password": settings.ONCR_PASSWORD}
regex = r'name="_csrf_token" value="([A-Za-z0-9\-_]*)"'
csrf = re.findall(regex, r1.text)

if len(csrf) == 0:
    print "ERROR connecting to ONCR.ro"

login_data['_csrf_token'] = csrf[0]

r2 = s.post("https://www.oncr.ro/login_check", login_data)

r3 = s.get("https://www.oncr.ro/local_center/activitati/new")

from bs4 import BeautifulSoup
soup = BeautifulSoup(r3.text)

data = {"activity[published_in][]": ['1', '2'],
        "activity[name]": "test1",
        "activity[category_id]": "2",
        "activity[location]": "test_locatie",
        "activity[from_date]": "2014-03-01",
        "activity[to_date]": "2014-03-03",
        "activity[type][]": ["2", "4"],
        "activity[participants_number]": "23",
        "activity[_token]": soup.find("input", {"name": "activity[_token]"}).attrs.get("value"),
        "activity[short_description]": "testdescription",
        "activity[objectives]": "testobjectives",
        "activity[target]": "testtargetgroup",
        "activity[activities]": "testactivites",
        "activity[promotion]": "testpromotion",
        "activity[partners]": "tespartnerst",
        "activity[budget]": "7000",
        "activity[beneficiaries]": "testbeneficiaries",
        # "_csrf_token": soup.find("input", {"name": "_csrf_token"}).attrs.get("value"),
        }


# m = MultipartEncoder(fields=data)
# print m.to_string()

r4 = s.post("https://www.oncr.ro/local_center/activitati/new",
            data=data,
            files=[("photos[]", ("", "", "application/octet-stream"))],
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",
                     "Referer": "https://www.oncr.ro/local_center/activitati/new",
                     "Host": "www.oncr.ro",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
print r4.status_code
print r4.text
# activity[published_in][]
# activity[published_in][]
# activity[name]
# activity[location]
# activity[from_date]
# activity[to_date]
# activity[type][]
# activity[type][]
# activity[type][]
# activity[type][]
# activity[type][]
# activity[type][]
# activity[type][]
# activity[participants_number]
# photos[]
# None
# activity[_token]
# activity[short_description]
# activity[objectives]
# activity[target]
# activity[activities]
# activity[promotion]
# activity[budget]
# activity[partners]
# activity[beneficiaries]

