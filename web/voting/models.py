from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import IntegerChoices
from django.db.models.options import Options

from documente.models import Document


class VotingModel(IntegerChoices):
    SIMPLE_MAJORITY = 1, "50% + 1"
    TWO_THRIDS = 2, "2 / 3"


class QuorumModel(IntegerChoices):
    SIMPLE = 1, "50% + 1"
    TWO_THRIDS = 2, "2 / 3"


class TopicGroup(models.Model):
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()

    name = models.CharField(max_length=255, blank=True)


class Topic(models.Model):
    class TopicStatus(IntegerChoices):
        PENDING = 0, "Propusă"
        OPEN = 1, "Deschisă"
        PAUSED = 2, "Vot suspendat"
        CLOSED = 3, "Vot finalizat"

    class TopicSource(IntegerChoices):
        ORGANIC = 1, "Organic"
        SLACK = 2, "Slack"

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.PositiveSmallIntegerField(choices=TopicStatus.choices, default=TopicStatus.PENDING)
    owner = models.ForeignKey(get_user_model(), null=True, blank=True)
    sessions = models.ManyToManyField(TopicGroup, null=True, blank=True)

    created = models.DateTimeField()
    source = models.PositiveSmallIntegerField(choices=TopicSource.choices, default=TopicSource.ORGANIC)

    voting_enabled = models.BooleanField(default=False)
    voting_model = models.PositiveSmallIntegerField(choices=VotingModel.choices, default=VotingModel.SIMPLE_MAJORITY)
    quorum_model = models.PositiveSmallIntegerField(choices=QuorumModel.choices, default=QuorumModel.SIMPLE)


class VotingOptions(models.Model):
    name = models.CharField(max_length=255)
    motion = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="options")


class DiscussionItem(models.Model):
    class DiscussionSource(IntegerChoices):
        ORGANIC = 1, "Organic"
        EMAIL = 2, "Email"
        SLACK = 3, "Slack"

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    comment = models.TextField()
    documents = models.ManyToManyField(Document, null=True, blank=True)
    vote = models.ForeignKey(VotingOptions, on_delete=models.CASCADE, related_name="votes")

    source = models.PositiveSmallIntegerField(DiscussionSource.choices, default=DiscussionSource.ORGANIC)
    external_id = models.CharField(max_length=255, null=True, blank=True)

    parent_topic = models.ForeignKey("DiscussionItem", null=True, blank=True, on_delete=models.CASCADE)
