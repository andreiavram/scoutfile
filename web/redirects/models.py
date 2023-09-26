import random
import string

from django.contrib.sites.models import Site
from django.db import models
from django.db.models import IntegerChoices
from django.urls import reverse
from qr_code.qrcode.maker import make_qr_code_url_with_args


def generate_token():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


class PhysicalTag(models.Model):
    class TagTypes(IntegerChoices):
        QRCODE = 1, "QR Code"
        RFID = 2, "RFID"

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    ref = models.CharField(max_length=255, null=True, default='', verbose_name="Reference")

    token = models.CharField(default=generate_token, max_length=30, unique=True, db_index=True)
    to_url = models.CharField(max_length=255)
    hit_count = models.PositiveIntegerField(default=0)

    tag_type = models.PositiveIntegerField(choices=TagTypes.choices, default=TagTypes.QRCODE)

    @property
    def url(self):
        return Site.objects.get_current().domain + reverse('redirects:tag-redirect', kwargs={'code': self.token})

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id}, token={self.token}, target={self.to_url})"

    def qr_image_url(self, **kwargs):
        defaults = {
            'size': 'H',
            'image_format': 'png',
            'error_correction': 'H',
            'boost_error': True,
        }

        for key in defaults:
            if key not in kwargs:
                kwargs[key] = defaults[key]

        return make_qr_code_url_with_args(data=self.url, qr_code_args=kwargs)

    def svg_qr_image_url(self):
        return self.qr_image_url(image_format="svg")

    def png_qr_image_url(self):
        return self.qr_image_url(image_format="png")


