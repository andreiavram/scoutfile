from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated

from album.api.permissions import WriteAccessParticipareEveniment
from album.api.serializers import ParticipareEvenimentSerializers
from album.models import ParticipareEveniment


class ParticipareEvenimentAPIUpdate(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = ParticipareEveniment.objects.all()
    serializer_class = ParticipareEvenimentSerializers
    permission_classes = [IsAuthenticated, WriteAccessParticipareEveniment]
