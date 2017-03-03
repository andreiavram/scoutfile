from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from generic.views import Logout, Login, IndexView, Issues, CreateIssue

admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = \
    patterns('',
             url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
             url(r'^admin/', include(admin.site.urls)),

             (r'^structuri/', include('structuri.urls', namespace='structuri')),
             (r'^album/', include('album.urls', namespace='album')),
             (r'^goodies/', include('goodies.urls', namespace='goodies')),
             (r'^patrocle/', include('patrocle.urls', namespace='patrocle')),
             (r'^documente/', include('documente.urls', namespace='documente')),
             (r'^extra/', include('extra.urls', namespace='extra')),
             (r'^utils/', include('utils.urls', namespace='utils')),
             (r'^cantece/', include('cantece.urls', namespace='cantece')),
             (r'^jocuri/', include('jocuri.urls', namespace='jocuri')),
             (r'^badge/', include('badge.urls', namespace='badge')),
             (r'^inventar/', include('inventar.urls', namespace='inventar')),

             (r'issues/$', Issues.as_view(), {}, "issues"),
             (r'issues/create/$', CreateIssue.as_view(), {}, "create_issue"),

             ('^$', IndexView.as_view(template_name="home.html"), {}, "index"),

             (r'^ajax_select/', include('ajax_select.urls')),
             (r'^photologue/', include('photologue.urls')),


             (r'login/$', Login.as_view(), {}, "login"),
             (r'logout/$', Logout.as_view(), {}, "logout"),

             url('^markdown/', include('django_markdown.urls')),
             url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
             )

urlpatterns += staticfiles_urlpatterns()

#    temp media fix
if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                            }),
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )


handler500 = "scoutfile3.generic.views.custom_500"