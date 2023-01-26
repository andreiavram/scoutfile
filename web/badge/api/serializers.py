from rest_framework import serializers

from badge.models import Badge


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'nume', 'descriere', 'tip', 'tiraj', 'producator']
