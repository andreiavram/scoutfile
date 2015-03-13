__author__ = 'yeti'

from django.conf import settings

def product_version(request):
    return { "MAJOR_VERSION" : settings.MAJOR_VERSION,
             "MINOR_VERSION" : settings.MINOR_VERSION,
             "REDMINE_VERSION_URL" : settings.REDMINE_VERSION_URL }


def api_keys(request):
    return { "GOOGLE_API_KEY" : settings.GOOGLE_API_KEY }


def url_root(request):
    return { "url_root" : settings.URL_ROOT.strip("/") }