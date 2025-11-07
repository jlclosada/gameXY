from django.contrib import admin
from .models import Group, GroupMembership, Forum, Topic, Post, GroupPost, GroupPostComment, GroupJoinRequest, GroupInvitation


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'member_count', 'is_public', 'is_active', 'created_at']
    list_filter = ['is_public', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['group', 'user', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['group__name', 'user__username']


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'topic_count', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'forum', 'author', 'is_pinned', 'is_locked', 'views', 'created_at']
    list_filter = ['is_pinned', 'is_locked', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic', 'author', 'is_solution', 'is_edited', 'created_at']
    list_filter = ['is_solution', 'is_edited', 'created_at']
    search_fields = ['content', 'author__username', 'topic__title']


@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'post_type', 'is_pinned', 'created_at']
    list_filter = ['post_type', 'is_pinned', 'is_active', 'created_at']
    search_fields = ['content', 'author__username', 'group__name']


@admin.register(GroupPostComment)
class GroupPostCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']


@admin.register(GroupJoinRequest)
class GroupJoinRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'group__name']


@admin.register(GroupInvitation)
class GroupInvitationAdmin(admin.ModelAdmin):
    list_display = ['inviter', 'invitee', 'group', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['inviter__username', 'invitee__username', 'group__name']
