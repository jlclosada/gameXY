from django.db import models
from django.conf import settings

class Genre(models.Model):
    """Géneros de videojuegos"""
    name = models.CharField(max_length=100, unique=True, help_text='Nombre del género')
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='🎮', help_text='Emoji o icono para el género')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text='Orden de visualización')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Game(models.Model):
    GENRE_CHOICES = [
        ('action', 'Acción'),
        ('adventure', 'Aventura'),
        ('rpg', 'RPG'),
        ('strategy', 'Estrategia'),
        ('shooter', 'Shooter'),
        ('sports', 'Deportes'),
        ('racing', 'Carreras'),
        ('fighting', 'Pelea'),
        ('puzzle', 'Puzzle'),
        ('simulation', 'Simulación'),
        ('horror', 'Terror'),
        ('platform', 'Plataformas'),
        ('mmorpg', 'MMORPG'),
        ('moba', 'MOBA'),
        ('battle_royale', 'Battle Royale'),
    ]
    
    STYLE_CHOICES = [
        ('2d', '2D'),
        ('3d', '3D'),
        ('pixel_art', 'Pixel Art'),
        ('realistic', 'Realista'),
        ('cartoon', 'Cartoon'),
        ('anime', 'Anime'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='games/covers/', null=True, blank=True, help_text='Imagen para la tarjeta del juego')
    banner_image = models.ImageField(upload_to='games/banners/', null=True, blank=True, help_text='Imagen wallpaper del juego')
    release_date = models.DateField(null=True, blank=True)
    developer = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True)
    style = models.CharField(max_length=50, choices=STYLE_CHOICES, blank=True)
    platforms = models.JSONField(default=list, blank=True, help_text='Lista de plataformas: PC, PlayStation, Xbox, Switch, Mobile')
    categories = models.ManyToManyField(Category, related_name='games', blank=True)
    # Valoración oficial de la plataforma (solo GOAT/Admin)
    official_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, help_text='Valoración oficial GOAT (0-10)')
    official_review = models.TextField(blank=True, help_text='Reseña oficial del equipo')
    # Valoración de comunidad (calculada automáticamente - promedio)
    community_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, help_text='Rating promedio de la comunidad (1-5)')
    # Rating legacy (mantener compatibilidad)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, help_text='Rating promedio de 0-5')
    min_players = models.IntegerField(null=True, blank=True)
    max_players = models.IntegerField(null=True, blank=True)
    multiplayer = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    trailer_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    steam_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_games')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class GameRating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.rating}/5)"

    class Meta:
        unique_together = ['game', 'user']
        ordering = ['-created_at']
