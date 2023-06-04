from django.urls import path

from slackbot.api.views import SlackEventHook

urlpatterns = [
    path("events/", SlackEventHook.as_view(), name="event-hook"),
]
