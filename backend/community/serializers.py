from rest_framework import serializers
from .models import Group, GroupMembership, Forum, Topic, Post, GroupPost, GroupPostComment, GroupJoinRequest, GroupInvitation
from users.serializers import UserSerializer


class GroupMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'role', 'joined_at']


class GroupJoinRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    
    class Meta:
        model = GroupJoinRequest
        fields = ['id', 'group', 'group_name', 'user', 'status', 'message', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class GroupInvitationSerializer(serializers.ModelSerializer):
    invitee = UserSerializer(read_only=True)
    inviter = UserSerializer(read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    group_slug = serializers.CharField(source='group.slug', read_only=True)
    
    class Meta:
        model = GroupInvitation
        fields = ['id', 'group', 'group_name', 'group_slug', 'invitee', 'inviter', 'status', 'message', 'created_at', 'updated_at']
        read_only_fields = ['inviter', 'created_at', 'updated_at']


class GroupSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    member_count = serializers.ReadOnlyField()
    is_member = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    has_pending_request = serializers.SerializerMethodField()
    game_name = serializers.CharField(source='game.title', read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'slug', 'description', 'icon', 'banner', 'game', 'game_name', 
                  'creator', 'member_count', 'is_member', 'user_role', 'has_pending_request', 
                  'is_public', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'creator', 'is_active', 'created_at', 'updated_at']
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(id=request.user.id).exists()
        return False
    
    def get_user_role(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = GroupMembership.objects.filter(group=obj, user=request.user).first()
            return membership.role if membership else None
        return None
    
    def get_has_pending_request(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return GroupJoinRequest.objects.filter(
                group=obj, 
                user=request.user, 
                status='pending'
            ).exists()
        return False


class ForumSerializer(serializers.ModelSerializer):
    topic_count = serializers.ReadOnlyField()
    post_count = serializers.ReadOnlyField()
    group_name = serializers.CharField(source='group.name', read_only=True)
    game_name = serializers.CharField(source='game.title', read_only=True)
    
    class Meta:
        model = Forum
        fields = ['id', 'name', 'slug', 'description', 'icon', 'category', 'group', 'group_name',
                  'game', 'game_name', 'topic_count', 'post_count', 'order', 'is_active', 'created_at']
        read_only_fields = ['slug', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'topic', 'author', 'is_solution', 'is_edited', 
                  'can_edit', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user or request.user.can_edit_content
        return False


class TopicSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    reply_count = serializers.ReadOnlyField()
    can_edit = serializers.SerializerMethodField()
    forum_name = serializers.CharField(source='forum.name', read_only=True)
    latest_post = serializers.SerializerMethodField()
    
    class Meta:
        model = Topic
        fields = ['id', 'title', 'slug', 'content', 'forum', 'forum_name', 'author', 
                  'is_pinned', 'is_locked', 'is_active', 'views', 'reply_count', 'can_edit',
                  'latest_post', 'created_at', 'updated_at', 'last_post_at']
        read_only_fields = ['slug', 'author', 'views', 'created_at', 'updated_at', 'last_post_at']
    
    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user or request.user.can_edit_content
        return False
    
    def get_latest_post(self, obj):
        latest = obj.posts.order_by('-created_at').first()
        if latest:
            return {
                'author': latest.author.username,
                'created_at': latest.created_at
            }
        return None


class TopicDetailSerializer(TopicSerializer):
    posts = PostSerializer(many=True, read_only=True)
    
    class Meta(TopicSerializer.Meta):
        fields = TopicSerializer.Meta.fields + ['posts']


class GroupPostCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = GroupPostComment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class GroupPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comment_count = serializers.ReadOnlyField()
    comments = GroupPostCommentSerializer(many=True, read_only=True)
    can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = GroupPost
        fields = ['id', 'group', 'author', 'content', 'post_type', 'image', 'video_url',
                  'link_url', 'link_title', 'is_pinned', 'comment_count', 'comments',
                  'can_edit', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user or request.user.can_edit_content
        return False
