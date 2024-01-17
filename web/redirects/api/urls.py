from rest_framework import routers

from redirects.api.viewsets import PhysicalTagViewSet

app_name = 'redirects'

router = routers.SimpleRouter()
router.register(r'physicaltag', viewset=PhysicalTagViewSet, basename="physicaltag")

urlpatterns = [

]
urlpatterns += router.urls

