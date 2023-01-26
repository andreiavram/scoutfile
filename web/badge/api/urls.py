from rest_framework import routers

from badge.api.viewsets import BadgeViewSet

app_name = 'badge'

router = routers.SimpleRouter()
router.register('badges', BadgeViewSet)


urlpatterns = []
urlpatterns += router.urls
