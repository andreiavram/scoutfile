# coding: utf-8
'''
Created on Aug 28, 2012

@author: yeti
'''

import os

from bootstrap import bootstrap

bootstrap("/yetiweb/scoutfile/scoutfile3/")

from album import Eveniment, SetPoze, Imagine

root_linked_path = "/media/rojam_photos/alba/"
media_path_prefix = "ccl2012"
photo_import_paths = ["andreibregar/", "andra/", "yeti/", "irina/", "iuli/", "stefana/", "ioana/", "paul/", "popi/"]
e = Eveniment.objects.get(slug = "ccl2012") 

def process_directory(args, dirname, filenames):
    if not os.path.exists("%s/authors.txt" % dirname):
        return

    with open("%s/authors.txt" % dirname, "rt") as f:
        author = f.read()

    set_poze, created = SetPoze.objects.get_or_create(eveniment = e, autor = author)
    if created:
        set_poze.save()
    
    new_path = "%s/%s" % (media_path_prefix, dirname.lstrip(root_linked_path))
    
    for filename in filenames:
        if os.path.splitext(filename)[1][1:].upper() != "JPG":
            continue
        
        print filename
        img = Imagine()
        img.set_poze = set_poze
        img.image = "%s/%s" % (new_path, filename)
        img.save() 

for current_dir in photo_import_paths:
    os.path.walk("%s%s" % (root_linked_path, current_dir), process_directory, None)
    print "Done with %s" % current_dir