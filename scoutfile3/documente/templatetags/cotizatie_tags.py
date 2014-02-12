# coding: utf8
__author__ = 'andrei'

from django import template
register = template.Library()

@register.filter(name='cotizatie_level')
def cotizatie_level(value):
    if value > 0:
        return "danger"
    if value == 0:
        return "info"
    if value < 0:
        return "success"


@register.filter(name='cotizatie_description')
def cotizatie_description(value):
    trimestru_string = "trimestre" if abs(value) > 1 else "trimestru"
    if value > 0:
        return u"în urmă cu %d %s" % (abs(value), trimestru_string)
    if value == 0:
        return u"la zi"
    if value < 0:
        return u"avans pentru %d %s" % (abs(value), trimestru_string)