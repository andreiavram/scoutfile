from rest_framework import serializers

from voting.models import Topic, VotingOption, DiscussionItem


class VotingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingOption
        fields = ["name", "description"]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["title", "description", "status", "owner", "sessions", "created", "source",
                  "voting_enabled", "voting_model", "quorum_model", "options", "discussion_count"]
        read_only_fields = ["sessions", "created"]

    options = VotingOptionSerializer(many=True)
    discussion_count = serializers.SerializerMethodField()

    def get_discussion_count(self, obj):
        return obj.discussion.all().count()


class DiscussionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussionItem
        fields = ["timestamp", "topic", "user", "comment", "documents", "vote", "source", "external_id",
                  "parent_topic", "topic_path", "reply_count"]

    reply_count = serializers.SerializerMethodField()

    def get_reply_count(self, obj):
        return obj.replies.all().filter(topic_path__startswith=obj.topic_path).count()
