__author__ = 'yeti'

from scoutfile3 import settings

def product_version(request):
    return { "MAJOR_VERSION" : settings.MAJOR_VERSION,
             "MINOR_VERSION" : settings.MINOR_VERSION,
             "REDMINE_VERSION_URL" : settings.REDMINE_VERSION_URL }