__author__ = 'andrei'

import collections

from django import template

from album.models import StatusParticipare

register = template.Library()

@register.inclusion_tag("album/camparbitrar.html", takes_context=True)
def valoare_camp(context, camp, participare):
    valoare = camp.get_representation(participare)
    return {"camp": camp, "participare": participare, "valoare": valoare}

@register.simple_tag(takes_context=True)
def camp_special(context, participare, camp):
    return participare.process_camp_aditional(camp)


@register.inclusion_tag("album/breakdown.html", takes_context=True)
def participare_breakdown(context, tip, target=None):
    data = []
    is_countable = True

    eveniment = context.get("eveniment")
    participari = eveniment.participareeveniment_set.exclude(status_participare=5)
    representation_mapping = ()

    if tip in ("rol", "status_participare"):
        data = [getattr(a, "get_%s_display" % tip)() for a in participari]
    elif tip in ("is_partial", ):
        data = len([a.is_partiala for a in participari if a.is_partiala is True])
        is_countable = False
    elif tip in ("drept_vot", ):
        data = len([a for a in participari if a.membru and a.membru.drept_vot()])
        is_countable = False
    elif tip in ("contribution_option", ):
        data = [a.contribution_option for a in participari]
    elif tip == "camp":
        if target is None or not target.afiseaza_sumar:
            return {}

        data = [a.get_value() for a in target.instante.select_related("participare", "camp").all() if a.participare.status_participare in StatusParticipare.participating_statuses()]
        if target.tip_camp in ("number", "bool"):
            data = [float(a) if a else 0 for a in data]
            data = sum(data)
            if target.tip_camp == 'bool':
                data = int(data)
            is_countable = False
        if target.tip_camp in ("choice", ):
            representation_mapping = target.config.get("choices", ())
            representation_mapping = {str(k): v for k, v in representation_mapping}

    if not is_countable:
        return {"breakdown": {"Total": data}}

    breakdown = dict(collections.Counter(data))
    if representation_mapping:
        breakdown = {representation_mapping[k]: v for k, v in breakdown.items()}

    return {"breakdown": breakdown}
