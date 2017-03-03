from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from structuri.models import CentruLocal, Unitate, Patrula, Membru, AsociereMembruStructura, InformatieContact

from structuri.decorators import redirect_with_error

__author__ = 'yeti'


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

            lookups = {"Centru Local" : lambda : get_object_or_404(CentruLocal, id=kwargs.get(pkname)),
             "Unitate" :  lambda : get_object_or_404(Unitate, id=kwargs.get(pkname)),
             "Patrula" : lambda : get_object_or_404(Patrula, id = kwargs.get(pkname)).unitate.centru_local,
             "Unitate, Centru Local" :  lambda : get_object_or_404(Unitate, id = kwargs.get(pkname)).centru_local,
             "Patrula, Unitate, Centru Local" : lambda : get_object_or_404(Patrula, id = kwargs.get(pkname)).unitate.centru_local,
             "Patrula, Unitate" : lambda : get_object_or_404(Patrula, id = kwargs.get(pkname)).unitate,
             "Membru, Centru Local" : lambda : get_object_or_404(Membru, id = kwargs.get(pkname)).get_centru_local(),
             "Membru, Unitate" : lambda : get_object_or_404(Membru, id = kwargs.get(pkname)).get_unitate(),
             "Membru, Patrula" : lambda : get_object_or_404(Membru, id = kwargs.get(pkname)).get_patrula(),
             "Afiliere, Membru, *, Centru Local" : lambda : get_object_or_404(AsociereMembruStructura, id = kwargs.get(pkname)).get_structura(ContentType.objects.get_for_model(CentruLocal)),
             "Afiliere, Membru, *, Unitate" : lambda : get_object_or_404(AsociereMembruStructura, id = kwargs.get(pkname)).get_structura(ContentType.objects.get_for_model(Unitate)),
             "Afiliere, Membru, *, Patrula" : lambda : get_object_or_404(AsociereMembruStructura, id = kwargs.get(pkname)).get_structura(ContentType.objects.get_for_model(Patrula)),
             "InformatieContact, Centru Local" : lambda : get_object_or_404(InformatieContact, id = kwargs.get(pkname)).content_object,
             "InformatieContact, Membru, Centru Local" : lambda : get_object_or_404(InformatieContact, id = kwargs.get(pkname)).content_object.centru_local,
             }

            text_asocieri = ", ".join(["%s @ %s" % (s, a) for s, a in asocieri])

            if not args[0].user.is_authenticated():
                return redirect_with_error(args[0], text_asocieri)

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

                    login_ok = login_ok or False

                login_ok = login_ok or True

            if not login_ok:
                return redirect_with_error(args[0], text_asocieri)
            return view_func(self, *args, **kwargs)
        return _wrapper
    return _view_wrapper