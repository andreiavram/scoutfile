# coding: utf-8
'''
Created on Sep 18, 2012

@author: yeti
'''
import logging

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from album.models import Eveniment
from album.models import Imagine, ParticipareEveniment
from structuri.models import CentruLocal, Patrula, Unitate, Membru,\
    AsociereMembruStructura, InformatieContact

logger = logging.getLogger()

def redirect_with_error(request, msg = None):
    messages.error(request, u"Nu ai suficiente drepturi pentru această acțiune (%s)" % msg)
    return HttpResponseRedirect(reverse("login") + "?err")


def allow_by_afiliere(asocieri, pkname = "pk", combine = False):
    def _view_wrapper(view_func):
        def _wrapper(self, *args, **kwargs):
            
            #    skip checks if dispatch method is being called from a child class for some reason
            #    and the child class has different checks then us
            if "skip_checks" in kwargs.keys() and kwargs['skip_checks']:
                return view_func(self, *args, **kwargs)
            
            #    pass-through for system administrators
            if args[0].user.groups.filter(name__icontains = u"administrator").count():
                return view_func(self, *args, **kwargs)


            text_asocieri = ", ".join(["%s @ %s" % (s, a) for s, a in asocieri])

            if not args[0].user.is_authenticated():
                return redirect_with_error(args[0], text_asocieri)
            
            lookups = {"Centru Local" : lambda : get_object_or_404(CentruLocal, id = kwargs.get(pkname)),
             "Unitate" :  lambda : get_object_or_404(Unitate, id = kwargs.get(pkname)),
             "Patrula": lambda : get_object_or_404(Patrula, id = kwargs.get(pkname)).unitate.centru_local,
             "Unitate, Centru Local": lambda : get_object_or_404(Unitate, id = kwargs.get(pkname)).centru_local,
             "Patrula, Unitate, Centru Local": lambda : get_object_or_404(Patrula, id = kwargs.get(pkname)).unitate.centru_local,
             "Patrula, Unitate": lambda : get_object_or_404(Patrula, id = kwargs.get(pkname)).unitate,
             "Membru, Centru Local": lambda: get_object_or_404(Membru, id=kwargs.get(pkname)).get_centru_local(),
             "Membru, Unitate": lambda : get_object_or_404(Membru, id = kwargs.get(pkname)).get_unitate(),
             "Membru, Patrula": lambda : get_object_or_404(Membru, id = kwargs.get(pkname)).get_patrula(),
             "Afiliere, Membru, *, Centru Local": lambda : get_object_or_404(AsociereMembruStructura, id = kwargs.get(pkname)).get_structura(ContentType.objects.get_for_model(CentruLocal)),
             "Afiliere, Membru, *, Unitate": lambda : get_object_or_404(AsociereMembruStructura, id = kwargs.get(pkname)).get_structura(ContentType.objects.get_for_model(Unitate)),
             "Afiliere, Membru, *, Patrula": lambda : get_object_or_404(AsociereMembruStructura, id = kwargs.get(pkname)).get_structura(ContentType.objects.get_for_model(Patrula)),
             "InformatieContact, Centru Local": lambda : get_object_or_404(InformatieContact, id = kwargs.get(pkname)).content_object,
             "InformatieContact, Membru, Centru Local": lambda : get_object_or_404(InformatieContact, id = kwargs.get(pkname)).content_object.centru_local,
             "Eveniment, Centru Local": lambda: get_object_or_404(Eveniment, slug=kwargs.get(pkname)).centru_local,
             "Utilizator, Centru Local": lambda: args[0].user.utilizator.membru.centru_local,
             "Imagine, Centru Local": lambda: get_object_or_404(Imagine, pk=kwargs.get(pkname)).set_poze.eveniment.centru_local,
             "Participare, Eveniment, Centru Local": lambda: get_object_or_404(ParticipareEveniment, pk=kwargs.get(pkname)).eveniment.centru_local,
             }

            
            login_ok = False
            for structura_ref, calitate in asocieri:
                if not structura_ref in lookups.keys():
                    if combine:
                        login_ok = False
                        break
                    continue
                            
                structura = lookups[structura_ref]()

                if not structura or not args[0].user.utilizator.membru.are_calitate(calitate, structura):
                    if combine:
                        login_ok = False
                        break

                    # login_ok = login_ok or False
                    logger.debug("allow_by_afiliere matched rule! %s %s" % (structura_ref, calitate))
                else:
                    login_ok = True

                #login_ok = login_ok or True

            if not login_ok:
                return redirect_with_error(args[0], text_asocieri)
            return view_func(self, *args, **kwargs)
        return _wrapper
    return _view_wrapper