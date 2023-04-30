from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import IntegerChoices
from django.db.models.options import Options


class VotingSession(models.Model):
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()

    name = models.CharField(max_length=255, blank=True)


class VotingMotion(models.Model):
    class MotionStatus(IntegerChoices):
        PENDING = 0, "În așteptare"
        OPEN = 1, "Vot în curs"
        PAUSED = 2, "Vot suspendat"
        CLOSED = 3, "Vot închis"

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.PositiveSmallIntegerField(choices=MotionStatus.choices, default=MotionStatus.PENDING)
    owner = models.ForeignKey(get_user_model(), null=True, blank=True)
    session = models.ForeignKey(VotingSession, null=True, blank=True, on_delete=models.CASCADE)


class VotingOptions(models.Model):
    name = models.CharField(max_length=255)
    motion = models.ForeignKey(VotingMotion, on_delete=models.CASCADE, related_name="options")

class Vote(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model())
    vote = models.ForeignKey(VotingOptions, on_delete=models.CASCADE, related_name="votes")
