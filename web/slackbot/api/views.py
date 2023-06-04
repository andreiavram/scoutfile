from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response

from slackbot.api.permissions import SlackVerifiedRequestPermission
from slackbot.slack_constants import SlackEventTypes
from slackbot.tasks import process_slack_message


class SlackEventHook(CreateAPIView, GenericAPIView):
    permission_classes = [SlackVerifiedRequestPermission, ]

    def create(self, request, *args, **kwargs):
        if request.data.get("type") == SlackEventTypes.URL_VERIFICATION:
            # pass Slack initial Challenge for URLs
            data = {"challenge": request.data.get("challenge")}
            return Response(data, status=status.HTTP_200_OK)

        process_slack_message.apply_async(kwargs={'data': request.data}, queue="process_slack_messages")
        return Response({"received": True}, status=status.HTTP_200_OK)

