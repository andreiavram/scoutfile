from django.conf.urls import patterns, include, url
from utils.views import FacebookLoginView, FacebookUserConnectView

urlpatterns = patterns('',
                       # (r'^associate/$', FacebookAssociateView.as_view(), {}, "facebook_auth"),
                       (r'^facebook/login/', FacebookLoginView.as_view(), {}, "facebook_login"),
                       (r'^facebook/connect/', FacebookUserConnectView.as_view(), {}, "facebook_connect"),
)
