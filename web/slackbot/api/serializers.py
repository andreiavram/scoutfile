from django.db.models import Q
from rest_framework import serializers
from django.conf import settings
from slack_bolt import App

from slackbot.slack_constants import SlackEventTypes
from structuri.models import Membru

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
    event = SlackInnerEventSerializer(required=False)

    class Meta:
        fields = ["token", "type", "challenge", "team_id", "event"]

    def create(self, validated_data):
        if "event" not in validated_data:
            return validated_data

        # TODO: add queue mechanism here to deal with pubsub messages

        if validated_data["event"]["user"] == "U05AT2TT3PX":
            # this is the current slack bot's uid
            return validated_data

        if validated_data["event"]["channel_type"] != "im":
            return validated_data

        user = app.client.users_profile_get(user=validated_data["event"]["user"])

        email = user["profile"]["email"]
        try:
            membru = Membru.objects.get(Q(email__iexact=email) | Q(slack_email__iexact=email))
        except Membru.DoesNotExist:
            text = f"Emailul tau {email} nu este configurat în contul tău de Scoutfile. Vorbește cu yeti să rezolvi!"
            app.client.chat_postMessage(channel=validated_data['event']['channel'], text=text)
            return validated_data

        inquiry = validated_data['event']['text'].lower()
        if "cotizatie" in inquiry or "cotizație" in inquiry or "cotizația" in inquiry or "cotizatia" in inquiry:
            text = f"Cotizația ta este {membru.status_cotizatie()}"
        elif "ccl" in inquiry or "când e ccl" in inquiry or "cand e ccl" in inquiry or "cand e campul" in inquiry or "când e campul" in inquiry:
            text = "Campul Centrului Local este între 12 și 20 august 2023"
        else:
            text = "Nu știu despre ce vorbești ..."

        app.client.chat_postMessage(channel=validated_data['event']['channel'], text=text)
        return validated_data
