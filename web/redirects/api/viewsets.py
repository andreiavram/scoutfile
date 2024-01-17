from rest_framework import viewsets, permissions

from redirects.api.filters import PhysicalTagFilter
from redirects.api.serializers import PhysicalTagSerializer
from redirects.models import PhysicalTag


class PhysicalTagViewSet(viewsets.ModelViewSet):
    queryset = PhysicalTag.objects.all()
    serializer_class = PhysicalTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = PhysicalTagFilter
