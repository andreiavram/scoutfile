from django.contrib.auth import get_user_model
from rest_framework import serializers


class AuthorizationTokenSerializer(serializers.Serializer):
    account = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.all(),
        required=True,
        view_name='api:account-detail',
    )

    class Meta:
        fields = ['account']
