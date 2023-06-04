from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from slackbot.api.permissions import SlackVerifiedRequestPermission
from slackbot.api.serializers import SlackEventSerializer
from slackbot.slack_constants import SlackEventTypes


class SlackEventHook(CreateAPIView, GenericAPIView):
    serializer_class = SlackEventSerializer
    permission_classes = [SlackVerifiedRequestPermission, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = serializer.data
        if serializer.data.get("type") == SlackEventTypes.URL_VERIFICATION:
            data = {"challenge": serializer.data.get("challenge")}

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_200_OK, headers=headers)

