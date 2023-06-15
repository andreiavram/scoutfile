from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from voting.api.serializers import TopicSerializer, DiscussionItemSerializer
from voting.filters import DiscussionItemFilter
from voting.models import Topic, DiscussionItem


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class DiscussionItemViewSet(viewsets.ModelViewSet):
    serializer_class = DiscussionItemSerializer
    queryset = DiscussionItem.objects.all()
    filterset_class = DiscussionItemFilter

    def get_queryset(self):
        return self.queryset.filter(topic=self.kwargs['topic_pk'])

