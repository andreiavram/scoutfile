from django.db.models import TextChoices


class SlackEventTypes(TextChoices):
    CALLBACK = "event_callback", "Event Callback"
    URL_VERIFICATION = "url_verification", "URL Verification"
