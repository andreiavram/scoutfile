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
    owner = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    sessions = models.ManyToManyField(TopicGroup, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    source = models.PositiveSmallIntegerField(choices=TopicSource.choices, default=TopicSource.ORGANIC)

    voting_enabled = models.BooleanField(default=False)
    voting_model = models.PositiveSmallIntegerField(choices=VotingModel.choices, default=VotingModel.SIMPLE_MAJORITY)
    quorum_model = models.PositiveSmallIntegerField(choices=QuorumModel.choices, default=QuorumModel.SIMPLE)

    def __str__(self):
        return f"{self.title}"


class VotingOption(models.Model):
    name = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="options")
    description = models.TextField(blank=True)
    carries_motion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class DiscussionItem(models.Model):
    class DiscussionSource(IntegerChoices):
        ORGANIC = 1, "Organic"
        EMAIL = 2, "Email"
        SLACK = 3, "Slack"

    timestamp = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True, related_name="discussion")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    comment = models.TextField()
    documents = models.ManyToManyField(Document, blank=True)
    vote = models.ForeignKey(VotingOption, on_delete=models.CASCADE, related_name="votes", null=True, blank=True)

    source = models.PositiveSmallIntegerField(choices=DiscussionSource.choices, default=DiscussionSource.ORGANIC)
    external_id = models.CharField(max_length=255, null=True, blank=True)

    parent_item = models.ForeignKey("DiscussionItem", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    path = models.CharField(max_length=1024, db_index=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def save(self, *args, **kwargs):
        new_path = f"{self.pk}" if self.pk else "?"

        if self.parent_item:
            new_path = f"{self.parent_item.path}:{new_path}"

        if self.path != new_path:
            self.path = new_path

        super().save(*args, **kwargs)
