from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import F, Sum, Count, Q
from .models import Achievement, UserAchievement
from .achievement_serializers import (
    AchievementSerializer, 
    UserAchievementSerializer,
    UserAchievementStatsSerializer
)
from .achievement_service import AchievementService


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar todos los logros disponibles.
    Solo lectura - los logros se gestionan desde el admin.
    """
    queryset = Achievement.objects.filter(is_active=True)
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('category', '-points')
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Retorna las categorías disponibles de logros"""
        return Response(dict(Achievement.CATEGORY_CHOICES))


class UserAchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para los logros de un usuario.
    """
    serializer_class = UserAchievementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna solo los logros del usuario autenticado"""
        return UserAchievement.objects.filter(
            user=self.request.user
        ).select_related('achievement').order_by('-unlocked_at')
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Retorna estadísticas completas de logros del usuario.
        GET /api/user-achievements/stats/
        """
        user = request.user
        all_achievements = Achievement.objects.filter(is_active=True)
        user_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')
        
        total_achievements = all_achievements.count()
        
        # Contar logros desbloqueados (progreso >= requirement_value)
        unlocked_achievements = user_achievements.filter(
            progress__gte=F('achievement__requirement_value')
        )
        unlocked_count = unlocked_achievements.count()
        
        # Calcular puntos totales
        total_points = unlocked_achievements.aggregate(
            points=Sum('achievement__points')
        )['points'] or 0
        
        # Porcentaje de completitud
        completion = (unlocked_count / total_achievements * 100) if total_achievements > 0 else 0
        
        # Logros por categoría
        achievements_by_category = {}
        for category_code, category_name in Achievement.CATEGORY_CHOICES:
            category_total = all_achievements.filter(category=category_code).count()
            category_unlocked = unlocked_achievements.filter(
                achievement__category=category_code
            ).count()
            achievements_by_category[category_name] = {
                'total': category_total,
                'unlocked': category_unlocked,
                'percentage': round((category_unlocked / category_total * 100) if category_total > 0 else 0, 1)
            }
        
        # Logros recientes (últimos 5 desbloqueados)
        recent_unlocks = unlocked_achievements.order_by('-unlocked_at')[:5]
        
        stats_data = {
            'total_achievements': total_achievements,
            'unlocked_achievements': unlocked_count,
            'total_points': total_points,
            'completion_percentage': round(completion, 1),
            'achievements_by_category': achievements_by_category,
            'recent_unlocks': UserAchievementSerializer(recent_unlocks, many=True).data
        }
        
        serializer = UserAchievementStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def progress(self, request):
        """
        Retorna el progreso del usuario en todos los logros (desbloqueados y bloqueados).
        GET /api/user-achievements/progress/
        """
        user = request.user
        all_achievements = Achievement.objects.filter(is_active=True).order_by('category', '-points')
        user_achievements_dict = {
            ua.achievement_id: ua 
            for ua in UserAchievement.objects.filter(user=user).select_related('achievement')
        }
        
        achievements_with_progress = []
        for achievement in all_achievements:
            user_achievement = user_achievements_dict.get(achievement.id)
            
            achievement_data = AchievementSerializer(achievement).data
            if user_achievement:
                achievement_data.update({
                    'progress': user_achievement.progress,
                    'progress_percentage': min(
                        round((user_achievement.progress / achievement.requirement_value * 100), 1),
                        100
                    ) if achievement.requirement_value > 0 else 100,
                    'is_unlocked': user_achievement.progress >= achievement.requirement_value,
                    'unlocked_at': user_achievement.unlocked_at
                })
            else:
                achievement_data.update({
                    'progress': 0,
                    'progress_percentage': 0,
                    'is_unlocked': False,
                    'unlocked_at': None
                })
            
            achievements_with_progress.append(achievement_data)
        
        return Response(achievements_with_progress)
    
    @action(detail=False, methods=['post'])
    def check(self, request):
        """
        Verifica y actualiza todos los logros del usuario.
        POST /api/user-achievements/check/
        """
        newly_unlocked = AchievementService.check_all_achievements(request.user)
        
        if newly_unlocked:
            serializer = UserAchievementSerializer(newly_unlocked, many=True)
            return Response({
                'message': f'{len(newly_unlocked)} nuevo(s) logro(s) desbloqueado(s)',
                'achievements': serializer.data
            })
        else:
            return Response({
                'message': 'No hay nuevos logros desbloqueados',
                'achievements': []
            })
