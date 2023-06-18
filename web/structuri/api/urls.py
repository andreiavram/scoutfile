from django.urls import path
from rest_framework import routers

from structuri.api.viewsets import UtilizatorViewSet, UtilizatorSelfView

app_name = 'structuri'

router = routers.SimpleRouter()
router.register(r'user', viewset=UtilizatorViewSet, basename="user")

urlpatterns = [
    path("me/", UtilizatorSelfView.as_view(), name="self-user")
]
urlpatterns += router.urls

