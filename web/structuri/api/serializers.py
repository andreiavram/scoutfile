from rest_framework import serializers

from structuri.models import Utilizator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizator
        fields = ["id", "user_id", "email", "is_active", "nume_complet", "nume", "prenume"]

    is_active = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_is_active(self, obj):
        return obj.user.is_active

    def get_user_id(self, obj):
        return obj.user.id


