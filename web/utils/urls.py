from utils.views import FacebookLoginView, FacebookUserConnectView
from django.urls import path

urlpatterns = [
    # (r'^associate/$', FacebookAssociateView.as_view(), {}, "facebook_auth"),
    path('facebook/login/', FacebookLoginView.as_view(), name="facebook_login"),
    path('facebook/connect/', FacebookUserConnectView.as_view(), name="facebook_connect"),
    # (r'qr/(?P<category>\w+)/(?P<id>\d+)/$', QRFactory.as_view(), {}, "qr_factory")
]
