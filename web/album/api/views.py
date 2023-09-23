from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from album.api.permissions import WriteAccessParticipareEveniment
from album.api.serializers import ParticipareEvenimentSerializers
from album.models import ParticipareEveniment


class ParticipareEvenimentViewset(viewsets.ModelViewSet):
    queryset = ParticipareEveniment.objects.all()
    serializer_class = ParticipareEvenimentSerializers
    permission_classes = [IsAuthenticated, WriteAccessParticipareEveniment]
