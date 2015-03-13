# coding: utf-8
'''
Created on Aug 28, 2012

@author: yeti
'''


from bootstrap import bootstrap
bootstrap("/yetiweb/scoutfile/scoutfile3/")

import datetime
from structuri.models import Membru


membri = Membru.objects.all()
count = 0
for membru in membri:
    if membru.afilieri.all().count() == 0:
        print membru
        count += 1
        
        
print "Total %s oameni cu probleme" % count