from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Achievement, UserAchievement, Notification

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'created_at']
    list_filter = BaseUserAdmin.list_filter + ('role',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'avatar', 'role', 'favorite_games', 'following_categories')}),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'points', 'requirement_value', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering = ['category', '-points']
    

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'progress', 'is_complete', 'unlocked_at', 'notified']
    list_filter = ['achievement__category', 'notified', 'unlocked_at']
    search_fields = ['user__username', 'achievement__name']
    readonly_fields = ['unlocked_at']
    ordering = ['-unlocked_at']
    
    def is_complete(self, obj):
        return obj.progress >= obj.achievement.requirement_value
    is_complete.boolean = True
    is_complete.short_description = 'Completado'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']
    ordering = ['-created_at']
