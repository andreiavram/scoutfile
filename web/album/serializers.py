from builtins import object
from rest_framework.serializers import ModelSerializer

from album.models import Imagine

__author__ = 'yeti'


class ImageSerializer(ModelSerializer):
    class Meta(object):
        model = Imagine
        fields = ["score"]


