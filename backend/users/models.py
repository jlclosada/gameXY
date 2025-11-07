from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('goat', 'GOAT'),
        ('admin', 'Administrador'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Masculino'),
        ('female', 'Femenino'),
        ('other', 'Otro'),
        ('prefer_not_to_say', 'Prefiero no decir'),
    ]
    
    # Override username para permitir null inicialmente
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    
    # Email es el campo principal para autenticación
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username se pedirá en el perfil, no en registro
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    favorite_games = models.ManyToManyField('games.Game', related_name='favorited_by', blank=True)
    favorite_genres = models.JSONField(default=list, blank=True, help_text='Lista de géneros favoritos del usuario')
    following_categories = models.ManyToManyField('games.Category', related_name='followers', blank=True)
    saved_guides = models.ManyToManyField('content.Guide', related_name='saved_by', blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_completed = models.BooleanField(default=False, help_text='Indica si el usuario completó su perfil inicial')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
    @property
    def is_goat(self):
        return self.role == 'goat'
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def can_edit_content(self):
        """GOAT y Admin pueden editar contenido"""
        return self.role in ['goat', 'admin']

    class Meta:
        ordering = ['-created_at']


class Achievement(models.Model):
    """Definición de logros disponibles"""
    CATEGORY_CHOICES = [
        ('content', 'Creación de Contenido'),
        ('social', 'Social'),
        ('engagement', 'Participación'),
        ('time', 'Antigüedad'),
        ('special', 'Especial'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='content')
    points = models.IntegerField(default=10)
    requirement_value = models.IntegerField(help_text='Valor requerido para desbloquear')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.icon} {self.name}"
    
    class Meta:
        ordering = ['category', '-points']


class UserAchievement(models.Model):
    """Logros desbloqueados por usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlocked_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    notified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'achievement')
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class Notification(models.Model):
    """Sistema de notificaciones para usuarios"""
    
    TYPE_CHOICES = [
        ('comment_reply', 'Respuesta a comentario'),
        ('guide_like', 'Me gusta en guía'),
        ('guide_rating', 'Valoración en guía'),
        ('achievement', 'Logro desbloqueado'),
        ('new_guide_favorite_game', 'Nueva guía de juego favorito'),
        ('new_follower', 'Nuevo seguidor'),
        ('system', 'Notificación del sistema'),
        ('post_reply', 'Respuesta en foro'),
        ('group_post_comment', 'Comentario en grupo'),
        ('join_request', 'Solicitud para unirse al grupo'),
        ('join_approved', 'Solicitud aprobada'),
        ('join_rejected', 'Solicitud rechazada'),
        ('group_post', 'Nueva publicación en grupo'),
        ('group_invitation', 'Invitación a grupo'),
        ('invitation_accepted', 'Invitación aceptada'),
        ('invitation_rejected', 'Invitación rechazada'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Para enlazar a cualquier objeto (guía, comentario, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    action_url = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.notification_type} para {self.recipient.username}"
    
    def mark_as_read(self):
        """Marcar notificación como leída"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
