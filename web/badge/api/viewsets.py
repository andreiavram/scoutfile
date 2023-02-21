from rest_framework import viewsets

from badge.api.serializers import BadgeSerializer
from badge.models import Badge


class BadgeViewSet(viewsets.ModelViewSet):
    serializer_class = BadgeSerializer
    queryset = Badge.objects.all()
