from rest_framework import serializers

from album.models import ParticipareEveniment, Eveniment, EventContributionOption


class EvenimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eveniment
        fields = ["id", "slug", "nume"]


class EvenimentContributionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventContributionOption
        fields = ["id", "eveniment_id", "value", "description", "is_default", "per_diem"]


class ParticipareEvenimentSerializers(serializers.ModelSerializer):
    class Meta:
        model = ParticipareEveniment
        fields = [
            "id",
            "membru_id",
            "nonmembru",
            "eveniment",
            "data_sosire",
            "data_plecare",
            "status_participare",
            "status_participare_display",
            "detalii",
            "participant_notes",
            "rol",
            "ultima_modificare",
            "user_modificare_id",
            "contribution_option",
            "contribution_payments",
        ]
        read_only_fields = ["id", "membru_id", "nonmembru", "eveniment", "ultima_modificare", "user_modificare_id"]

    eveniment = EvenimentSerializer(read_only=True)
    contribution_option = EvenimentContributionOptionSerializer(read_only=True)
    status_participare_display = serializers.SerializerMethodField()

    def get_status_participare_display(self, obj):
        return obj.get_status_participare_display()
