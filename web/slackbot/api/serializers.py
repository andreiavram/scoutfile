from rest_framework import serializers

from slackbot.slack_constants import SlackEventTypes


class SlackEventSerializer(serializers.Serializer):
    token = serializers.CharField()
    type = serializers.ChoiceField(choices=SlackEventTypes.choices)
    challenge = serializers.CharField(required=False)

    class Meta:
        fields = ["token", "type", "challenge"]

    def create(self, validated_data):
        # TODO: add queue mechanism here to deal with pubsub messages
        return validated_data
