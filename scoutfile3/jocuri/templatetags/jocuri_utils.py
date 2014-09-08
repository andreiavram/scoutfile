# coding: utf-8
__author__ = 'andrei'

from django import template
from django.template.defaultfilters import stringfilter

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

@register.filter
def durata_string(value):
    if value.min_durata is not None and value.max_durata is None:
        return u"Cel puțin %d" % value.min_durata
    if value.min_durata is None and value.max_durata is not None:
        return u"Cel mult %d" % value.max_durata
    return u"Între %s și %s" % (value.min_durata, value.max_durata)
