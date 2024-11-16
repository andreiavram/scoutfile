from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from generic.views import Logout, Login, ProjectIndex
from utils.api.views import ObtainAuthorizationTokenView

admin.autodiscover()

from rest_framework_sso.views import obtain_session_token

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    path(r'admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', ProjectIndex.as_view(), name="index"),

    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),

    # url('^markdown/', include('django_markdown.urls')),
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/', include('scoutfile3.api.urls', namespace='api')),
]

urlpatterns += [
    path('api/v1/session/', obtain_session_token, name="session_token"),
    path('api/v1/authorize/', ObtainAuthorizationTokenView.as_view(), name="authorization_token"),
]

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
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
