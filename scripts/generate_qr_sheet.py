import base64
from io import StringIO, BytesIO
from tkinter import Image
from typing import Union

import requests
from svgwrite import mm
import svgwrite
from svgwrite.image import Image

base_url = "http://127.0.0.1:8004/api/v1"
api_url = "/redirects/physicaltag/"
login_url = "/auth/login/"

def configure_fonts(dwg):
    dwg.embed_google_web_font(
        name="Roboto",
        uri='https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap'
    )

    dwg.embed_stylesheet("""
    .roboto {
        font-family: "Roboto";
        font-size: 4mm;
    }
    """)


login_response = requests.post(f"{base_url}{login_url}", json={"username": username, "password": password})
token = login_response.json().get("key")

created_ids = []

for i in range(1, 50):
    create_qr = requests.post(
      f"{base_url}{api_url}",
      json={
        "active": True,
        "ref": "?",
        "to_url": "",
        "tag_type": 1
      },
      headers={
        "Authorization": f"Token {token}"
      }
    )

    created_ids.append(create_qr.json().get("id"))


qr_data = requests.get(
f"{base_url}{api_url}?id__in={','.join([f'{i}' for i in created_ids])}",
    headers={
      "Authorization": f"Token {token}"
    }
)
data = qr_data.json()

svg_urls = [d['svg_qr_image_url'] for d in data]


def mm_dim(dim: int | float):
    return dim * mm

svg_width = 500
svg_height = 980
qr_size = 40
qrcode_size = 30

margin = 20

ncols = int((svg_width - 2 * margin) / qr_size)
nrows = int((svg_height - 2 * margin) / qr_size)

x_offset = int((qr_size - qrcode_size) / 2)
y_offset = int((qr_size - qrcode_size) / 2)

dwg = svgwrite.Drawing('qr.svg', size=(f"{svg_width}mm", f"{svg_height}mm"), fill=svgwrite.rgb(255, 255, 255), debug=True)
configure_fonts(dwg)

paragraph = dwg.add(dwg.g(class_="roboto"))

qr_index = 0
for item in data:
    qr_url = item['svg_qr_image_url']
    qr_data = requests.get(qr_url)
    if qr_data.status_code != 200:
        continue

    encoded = base64.b64encode(qr_data.text.encode("utf-8")).decode()
    svg_data = 'data:image/svg+xml;base64,{}'.format(encoded)

    dwg.add(
        Image(
            href=f'{svg_data}',
            insert=(mm_dim((qr_index % ncols) * qr_size + x_offset + margin), mm_dim((int(qr_index / ncols)) * qr_size + y_offset + margin)),
            size=(mm_dim(qrcode_size), mm_dim(qrcode_size)),
        )
    )
    print(item['token'])

    paragraph.add(
        dwg.text(
            item['token'],
            (
                mm_dim((qr_index % ncols) * qr_size + x_offset + qrcode_size * 0.08 + margin),
                mm_dim((int(qr_index / ncols)) * qr_size + y_offset + margin)
            ),
            fill=svgwrite.rgb(0, 0, 0),
            text_anchor="start",
        )
    )

    qr_index += 1
dwg.save()



