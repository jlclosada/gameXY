from rest_framework import serializers
from .models import Achievement, UserAchievement

class AchievementSerializer(serializers.ModelSerializer):
    """Serializer para definiciones de logros"""
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'code', 'name', 'description', 'icon', 'category',
            'points', 'requirement_value', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer para logros desbloqueados por usuarios"""
    achievement = AchievementSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()
    
    class Meta:
        model = UserAchievement
        fields = [
            'id', 'achievement', 'unlocked_at', 'progress', 
            'progress_percentage', 'is_unlocked', 'notified'
        ]
        read_only_fields = ['id', 'unlocked_at']
    
    def get_progress_percentage(self, obj):
        """Calcula el porcentaje de progreso hacia el logro"""
        if obj.achievement.requirement_value == 0:
            return 100
        percentage = (obj.progress / obj.achievement.requirement_value) * 100
        return min(round(percentage, 1), 100)
    
    def get_is_unlocked(self, obj):
        """Indica si el logro está completamente desbloqueado"""
        return obj.progress >= obj.achievement.requirement_value


class UserAchievementStatsSerializer(serializers.Serializer):
    """Estadísticas de logros de un usuario"""
    total_achievements = serializers.IntegerField()
    unlocked_achievements = serializers.IntegerField()
    total_points = serializers.IntegerField()
    completion_percentage = serializers.FloatField()
    achievements_by_category = serializers.DictField()
    recent_unlocks = UserAchievementSerializer(many=True)
