from django.shortcuts import render, get_object_or_404
from django.views.generic import RedirectView

from redirects.models import PhysicalTag

from logging import getLogger
log = getLogger()


class PhysicalTagRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        code = kwargs['code']
        qr_code = get_object_or_404(PhysicalTag, token=code, active=True)
        qr_code.hit_count += 1
        qr_code.save()
        log.info(f'Redirecting QR code from {self.request.path} to {qr_code.to_url}')
        return qr_code.to_url
