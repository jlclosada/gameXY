from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from users.permissions import IsGoatOrReadOnly
from .models import Category, Game, GameRating
from .serializers import (CategorySerializer, GameListSerializer, 
                          GameDetailSerializer, GameRatingSerializer)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsGoatOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories__slug', 'is_featured', 'genre', 'multiplayer']
    search_fields = ['title', 'description', 'developer', 'publisher']
    ordering_fields = ['created_at', 'rating', 'release_date', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GameListSerializer
        return GameDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def ratings(self, request, slug=None):
        game = self.get_object()
        ratings = game.ratings.all()
        serializer = GameRatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def set_official_rating(self, request, slug=None):
        """Solo GOAT/Admin pueden establecer la valoración oficial"""
        if not request.user.can_edit_content:
            return Response(
                {'error': 'Solo los usuarios GOAT pueden establecer la valoración oficial'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        game = self.get_object()
        rating_value = request.data.get('rating')
        review = request.data.get('review', '')
        
        if rating_value is None or not (0 <= float(rating_value) <= 10):
            return Response(
                {'error': 'La valoración oficial debe estar entre 0 y 10'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        game.official_rating = round(float(rating_value), 1)
        game.official_review = review
        game.save()
        
        return Response({
            'official_rating': float(game.official_rating),
            'official_review': game.official_review
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request, slug=None):
        """Marcar/desmarcar juego como favorito"""
        game = self.get_object()
        user = request.user
        
        if game in user.favorite_games.all():
            user.favorite_games.remove(game)
            return Response({
                'status': 'removed',
                'is_favorite': False
            })
        else:
            user.favorite_games.add(game)
            return Response({
                'status': 'added',
                'is_favorite': True
            })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate(self, request, slug=None):
        game = self.get_object()
        rating_value = request.data.get('rating')
        
        if not rating_value or not (1 <= int(rating_value) <= 5):
            return Response(
                {'error': 'La valoración debe estar entre 1 y 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear o actualizar la valoración del usuario
        game_rating, created = GameRating.objects.update_or_create(
            game=game,
            user=request.user,
            defaults={'rating': int(rating_value)}
        )
        
        # Recalcular community rating (promedio de usuarios)
        avg_rating = game.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        game.community_rating = round(avg_rating, 1)
        game.rating = round(avg_rating, 1)  # Legacy compatibility
        game.save()
        
        return Response({
            'rating': game_rating.rating,
            'community_rating': float(game.community_rating),
            'official_rating': float(game.official_rating) if game.official_rating else None,
            'total_ratings': game.ratings.count()
        })

class GameRatingViewSet(viewsets.ModelViewSet):
    queryset = GameRating.objects.all()
    serializer_class = GameRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game', 'user']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
