from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Notification(models.Model):
    actor_id = models.PositiveIntegerField(null=True, blank=True)
    actor_ctype = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, related_name="actor_notifications")
    actor = GenericForeignKey(ct_field="actor_ctype", fk_field="actor_id")

    target_id = models.PositiveIntegerField()
    target_ctype = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="target_notifications")

    # notifications
    # invited to an event
    # reminded to pay fees
    # invitation to topics

    requires_reply = models.BooleanField(default=False)
    reply_options = models.JSONField()


class NotificationChannel(models.Model):
    class NotificationType(models.TextChoices):
        EMAIL_LIST = "email-list", "Email List"
        SLACK = "slack", "Slack"
        SMS = "sms", "SMS",

    notification_type = models.CharField(max_length=255, choices=NotificationType.choices, default=NotificationType.EMAIL_LIST)
    config = models.JSONField()


class NotificatonMessage(models.Model):
    class NotificationStatus(models.TextChoices):
        PENDING = "queued", "Queued"
        SENT = "sent", "Sent"
        CONFIRMED = "confirmed", "Confirmed"
        ERROR = "error", "Error"


    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="instances")
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, )
