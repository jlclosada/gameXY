from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    is_goat = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    can_edit_content = serializers.ReadOnlyField()
    comments_count = serializers.SerializerMethodField()
    guides_count = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'avatar', 'role',
                  'is_goat', 'is_admin', 'can_edit_content', 'favorite_games', 
                  'following_categories', 'created_at', 'comments_count', 'guides_count', 'favorites_count']
        read_only_fields = ['created_at', 'role']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_guides_count(self, obj):
        return obj.guides.count()
    
    def get_favorites_count(self, obj):
        return obj.favorite_games.count()
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'bio', 'created_at']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
