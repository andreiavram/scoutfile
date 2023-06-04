from rest_framework import serializers

from slackbot.slack_constants import SlackEventTypes


class SlackEventSerializer(serializers.Serializer):
    token = serializers.CharField()
    type = serializers.ChoiceField(choices=SlackEventTypes.choices)
    challenge = serializers.CharField(required=False)

    class Meta:
        fields = ["token", "type", "challenge"]
