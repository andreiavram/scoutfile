# coding: utf-8
'''
Created on Aug 28, 2012

@author: yeti
'''
from django.shortcuts import get_object_or_404
from album.models import Imagine
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def vote_picture(request, picture_id, score):
    dajax = Dajax()
    picture = get_object_or_404(Imagine, id = picture_id)
    
    if "has_voted_%d" % picture_id in request.session:
        return dajax.json()
    
    request.session["has_voted_%d" % picture_id] = True
    
    if score >= 0:
        score = 1
    elif score < 0:
        score = -1
    
    picture.vote_photo(score)
    dajax.add_data({"picture_id" : picture_id, "current_score" : picture.score}, "after_vote")
    
    return dajax.json()
        
        
    