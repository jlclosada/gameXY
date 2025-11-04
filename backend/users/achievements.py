from django.db import models
from django.conf import settings


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'achievement')
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


# Definición de logros predefinidos
ACHIEVEMENTS_DATA = [
    # Creación de Contenido
    {
        'code': 'first_guide',
        'name': 'Primera Guía',
        'description': 'Publica tu primera guía',
        'icon': '📖',
        'category': 'content',
        'points': 10,
        'requirement_value': 1
    },
    {
        'code': 'guide_master',
        'name': 'Maestro de Guías',
        'description': 'Publica 10 guías',
        'icon': '📚',
        'category': 'content',
        'points': 50,
        'requirement_value': 10
    },
    {
        'code': 'guide_legend',
        'name': 'Leyenda de Guías',
        'description': 'Publica 50 guías',
        'icon': '🏆',
        'category': 'content',
        'points': 200,
        'requirement_value': 50
    },
    # Engagement
    {
        'code': 'first_comment',
        'name': 'Primera Opinión',
        'description': 'Deja tu primer comentario',
        'icon': '💬',
        'category': 'engagement',
        'points': 5,
        'requirement_value': 1
    },
    {
        'code': 'social_butterfly',
        'name': 'Mariposa Social',
        'description': 'Deja 100 comentarios',
        'icon': '🦋',
        'category': 'engagement',
        'points': 50,
        'requirement_value': 100
    },
    {
        'code': 'popular_guide',
        'name': 'Guía Popular',
        'description': 'Una de tus guías recibe 50 likes',
        'icon': '⭐',
        'category': 'content',
        'points': 30,
        'requirement_value': 50
    },
    {
        'code': 'viral_guide',
        'name': 'Guía Viral',
        'description': 'Una de tus guías alcanza 1000 vistas',
        'icon': '🔥',
        'category': 'content',
        'points': 75,
        'requirement_value': 1000
    },
    # Social
    {
        'code': 'first_favorite',
        'name': 'Primer Favorito',
        'description': 'Marca tu primer juego como favorito',
        'icon': '❤️',
        'category': 'social',
        'points': 5,
        'requirement_value': 1
    },
    {
        'code': 'game_collector',
        'name': 'Coleccionista',
        'description': 'Marca 20 juegos como favoritos',
        'icon': '🎮',
        'category': 'social',
        'points': 25,
        'requirement_value': 20
    },
    # Antigüedad
    {
        'code': 'veteran_30',
        'name': 'Veterano',
        'description': 'Miembro por 30 días',
        'icon': '🎖️',
        'category': 'time',
        'points': 20,
        'requirement_value': 30
    },
    {
        'code': 'veteran_365',
        'name': 'Veterano de Oro',
        'description': 'Miembro por 1 año',
        'icon': '👑',
        'category': 'time',
        'points': 100,
        'requirement_value': 365
    },
    # Especiales
    {
        'code': 'early_adopter',
        'name': 'Adoptante Temprano',
        'description': 'Uno de los primeros 100 usuarios',
        'icon': '🌟',
        'category': 'special',
        'points': 50,
        'requirement_value': 100
    },
    {
        'code': 'helpful',
        'name': 'Útil',
        'description': 'Tus guías reciben una valoración promedio de 4.5+',
        'icon': '🌟',
        'category': 'content',
        'points': 40,
        'requirement_value': 45  # 4.5 * 10
    },
]
