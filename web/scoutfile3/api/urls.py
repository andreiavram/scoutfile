from django.urls import path, include
from rest_framework.routers import DefaultRouter

from voting.api.viewsets import TopicViewSet, DiscussionItemViewSet

app_name = 'api'


urlpatterns = [
    path('badges/', include('badge.api.urls')),
    path('voting/', include('voting.api.urls')),
]
