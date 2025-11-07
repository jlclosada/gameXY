from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Group(models.Model):
    """Gaming groups/clans"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='community/groups/', null=True, blank=True)
    banner = models.ImageField(upload_to='community/groups/banners/', null=True, blank=True)
    game = models.ForeignKey('games.Game', on_delete=models.SET_NULL, null=True, blank=True, related_name='groups')
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GroupMembership', related_name='joined_groups')
    
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def member_count(self):
        return self.members.count()


class GroupMembership(models.Model):
    """Membership with roles"""
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('group', 'user')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.role})"


class GroupJoinRequest(models.Model):
    """Join requests for private groups"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_join_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text='Optional message from user')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('group', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} -> {self.group.name} ({self.status})"


class GroupInvitation(models.Model):
    """Invitations sent by group creators to users"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='invitations')
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_invitations')
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_group_invitations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text='Optional message from inviter')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('group', 'invitee')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.inviter.username} invited {self.invitee.username} to {self.group.name} ({self.status})"


class Forum(models.Model):
    """Discussion forums"""
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('games', 'Games'),
        ('news', 'News & Updates'),
        ('guides', 'Guides & Tips'),
        ('support', 'Support'),
        ('off_topic', 'Off Topic'),
    ]
    
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='💬')  # Emoji icon
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='forums')
    game = models.ForeignKey('games.Game', on_delete=models.SET_NULL, null=True, blank=True, related_name='forums')
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def topic_count(self):
        return self.topics.count()
    
    @property
    def post_count(self):
        return sum(topic.posts.count() for topic in self.topics.all())


class Topic(models.Model):
    """Discussion topics within forums"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = models.TextField()
    
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topics')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_topics')
    
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    views = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_post_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_pinned', '-last_post_at']
        unique_together = ('forum', 'slug')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def reply_count(self):
        return self.posts.count()


class Post(models.Model):
    """Replies to topics"""
    content = models.TextField()
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_posts')
    
    is_solution = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Post by {self.author.username} on {self.topic.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update topic's last_post_at
        self.topic.last_post_at = self.created_at
        self.topic.save()


class GroupPost(models.Model):
    """Posts within groups"""
    POST_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Link'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_posts')
    
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='text')
    
    # Optional media
    image = models.ImageField(upload_to='community/posts/', null=True, blank=True)
    video_url = models.URLField(max_length=500, null=True, blank=True)
    link_url = models.URLField(max_length=500, null=True, blank=True)
    link_title = models.CharField(max_length=200, null=True, blank=True)
    
    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return f"Post by {self.author.username} in {self.group.name}"
    
    @property
    def comment_count(self):
        return self.comments.count()


class GroupPostComment(models.Model):
    """Comments on group posts"""
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_post_comments')
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on post {self.post.id}"
