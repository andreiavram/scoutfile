from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django.views.generic.base import TemplateView
from generic.views import Logout, Login, IndexView, Issues,\
    CreateIssue
admin.autodiscover()

# New import
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = patterns('',
    (r'^structuri/', include('structuri.urls', namespace = 'structuri')),
    (r'^album/', include('album.urls', namespace = 'album')),
    (r'^generic/', include('generic.urls', namespace = 'generic')),
    (r'^patrocle/', include('patrocle.urls', namespace = 'patrocle')),
    (r'^documente/', include('documente.urls', namespace = 'documente')),
    
    (r'issues/$', Issues.as_view(), {}, "issues"),
    (r'issues/create/$', CreateIssue.as_view(), {}, "create_issue"),
    
    ('^$', IndexView.as_view(template_name = "home.html"), {}, "index"),
                       
#     (r'^dajaxice/', include('dajaxice.urls')),
# New style
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    (r'ajax_select/', include('ajax_select.urls')),

    (r'login/$', Login.as_view(), {}, "login"),
    (r'logout/$', Logout.as_view(), {}, "logout"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()