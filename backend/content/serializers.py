from rest_framework import serializers
from .models import News, Post, Guide, Comment
from users.serializers import UserPublicSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)
    score = serializers.ReadOnlyField()
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'news', 'post', 'guide', 'game',
                  'parent', 'replies', 'likes_count', 'dislikes_count', 
                  'score', 'user_vote', 'created_at', 'updated_at']
        read_only_fields = ['user', 'likes', 'dislikes']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []
    
    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if obj.likes.filter(id=request.user.id).exists():
                return 'like'
            elif obj.dislikes.filter(id=request.user.id).exists():
                return 'dislike'
        return None

class NewsListSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    game_title = serializers.CharField(source='game.title', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'excerpt', 'featured_image', 
                  'author', 'game_title', 'comments_count', 'views_count', 'created_at']

class NewsDetailSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['author', 'views_count']

class PostListSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    game_title = serializers.CharField(source='game.title', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'game_title', 
                  'likes_count', 'comments_count', 'views_count', 'created_at']

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'views_count', 'likes']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class GuideListSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    game_title = serializers.CharField(source='game.title', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_saved = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Guide
        fields = ['id', 'title', 'slug', 'description', 'thumbnail', 'author', 
                  'game_title', 'difficulty', 'likes_count', 'views_count', 'created_at', 'is_saved',
                  'average_rating', 'ratings_count']
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saved_by.filter(id=request.user.id).exists()
        return False
    
    def get_average_rating(self, obj):
        from django.db.models import Avg
        result = obj.ratings.aggregate(Avg('rating'))
        return round(result['rating__avg'], 1) if result['rating__avg'] else None
    
    def get_ratings_count(self, obj):
        return obj.ratings.count()

class GuideDetailSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Guide
        fields = '__all__'
        read_only_fields = ['author', 'views_count', 'likes']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saved_by.filter(id=request.user.id).exists()
        return False
    
    def get_average_rating(self, obj):
        from django.db.models import Avg
        result = obj.ratings.aggregate(Avg('rating'))
        return round(result['rating__avg'], 1) if result['rating__avg'] else None
    
    def get_ratings_count(self, obj):
        return obj.ratings.count()
    
    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = obj.ratings.filter(user=request.user).first()
            return rating.rating if rating else None
        return None
