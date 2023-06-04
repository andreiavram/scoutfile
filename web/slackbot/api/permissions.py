from django.conf import settings
from rest_framework.permissions import BasePermission
from slack_sdk.signature import SignatureVerifier


class SlackVerifiedRequestPermission(BasePermission):
    def has_permission(self, request, view):
        verifier = SignatureVerifier(signing_secret=settings.SLACK_APP_SECRET)
        timestamp = request.headers.get("x-slack-request-timestamp", ["0"])
        signature = request.headers.get("x-slack-signature", [""])
        return verifier.is_valid(request.body, timestamp, signature)
