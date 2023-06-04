from celery import shared_task
from slack_bolt import App
from django.conf import settings

from structuri.models import Membru

slack_app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_APP_SECRET
)


@shared_task
def process_slack_message(data=None):
    user = slack_app.client.users_profile_get(user=data["event"]["user"])

    email = user["profile"]["email"]
    try:
        membru = Membru.objects.get(Q(email__iexact=email) | Q(slack_email__iexact=email))
    except Membru.DoesNotExist:
        text = f"Emailul tau {email} nu este configurat în contul tău de Scoutfile. Vorbește cu yeti să rezolvi!"
        slack_app.client.chat_postMessage(channel=data['event']['channel'], text=text)
        return data

    inquiry = data['event']['text'].lower()
    if "cotizatie" in inquiry or "cotizație" in inquiry or "cotizația" in inquiry or "cotizatia" in inquiry:
        text = f"Cotizația ta este {membru.status_cotizatie()}"
    elif "ccl" in inquiry or "când e ccl" in inquiry or "cand e ccl" in inquiry or "cand e campul" in inquiry or "când e campul" in inquiry:
        text = "Campul Centrului Local este între 12 și 20 august 2023"
    else:
        text = "Nu știu despre ce vorbești ..."

    slack_app.client.chat_postMessage(channel=data['event']['channel'], text=text)
    return data

