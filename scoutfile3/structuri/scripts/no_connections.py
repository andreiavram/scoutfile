# coding: utf-8
'''
Created on Aug 28, 2012

@author: yeti
'''


from bootstrap import bootstrap
bootstrap("/yetiweb/scoutfile/scoutfile3/")

import datetime
from scoutfile3.structuri.models import Membru


from scoutfile3.album.models import Eveniment, SetPoze, Imagine

membri = Membru.objects.all()
count = 0
for membru in membri:
    if membru.afilieri.all().count() == 0:
        print membru
        count += 1
        
        
print "Total %s oameni cu probleme" % count