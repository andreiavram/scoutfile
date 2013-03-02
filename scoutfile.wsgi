import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'scoutfile3.settings'

if os.path.exists("/etc/DJANGO_DEV_MACHINE"):
	sys.path.append('/home/yeti/Workspace/scoutfile3/')

	path = '/home/yeti/Workspace/scoutfile3/scoutfile3/'
	if path not in sys.path:
	    sys.path.append(path)
else:
	sys.path.append('/yetiweb/scoutfile/')

	path = '/yetiweb/scoutfile/scoutfile3/'
	if path not in sys.path:
	    sys.path.append(path)
	    

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
