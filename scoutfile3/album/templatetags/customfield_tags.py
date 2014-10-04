__author__ = 'andrei'

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.inclusion_tag("album/camparbitrar.html", takes_context=True)
def valoare_camp(context, camp, participare):
    valoare = camp.get_value(participare)
    return {"camp": camp, "participare": participare, "valoare": valoare}

@register.simple_tag(takes_context=True)
def camp_special(context, participare, camp):
    return participare.process_camp_aditional(camp)