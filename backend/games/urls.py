from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GameViewSet, GameRatingViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'', GameViewSet, basename='game')
router.register(r'ratings', GameRatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
