from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from structuri.api.permissions import IsOwnUser
from structuri.api.serializers import UserSerializer
from structuri.models import Utilizator


class UtilizatorSelfView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user.utilizator


class UtilizatorViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Utilizator.objects.all()
    permission_classes = [IsAuthenticated, IsOwnUser, ]
