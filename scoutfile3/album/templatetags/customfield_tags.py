from album.models import ParticipareEveniment

__author__ = 'andrei'

from django import template
from django.template.defaultfilters import stringfilter
import collections

register = template.Library()

@register.inclusion_tag("album/camparbitrar.html", takes_context=True)
def valoare_camp(context, camp, participare):
    valoare = camp.get_value(participare)
    return {"camp": camp, "participare": participare, "valoare": valoare}

@register.simple_tag(takes_context=True)
def camp_special(context, participare, camp):
    return participare.process_camp_aditional(camp)


@register.inclusion_tag("album/breakdown.html", takes_context=True)
def participare_breakdown(context, tip, target=None):
    data = []
    is_countable = True
    eveniment = context.get("eveniment")
    if tip in ("rol", "status_participare"):
        data = [getattr(a, "get_%s_display" % tip)() for a in eveniment.participareeveniment_set.all()]

    if tip in ("is_partial", ):
        data = len([a.is_partiala for a in eveniment.participareeveniment_set.all() if a.is_partiala is True])
        is_countable = False

    if tip == "camp":
        if target is None or not target.afiseaza_sumar:
            return {}

        data = [a.get_value() for a in target.instante.all()]
        if target.tip_camp in ("number", "bool"):
            data = [float(a) if a else 0 for a in data]
            data = sum(data)
            if target.tip_camp == 'bool':
                data = int(data)
            is_countable = False

    if not is_countable:
        return {"breakdown": {"Total": data}}
    return {"breakdown": dict(collections.Counter(data))}
