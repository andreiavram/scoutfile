from rest_framework import serializers
from django.conf import settings
from slack_bolt import App

from slackbot.slack_constants import SlackEventTypes

app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_APP_SECRET
)


class SlackInnerEventSerializer(serializers.Serializer):
    type = serializers.CharField()
    channel = serializers.CharField()
    user = serializers.CharField()
    text = serializers.CharField()
    ts = serializers.CharField()
    event_ts = serializers.CharField()
    channel_type = serializers.CharField()


class SlackEventSerializer(serializers.Serializer):
    token = serializers.CharField()
    type = serializers.ChoiceField(choices=SlackEventTypes.choices)
    challenge = serializers.CharField(required=False)
    team_id = serializers.CharField(required=False)
    event = SlackInnerEventSerializer()

    class Meta:
        fields = ["token", "type", "challenge", "team_id", "event"]

    def create(self, validated_data):
        # TODO: add queue mechanism here to deal with pubsub messages
        app.client.chat_postMessage(channel=validated_data['event']['channel'], text=validated_data['event']['text'])
        return validated_data
