from rest_framework.serializers import ModelSerializer

from album.models import Imagine

__author__ = 'yeti'


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Imagine
        fields = ["score"]


