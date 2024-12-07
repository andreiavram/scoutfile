from django.urls import path

from voting.views import TopicListView, TopicDetailView, TopicCreateView

urlpatterns = [
    path('topics/my/', TopicListView.as_view(), name='topic_list'),
    path('topics/<int:pk>', TopicDetailView.as_view(), name='topic_detail'),
    path('topics/create/', TopicCreateView.as_view(), name='topic_create'),
]

