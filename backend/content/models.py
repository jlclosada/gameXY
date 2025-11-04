from django.db import models
from django.conf import settings

class News(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500)
    featured_image = models.ImageField(upload_to='news/', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news')
    game = models.ForeignKey('games.Game', on_delete=models.SET_NULL, null=True, blank=True, related_name='news')
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-created_at']

class Post(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='posts')
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Guide(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    description = models.TextField(max_length=500)
    thumbnail = models.ImageField(upload_to='guides/', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guides')
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='guides')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    video_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True, help_text='Las guías se publican automáticamente')
    views_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_guides', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class GuideRating(models.Model):
    RATING_CHOICES = [
        (1, '1 estrella'),
        (2, '2 estrellas'),
        (3, '3 estrellas'),
        (4, '4 estrellas'),
        (5, '5 estrellas'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guide_ratings')
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'guide')
    
    def __str__(self):
        return f"{self.user.username} - {self.guide.title}: {self.rating}"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    
    # Generic relations to News, Post, Guide, or Game
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    
    # Threading and voting
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_comments', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    
    @property
    def score(self):
        return self.likes.count() - self.dislikes.count()

    class Meta:
        ordering = ['-created_at']
