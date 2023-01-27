from rest_framework_sso import views as sso_views
from utils.api.serializers import ScoutfileAuthorizationTokenSerializer


class ObtainAuthorizationTokenView(sso_views.ObtainAuthorizationTokenView):
    serializer_class = ScoutfileAuthorizationTokenSerializer
