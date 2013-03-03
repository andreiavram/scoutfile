# coding: utf-8
'''
Created on Jul 1, 2012

Handles ajax requests (dajaxice) 

@author: yeti
'''
from dajax.core import Dajax
import logging
from django.contrib.contenttypes.models import ContentType
from dajaxice.decorators import dajaxice_register
logger = logging.getLogger(__name__)

@dajaxice_register
def delete_action(request, obj_id, obj_ctype_id, prefix):
    dajax = Dajax()

    try:
        delete_object(request, obj_id = obj_id, obj_ctype_id = obj_ctype_id)
        dajax.add_data({"error_msg" : u"", "obj_id" : obj_id}, "after_generic_delete_%s" % prefix)
    except:
        dajax.add_data({"error_msg" : u"Nu am putut șterge obiectul. Contactați administratorul."}, "after_generic_delete_%s" % prefix)
        
    return dajax.json()


def delete_object(request, obj_model = None, obj_id = None, obj = None, obj_ctype = None, obj_ctype_id = None):
    if obj == None and ((obj_model == None and obj_ctype == None and obj_ctype_id == None) or obj_id == None):
        raise ValueError(u"delete_object are nevoie fie de obiect, fie de tipul obiectului si ID")
    
    try:
        if obj == None:
            if obj_model == None:
                if obj_ctype == None:
                    obj_ctype = ContentType.objects.get(id = obj_ctype_id)
                obj_model = obj_ctype.model_class() 
        
            obj = obj_model.objects.get(id = int(obj_id))
        
        if hasattr(obj, 'status'):
            obj.status =  2
            obj.save()
        else:
            obj.delete()
        
        return True
    except Exception, e:
        logger.error(e)
        raise e
            
    raise Exception(u"Obiectul nu a putut fi șters - a intervenit o eroare generică.")    