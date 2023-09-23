from rest_framework import routers

from album.api.views import ParticipareEvenimentViewset

app_name = 'album'

router = routers.SimpleRouter()
router.register(r'participare', viewset=ParticipareEvenimentViewset, basename="participare-eveniment")

urlpatterns = [

]
urlpatterns += router.urls

