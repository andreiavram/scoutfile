from django.db.models import Q
from rest_framework import serializers
from django.conf import settings
from slack_bolt import App

from slackbot.slack_constants import SlackEventTypes
from structuri.models import Membru


class SlackInnerEventSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    channel = serializers.CharField()
    user = serializers.CharField()
    text = serializers.CharField()
    ts = serializers.CharField()
    event_ts = serializers.CharField(required=True)
    channel_type = serializers.CharField()


class SlackEventSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=SlackEventTypes.choices)
    challenge = serializers.CharField(required=False)
    team_id = serializers.CharField(required=False)
    event = SlackInnerEventSerializer(required=False)
    event_id = serializers.CharField(required=True)
    event_time = serializers.CharField()
    authed_users = serializers.ListSerializer()
    api_app_id = serializers.CharField()

    class Meta:
        fields = ["token", "type", "challenge", "team_id", "event"]

    def create(self, validated_data):
        if "event" not in validated_data:
            return validated_data

        if validated_data["event"]["user"] == "U05AT2TT3PX":
            # this is the current slack bot's uid
            return validated_data

        if validated_data["event"]["channel_type"] != "im":
            return validated_data

