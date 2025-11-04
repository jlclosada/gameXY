from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsGoatOrReadOnly
from .models import News, Post, Guide, Comment
from .serializers import (NewsListSerializer, NewsDetailSerializer,
                          PostListSerializer, PostDetailSerializer,
                          GuideListSerializer, GuideDetailSerializer,
                          CommentSerializer)

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_published=True)
    lookup_field = 'slug'
    permission_classes = [IsGoatOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['game', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'views_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        return NewsDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['game', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'status': 'unliked'})
        else:
            post.likes.add(request.user)
            return Response({'status': 'liked'})

class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.filter(is_published=True)
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['game', 'author', 'difficulty']
    search_fields = ['title', 'content', 'description']
    ordering_fields = ['created_at', 'views_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GuideListSerializer
        return GuideDetailSerializer
    
    def perform_create(self, serializer):
        guide = serializer.save(author=self.request.user)
        
        # Notificar a usuarios que tienen el juego como favorito
        from users.notifications import NotificationService
        NotificationService.notify_new_guide_favorite_game(guide)
    
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if self.action in ['update', 'partial_update', 'destroy']:
            # Solo el autor o usuarios con can_edit_content pueden editar/eliminar
            if obj.author != request.user and not request.user.can_edit_content:
                self.permission_denied(request, message='No tienes permiso para modificar esta guía.')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        guide = self.get_object()
        if request.user in guide.likes.all():
            guide.likes.remove(request.user)
            return Response({'status': 'unliked', 'likes_count': guide.likes.count()})
        else:
            guide.likes.add(request.user)
            
            # Enviar notificación al autor
            from users.notifications import NotificationService
            NotificationService.notify_guide_like(guide, request.user)
            
            return Response({'status': 'liked', 'likes_count': guide.likes.count()})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def save_guide(self, request, slug=None):
        """Guardar o quitar guía de la lista de guardados del usuario"""
        guide = self.get_object()
        user = request.user
        
        if guide in user.saved_guides.all():
            user.saved_guides.remove(guide)
            return Response({
                'status': 'unsaved',
                'is_saved': False,
                'message': 'Guía eliminada de guardados'
            })
        else:
            user.saved_guides.add(guide)
            return Response({
                'status': 'saved',
                'is_saved': True,
                'message': 'Guía guardada correctamente'
            })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def saved(self, request):
        """Obtener todas las guías guardadas por el usuario"""
        user = request.user
        saved_guides = user.saved_guides.filter(is_published=True).order_by('-created_at')
        serializer = GuideListSerializer(saved_guides, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate(self, request, slug=None):
        """Valorar una guía con estrellas (1-5)"""
        from .models import GuideRating
        
        guide = self.get_object()
        user = request.user
        rating_value = request.data.get('rating')
        
        if not rating_value or not (1 <= int(rating_value) <= 5):
            return Response(
                {'error': 'La valoración debe ser un número entre 1 y 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear o actualizar rating
        rating, created = GuideRating.objects.update_or_create(
            user=user,
            guide=guide,
            defaults={'rating': rating_value}
        )
        
        # Enviar notificación al autor (solo si es nuevo)
        if created:
            from users.notifications import NotificationService
            NotificationService.notify_guide_rating(guide, user, int(rating_value))
        
        # Calcular nuevo promedio
        from django.db.models import Avg
        result = guide.ratings.aggregate(Avg('rating'))
        avg_rating = round(result['rating__avg'], 1) if result['rating__avg'] else None
        
        return Response({
            'status': 'created' if created else 'updated',
            'rating': rating.rating,
            'average_rating': avg_rating,
            'ratings_count': guide.ratings.count()
        })

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['news', 'post', 'guide', 'game', 'parent']
    
    def get_queryset(self):
        # Excluir respuestas anidadas del queryset principal
        queryset = super().get_queryset()
        if not self.request.query_params.get('parent'):
            queryset = queryset.filter(parent=None)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            # Solo el autor o GOAT pueden editar/eliminar
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if self.action in ['update', 'partial_update', 'destroy']:
            if obj.user != request.user and not request.user.can_edit_content:
                self.permission_denied(request, message='No tienes permiso para modificar este comentario.')
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        comment = self.get_object()
        vote_type = request.data.get('vote_type')  # 'like', 'dislike', or 'remove'
        
        # Remover votos previos
        comment.likes.remove(request.user)
        comment.dislikes.remove(request.user)
        
        # Aplicar nuevo voto
        if vote_type == 'like':
            comment.likes.add(request.user)
            return Response({'status': 'liked', 'score': comment.score})
        elif vote_type == 'dislike':
            comment.dislikes.add(request.user)
            return Response({'status': 'disliked', 'score': comment.score})
        
        return Response({'status': 'removed', 'score': comment.score})
