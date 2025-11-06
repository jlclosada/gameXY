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
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 
                  'birth_date', 'gender', 'bio', 'avatar', 'role', 'is_goat', 'is_admin', 
                  'can_edit_content', 'favorite_games', 'favorite_genres', 'following_categories', 
                  'country', 'city', 'profile_completed', 'created_at', 'comments_count', 
                  'guides_count', 'favorites_count', 'age']
        read_only_fields = ['created_at', 'role']
        extra_kwargs = {
            'username': {'required': False, 'allow_null': True, 'allow_blank': True}
        }
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_guides_count(self, obj):
        return obj.guides.count()
    
    def get_favorites_count(self, obj):
        return obj.favorite_games.count()
    
    def get_age(self, obj):
        if obj.birth_date:
            from datetime import date
            today = date.today()
            return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
        return None
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        # Si no hay username, generar uno temporal basado en email
        if not validated_data.get('username'):
            email = validated_data.get('email')
            base_username = email.split('@')[0]
            # Generar username único
            import uuid
            validated_data['username'] = f"{base_username}_{uuid.uuid4().hex[:6]}"
        
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
    username_field = 'email'  # Usar email para el login
    
    def validate(self, attrs):
        # Permitir login con email
        email = attrs.get('email') or attrs.get(self.username_field)
        if email:
            attrs[self.username_field] = email
        
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
