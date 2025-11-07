from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GroupViewSet, ForumViewSet, TopicViewSet, PostViewSet,
    GroupPostViewSet, GroupPostCommentViewSet, community_stats
)

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'forums', ForumViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'posts', PostViewSet)
router.register(r'group-posts', GroupPostViewSet)
router.register(r'group-post-comments', GroupPostCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', community_stats, name='community-stats'),
]
