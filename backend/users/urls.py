from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomTokenObtainPairView
from .achievement_views import AchievementViewSet, UserAchievementViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'user-achievements', UserAchievementViewSet, basename='user-achievement')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]
