# coding: utf-8
__author__ = 'andrei'

from django import template
from django.template.defaultfilters import stringfilter
import datetime

register = template.Library()

@register.filter
def numar_participanti_string(value):
    if value.min_participanti is None and value.max_participanti is None:
        return u"Oricâți"
    if value.min_participanti is not None and value.max_participanti is None:
        return u"Minim %d" % value.min_participanti
    if value.min_participanti is None and value.max_participanti is not None:
        return u"Maxim %d" % value.max_participanti
    return u" Între %s și %s" % (value.min_participanti, value.max_participanti)


def seconds_to_string(value):
    td = datetime.timedelta(seconds=value)
    weeks, days, hours, minutes = td.days // 7, td.days % 7, td.seconds // 3600, td.seconds // 60 % 60
    output = ""
    if weeks:
        output += u"%d săptămâni"
    if days:
        output += ", " if len(output) else ""
        output += "%d zile" % days
    if hours:
        output += ", " if len(output) else ""
        output += "%d ore" % hours
    if minutes:
        output += ", " if len(output) else ""
        output += "%d minute" % minutes
    return output

@register.filter
def durata_string(value):
    if not value.min_durata and not value.max_durata:
        return u"-"
    if value.min_durata and not value.max_durata:
        return u"Cel puțin %s" % seconds_to_string(value.min_durata)
    if not value.min_durata and value.max_durata:
        return u"Cel mult %s" % seconds_to_string(value.max_durata)
    return u"Între %s și %s" % (seconds_to_string(value.min_durata), seconds_to_string(value.max_durata))
