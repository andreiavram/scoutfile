from django.contrib import admin

from voting.models import VotingOption, Topic, DiscussionItem


class VotingOptionsInline(admin.TabularInline):
    model = VotingOption


class DiscussionItemInline(admin.TabularInline):
    model = DiscussionItem


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_filter = ["source", ]
    list_display = ["title", "status", "owner", "created", "source", "voting_enabled", "voting_model", "quorum_model"]
    inlines = [VotingOptionsInline, ]


@admin.register(DiscussionItem)
class DiscussionItemAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "topic", "user", "comment", "vote", "source", "parent_item"]
    autocomplete_fields = ['documents']

