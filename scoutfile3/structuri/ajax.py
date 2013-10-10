# coding: utf-8
'''
Created on Sep 1, 2012

@author: yeti
'''
from structuri.models import CentruLocal, TipAsociereMembruStructura
from django.shortcuts import get_object_or_404
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.contenttypes.models import ContentType

@dajaxice_register
def get_unitati(request, id_centru_local):
    dajax = Dajax()
    
    centru_local = get_object_or_404(CentruLocal, id = id_centru_local)
    unitati = []
    for unitate in centru_local.unitate_set.all():
        unitati.append({"id" : unitate.id, "nume_complet" : unitate.nume})
    dajax.add_data({"unitati" : unitati}, "update_unitati")
    
    return dajax.json()
    
@dajaxice_register
def update_content_objects(request, ctype_id):
    dajax = Dajax()
    
    ctype = ContentType.objects.get(id = int(ctype_id))
    
    centre_locale_permise = request.user.get_profile().membru.get_centre_locale_permise()
    objects_filters = {u"Centru Local" : {"id__in" : (centru.id for centru in centre_locale_permise)},
                       u"Unitate" : {"centru_local__in" : centre_locale_permise},
                       u"Patrulă" : {"unitate__centru_local__in" : centre_locale_permise}}
    
    dajax.add_data({"objects" : [(obj.id, "%s" % obj) for obj in ctype.model_class().objects.filter(**(objects_filters.get(ctype.name)))],
                    "types" : [(obj.id, "%s" % obj) for obj in TipAsociereMembruStructura.objects.filter(content_types__in = (ctype, ))]
                    }, "after_update_content_objects")
    
    return dajax.json()


