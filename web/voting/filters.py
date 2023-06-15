from django_filters import rest_framework as filters

from voting.models import DiscussionItem, Topic


class DiscussionItemFilter(filters.FilterSet):
    topic = filters.ModelChoiceFilter(queryset=Topic.objects.all())

    class Meta:
        model = DiscussionItem
        fields = ["topic"]
