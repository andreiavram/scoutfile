from django.urls import path, include, re_path

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from generic.views import Login, Logout

urlpatterns = [
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),

    # Wagtail's serving mechanism
    re_path(r'', include(wagtail_urls)),
]

