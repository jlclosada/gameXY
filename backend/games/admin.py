from django.contrib import admin
from .models import Category, Game, GameRating, Genre

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'rating', 'release_date', 'is_featured']
    list_filter = ['is_featured', 'categories']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories']

@admin.register(GameRating)
class GameRatingAdmin(admin.ModelAdmin):
    list_display = ['game', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['name']
