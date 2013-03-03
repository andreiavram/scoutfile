import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'scoutfile3.settings'


components =  os.path.dirname(__file__).split(os.sep)
PROJECT_ROOT = str.join(os.sep, components)

ALLDIRS = [ ]

import sys 
import site 

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path 


sys.path.append(PROJECT_ROOT + "/scoutfile3/")

for path in paths:
	if path not in sys.path:
		sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
