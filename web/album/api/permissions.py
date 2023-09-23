from rest_framework.permissions import BasePermission

from structuri.decorators import allow_by_afiliere
from structuri.models import Membru


class WriteAccessParticipareEveniment(BasePermission):
    def has_object_permission(self, request, view, obj):
        centru_local = obj.eveniment.centru_local
        try:
            membru = request.user.membru
        except Membru.DoesNotExist:
            return False

        return membru.are_calitate("Lider", centru_local)


