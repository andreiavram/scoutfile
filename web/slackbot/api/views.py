from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from slack_sdk.signature import SignatureVerifier
from django.conf import settings

from slackbot.api.serializers import SlackEventSerializer
from rest_framework.permissions import BasePermission

from slackbot.slack_constants import SlackEventTypes


class SlackVerifiedRequestPermission(BasePermission):
    def has_permission(self, request, view):
        verifier = SignatureVerifier(signing_secret=settings.SLACK_APP_SECRET)
        timestamp = request.headers.get("x-slack-request-timestamp", ["0"])[0]
        signature = request.headers.get("x-slack-signature", [""])[0]
        return verifier.is_valid(request.body, timestamp, signature)


class SlackEventHook(CreateAPIView, GenericAPIView):
    serializer_class = SlackEventSerializer

    def __int__(self, *args, **kwargs):
        self.verifier = None
        super().__init__(*args, **kwargs)

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions.append(SlackVerifiedRequestPermission)
        return permissions

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = serializer.data
        if serializer.data.get("type") == SlackEventTypes.URL_VERIFICATION:
            data = {"challenge": serializer.data.get("challenge")}

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_200_OK, headers=headers)

