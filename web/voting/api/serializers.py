from rest_framework import serializers

from voting.models import Topic, VotingOption, DiscussionItem


class VotingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingOption
        fields = ["name", "description"]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "title", "description", "status", "owner", "sessions", "created", "source",
                  "voting_enabled", "voting_model", "quorum_model", "options", "discussion_count"]
        read_only_fields = ["sessions", "created", "options"]

    options = VotingOptionSerializer(many=True, read_only=True)
    discussion_count = serializers.SerializerMethodField()

    def get_discussion_count(self, obj):
        return obj.discussion.all().count()


class DiscussionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussionItem
        fields = ["id", "timestamp", "topic", "user", "comment", "documents", "vote", "source", "external_id",
                  "parent_item", "path", "reply_count"]

    reply_count = serializers.SerializerMethodField()

    def get_reply_count(self, obj):
        return obj.replies.all().filter(topic_path__startswith=obj.path).count()
