from django.urls import path, re_path

from redirects.views import PhysicalTagRedirectView

urlpatterns = [
    re_path(r'^tag/(?P<code>[\w-]+)/$', PhysicalTagRedirectView.as_view(), name='tag-redirect'),
]
