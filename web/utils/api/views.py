import rest_framework_sso

from utils.api.serializers import AuthorizationTokenSerializer


class ObtainAuthorizationTokenView(rest_framework_sso.views.ObtainAuthorizationTokenView):
    serializer_class = AuthorizationTokenSerializer
