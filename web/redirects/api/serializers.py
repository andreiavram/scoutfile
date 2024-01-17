from rest_framework import serializers
from redirects.models import PhysicalTag


class PhysicalTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalTag
        fields = [
            "created", "modified", "active", "ref", "token", "to_url", "hit_count", "tag_type",
            "svg_qr_image_url", "png_qr_image_url", "url", "id"
        ]

    hit_count = serializers.IntegerField(read_only=True)
    token = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
