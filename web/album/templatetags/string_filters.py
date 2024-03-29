__author__ = 'andrei'

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def newlines(value):
    return value.replace("\r\n", "\\n")

