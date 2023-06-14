from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from generic.views import Logout, Login, IndexView, Issues, CreateIssue
from utils.api.views import ObtainAuthorizationTokenView

admin.autodiscover()

from rest_framework_sso.views import obtain_session_token

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [path(r'admin/doc/', include('django.contrib.admindocs.urls')),
               path('admin/', admin.site.urls),
               path('structuri/', include(('structuri.urls', 'structuri'), namespace='structuri')),
               path('album/', include(('album.urls', 'album'),  namespace='album')),
               path('goodies/', include(('goodies.urls', 'goodies'),  namespace='goodies')),
               path('patrocle/', include(('patrocle.urls', 'patrocle'),  namespace='patrocle')),
               path('documente/', include(('documente.urls', 'documente'),  namespace='documente')),
               path('extra/', include(('extra.urls', 'extra'),  namespace='extra')),
               path('utils/', include(('utils.urls', 'utils'),  namespace='utils')),
               path('cantece/', include(('cantece.urls', 'cantece'),  namespace='cantece')),
               path('jocuri/', include(('jocuri.urls', 'jocuri'),  namespace='jocuri')),
               path('badge/', include(('badge.urls', 'badge'),  namespace='badge')),
               path('inventar/', include(('inventar.urls', 'inventar'),  namespace='inventar')),
               path('slack/', include(("slackbot.urls", "slack"), namespace="slack")),
               path('redirect/', include(("redirects.urls", "redirects"), namespace="redirects")),

               path('issues/', Issues.as_view(), name="issues"),
               path('issues/create/', CreateIssue.as_view(), name="create_issue"),

               path('', IndexView.as_view(template_name="home.html"), name="index"),

               path('ajax_select/', include('ajax_select.urls')),
               path('photologue/', include('photologue.urls')),

               path('login/', Login.as_view(), name="login"),
               path('logout/', Logout.as_view(), name="logout"),

               # url('^markdown/', include('django_markdown.urls')),
               path('api-auth/', include(('rest_framework.urls', 'rest_framework'),  namespace='rest_framework')),
               path('api/v1/', include('scoutfile3.api.urls', namespace='api')),
               ]

urlpatterns += [
    path('api/session/', obtain_session_token, name="session_token"),
    path('api/authorize/', ObtainAuthorizationTokenView.as_view(), name="authorization_token"),
]

# urlpatterns += staticfiles_urlpatterns()

#    temp media fix
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

urlpatterns += [
    path('wagtail/admin/', include(wagtailadmin_urls)),
    path('wagtail/documents/', include(wagtaildocs_urls)),

    # Wagtail's serving mechanism
    re_path(r'wagtail/', include(wagtail_urls)),
]


# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

handler500 = "generic.views.custom_500"
