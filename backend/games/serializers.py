from rest_framework import serializers
from .models import Category, Game, GameRating

class CategorySerializer(serializers.ModelSerializer):
    games_count = serializers.IntegerField(source='games.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'games_count', 'created_at']

class GameListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = ['id', 'title', 'slug', 'cover_image', 'rating', 'community_rating',
                  'official_rating', 'release_date', 'categories', 'is_featured', 'is_favorite']
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(id=request.user.id).exists()
        return False

class GameDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all(), 
        write_only=True, 
        source='categories',
        required=False
    )
    ratings_count = serializers.IntegerField(source='ratings.count', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    user_rating = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    can_edit_official = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ['created_by', 'rating', 'community_rating', 'created_at', 'updated_at']
    
    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = obj.ratings.filter(user=request.user).first()
            return rating.rating if rating else 0
        return 0
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(id=request.user.id).exists()
        return False
    
    def get_can_edit_official(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.can_edit_content
        return False

class GameRatingSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    
    class Meta:
        model = GameRating
        fields = ['id', 'game', 'user', 'user_username', 'user_avatar', 
                  'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['user']
