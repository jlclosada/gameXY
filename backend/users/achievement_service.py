from django.utils import timezone
from datetime import timedelta
from .models import Achievement, UserAchievement


class AchievementService:
    """Servicio para verificar y desbloquear logros de usuarios"""
    
    @staticmethod
    def check_and_unlock(user, achievement_code, current_progress=None):
        """Verificar y desbloquear un logro específico"""
        try:
            achievement = Achievement.objects.get(code=achievement_code, is_active=True)
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement,
                defaults={'progress': current_progress or 0}
            )
            
            # Actualizar progreso si se proporciona
            if not created and current_progress is not None:
                old_progress = user_achievement.progress
                user_achievement.progress = current_progress
                user_achievement.save()
                
                # Si se acaba de completar
                if old_progress < achievement.requirement_value and current_progress >= achievement.requirement_value:
                    from .notifications import NotificationService
                    NotificationService.notify_achievement_unlocked(user, achievement)
                    return user_achievement
            elif created and (current_progress or 0) >= achievement.requirement_value:
                # Enviar notificación si es nuevo y ya está completado
                from .notifications import NotificationService
                NotificationService.notify_achievement_unlocked(user, achievement)
            
            return user_achievement if created else None
        except Achievement.DoesNotExist:
            return None
    
    @staticmethod
    def check_all_achievements(user):
        """Verificar todos los logros posibles para un usuario"""
        newly_unlocked = []
        
        # Contar estadísticas del usuario
        guides_count = user.guides.filter(is_published=True).count()
        comments_count = user.comments.count()
        favorites_count = user.favorite_games.count()
        saved_guides_count = user.saved_guides.count()
        days_member = (timezone.now() - user.created_at).days
        
        # Primera Guía
        achievement = AchievementService.check_and_unlock(user, 'first_guide', guides_count)
        if achievement:
            newly_unlocked.append(achievement)
        
        # Maestro de Guías
        achievement = AchievementService.check_and_unlock(user, 'guide_master', guides_count)
        if achievement:
            newly_unlocked.append(achievement)
        
        # Leyenda de Guías
        achievement = AchievementService.check_and_unlock(user, 'guide_legend', guides_count)
        if achievement:
            newly_unlocked.append(achievement)
        
        # Primera Opinión
        achievement = AchievementService.check_and_unlock(user, 'first_comment', comments_count)
        if achievement:
            newly_unlocked.append(achievement)
        
        # Mariposa Social
        achievement = AchievementService.check_and_unlock(user, 'social_butterfly', comments_count)
        if achievement:
            newly_unlocked.append(achievement)
        
        # Primer Favorito
        achievement = AchievementService.check_and_unlock(user, 'first_favorite', favorites_count)
        if achievement:
            newly_unlocked.append(achievement)
        
        # Coleccionista
        achievement = AchievementService.check_and_unlock(user, 'game_collector', favorites_count)
        if achievement:
            newly_unlocked.append(achievement)
        
        # Curador
        if saved_guides_count >= 10:
            achievement = AchievementService.check_and_unlock(user, 'guide_saver')
            if achievement:
                newly_unlocked.append(achievement)
        
        # Guía Popular (una guía con 50+ likes)
        popular_guide = user.guides.filter(likes__gte=50).first()
        if popular_guide:
            achievement = AchievementService.check_and_unlock(user, 'popular_guide')
            if achievement:
                newly_unlocked.append(achievement)
        
        # Guía Viral (una guía con 1000+ vistas)
        viral_guide = user.guides.filter(views_count__gte=1000).first()
        if viral_guide:
            achievement = AchievementService.check_and_unlock(user, 'viral_guide')
            if achievement:
                newly_unlocked.append(achievement)
        
        # Veterano (30 días)
        if days_member >= 30:
            achievement = AchievementService.check_and_unlock(user, 'veteran_30')
            if achievement:
                newly_unlocked.append(achievement)
        
        # Veterano de Oro (365 días)
        if days_member >= 365:
            achievement = AchievementService.check_and_unlock(user, 'veteran_365')
            if achievement:
                newly_unlocked.append(achievement)
        
        # Adoptante Temprano (primeros 100 usuarios)
        total_users = user.__class__.objects.count()
        user_position = user.__class__.objects.filter(created_at__lt=user.created_at).count() + 1
        if user_position <= 100:
            achievement = AchievementService.check_and_unlock(user, 'early_adopter')
            if achievement:
                newly_unlocked.append(achievement)
        
        # Útil (promedio de rating 4.5+)
        from django.db.models import Avg
        from content.models import GuideRating
        
        if guides_count > 0:
            avg_rating = GuideRating.objects.filter(
                guide__author=user
            ).aggregate(Avg('rating'))['rating__avg']
            
            if avg_rating and avg_rating >= 4.5:
                achievement = AchievementService.check_and_unlock(user, 'helpful')
                if achievement:
                    newly_unlocked.append(achievement)
        
        return newly_unlocked
    
    @staticmethod
    def get_user_progress(user):
        """Obtener el progreso del usuario en todos los logros"""
        all_achievements = Achievement.objects.filter(is_active=True)
        unlocked = user.unlocked_achievements.values_list('achievement_id', flat=True)
        
        progress = {
            'total_achievements': all_achievements.count(),
            'unlocked_count': len(unlocked),
            'total_points': sum(
                ach.achievement.points 
                for ach in user.unlocked_achievements.all()
            ),
            'achievements': []
        }
        
        for achievement in all_achievements:
            is_unlocked = achievement.id in unlocked
            user_ach = None
            
            if is_unlocked:
                user_ach = user.unlocked_achievements.get(achievement=achievement)
            
            progress['achievements'].append({
                'id': achievement.id,
                'code': achievement.code,
                'name': achievement.name,
                'description': achievement.description,
                'icon': achievement.icon,
                'category': achievement.category,
                'points': achievement.points,
                'unlocked': is_unlocked,
                'unlocked_at': user_ach.unlocked_at if user_ach else None
            })
        
        return progress
