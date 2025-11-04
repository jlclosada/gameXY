from django.contrib import admin
from .models import News, Post, Guide, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'game', 'is_published', 'views_count', 'created_at']
    list_filter = ['is_published', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'game', 'is_published', 'views_count', 'created_at']
    list_filter = ['is_published', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'game', 'difficulty', 'is_published', 'views_count', 'created_at']
    list_filter = ['is_published', 'difficulty', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content', 'description']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username']
    
    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = 'Content'