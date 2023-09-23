from django.urls import path
from rest_framework import routers

from album.api.views import ParticipareEvenimentAPIUpdate

app_name = 'album'

router = routers.SimpleRouter()
# router.register(r'user', viewset=UtilizatorViewSet, basename="user")

urlpatterns = [
    path("participare/<int:pk>/", ParticipareEvenimentAPIUpdate.as_view(), name="participare-eveniment")
]
urlpatterns += router.urls

