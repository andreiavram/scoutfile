# coding: utf-8
'''
Created on Aug 28, 2012

@author: yeti
'''


from bootstrap import bootstrap
import datetime
bootstrap("/home/yeti/Workspace/scoutfile3/scoutfile3/")

from scoutfile3.album.models import Eveniment, SetPoze, Imagine

i = 0
for set_poze in SetPoze.objects.all():
    if set_poze.offset_secunde == 0:
        continue
    
    for imagine in set_poze.imagine_set.all():
        imagine.data = datetime.datetime.strptime(imagine.exifdata_set.get(key = "DateTimeOriginal").value, "%Y:%m:%d %H:%M:%S") + datetime.timedelta(seconds = set_poze.offset_secunde)
        imagine.save()
        i += 1
        if i % 100 == 0:
            print "Currently processing %dth photo" % i

#for imagine in Imagine.objects.all():
#    original_date = imagine.exifdata_set.get(key = u"DateTimeOriginal")
#    recorded_date = imagine.data
#    
#    if original_date.value != recorded_date:
#        imagine.data = datetime.datetime.strptime(original_date.value, "%Y:%m:%d %H:%M:%S")
#        imagine.save()
#        print imagine.image
