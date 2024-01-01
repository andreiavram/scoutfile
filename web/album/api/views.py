from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from album.api.permissions import WriteAccessParticipareEveniment
from album.api.serializers import ParticipareEvenimentSerializers
from album.models import ParticipareEveniment


class ParticipareEvenimentViewset(viewsets.ModelViewSet):
    queryset = ParticipareEveniment.objects.all()
    serializer_class = ParticipareEvenimentSerializers
    permission_classes = [IsAuthenticated, WriteAccessParticipareEveniment]
