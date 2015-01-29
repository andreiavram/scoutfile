# coding: utf-8
'''
Created on Jul 1, 2012

Handles ajax requests (dajaxice) 

@author: yeti
'''
from dajax.core import Dajax
from django.shortcuts import get_object_or_404
import logging
from django.contrib.contenttypes.models import ContentType
from dajaxice.decorators import dajaxice_register
from documente.models import ChitantaCotizatie

logger = logging.getLogger(__name__)

@dajaxice_register
def toggle_blocat_cotizatie(request, document):
    dajax = Dajax()

    document = get_object_or_404(ChitantaCotizatie, id=int(document))
    document.blocat = not document.blocat
    document.save()

    dajax.add_data({"document": document.id, "blocat": document.blocat}, "after_toggle_blocat")

    return dajax.json()