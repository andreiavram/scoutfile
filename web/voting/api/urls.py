from rest_framework_nested import routers

from voting.api.viewsets import TopicViewSet, DiscussionItemViewSet

app_name = 'voting'

router = routers.SimpleRouter()
router.register(r'topics', viewset=TopicViewSet, basename="topic")
router.register(r'discussions', viewset=DiscussionItemViewSet, basename="discussion")

topic_router = routers.NestedSimpleRouter(router, r'topics', lookup='topic')
topic_router.register(r'discussions', DiscussionItemViewSet, basename='topic-discussion')

urlpatterns = []
urlpatterns += router.urls
urlpatterns += topic_router.urls
