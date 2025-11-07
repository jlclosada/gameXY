from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum
from django.contrib.auth import get_user_model
from .models import Group, GroupMembership, Forum, Topic, Post, GroupPost, GroupPostComment, GroupJoinRequest, GroupInvitation
from .serializers import (
    GroupSerializer, GroupMembershipSerializer, ForumSerializer,
    TopicSerializer, TopicDetailSerializer, PostSerializer,
    GroupPostSerializer, GroupPostCommentSerializer, GroupJoinRequestSerializer,
    GroupInvitationSerializer
)
from users.permissions import IsGoatOrReadOnly


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.filter(is_active=True)
    serializer_class = GroupSerializer
    permission_classes = [IsGoatOrReadOnly]
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by game
        game_id = self.request.query_params.get('game')
        if game_id:
            queryset = queryset.filter(game_id=game_id)
        
        # Filter by public/private
        is_public = self.request.query_params.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')
        
        # Annotate with member count for sorting
        queryset = queryset.annotate(members_count=Count('members'))
        
        return queryset
    
    def perform_create(self, serializer):
        group = serializer.save(creator=self.request.user)
        # Auto-join creator as admin
        GroupMembership.objects.create(
            group=group,
            user=self.request.user,
            role='admin'
        )
    
    def update(self, request, *args, **kwargs):
        group = self.get_object()
        # Only creator can edit
        if group.creator != request.user:
            return Response({'detail': 'Solo el creador puede editar el grupo'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        group = self.get_object()
        # Only creator can edit
        if group.creator != request.user:
            return Response({'detail': 'Solo el creador puede editar el grupo'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, slug=None):
        group = self.get_object()
        
        if group.members.filter(id=request.user.id).exists():
            return Response({'detail': 'Ya eres miembro de este grupo'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not group.is_public:
            # Create join request for private groups
            join_request, created = GroupJoinRequest.objects.get_or_create(
                group=group,
                user=request.user,
                defaults={'message': request.data.get('message', '')}
            )
            if created:
                return Response({
                    'detail': 'Solicitud enviada. El creador del grupo revisará tu solicitud.',
                    'request_id': join_request.id
                })
            else:
                if join_request.status == 'pending':
                    return Response({'detail': 'Ya tienes una solicitud pendiente'}, status=status.HTTP_400_BAD_REQUEST)
                elif join_request.status == 'rejected':
                    join_request.status = 'pending'
                    join_request.save()
                    return Response({'detail': 'Solicitud reenviada'})
        
        GroupMembership.objects.create(group=group, user=request.user, role='member')
        return Response({'detail': 'Te has unido al grupo'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave(self, request, slug=None):
        group = self.get_object()
        
        if group.creator == request.user:
            return Response({'detail': 'El creador no puede abandonar el grupo'}, status=status.HTTP_400_BAD_REQUEST)
        
        membership = GroupMembership.objects.filter(group=group, user=request.user).first()
        if not membership:
            return Response({'detail': 'No eres miembro de este grupo'}, status=status.HTTP_400_BAD_REQUEST)
        
        membership.delete()
        return Response({'detail': 'Has abandonado el grupo'})
    
    @action(detail=True, methods=['get'])
    def members(self, request, slug=None):
        group = self.get_object()
        memberships = GroupMembership.objects.filter(group=group).select_related('user')
        serializer = GroupMembershipSerializer(memberships, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_member(self, request, slug=None):
        group = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'detail': 'user_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Only creator can remove members
        if group.creator != request.user:
            return Response({'detail': 'Solo el creador puede eliminar miembros'}, status=status.HTTP_403_FORBIDDEN)
        
        # Cannot remove creator
        if int(user_id) == group.creator.id:
            return Response({'detail': 'No puedes eliminar al creador'}, status=status.HTTP_400_BAD_REQUEST)
        
        membership = GroupMembership.objects.filter(group=group, user_id=user_id).first()
        if not membership:
            return Response({'detail': 'Miembro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        membership.delete()
        return Response({'detail': 'Miembro eliminado'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def invite_user(self, request, slug=None):
        group = self.get_object()
        user_id = request.data.get('user_id')
        message = request.data.get('message', '')
        
        if not user_id:
            return Response({'detail': 'user_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Only creator can invite
        if group.creator != request.user:
            return Response({'detail': 'Solo el creador puede invitar usuarios'}, status=status.HTTP_403_FORBIDDEN)
        
        User = get_user_model()
        try:
            invitee = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user is already a member
        if group.members.filter(id=user_id).exists():
            return Response({'detail': 'El usuario ya es miembro del grupo'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if invitation already exists
        existing_invitation = GroupInvitation.objects.filter(
            group=group,
            invitee=invitee,
            status='pending'
        ).first()
        
        if existing_invitation:
            return Response({'detail': 'Ya existe una invitación pendiente para este usuario'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create invitation
        invitation = GroupInvitation.objects.create(
            group=group,
            invitee=invitee,
            inviter=request.user,
            message=message
        )
        
        serializer = GroupInvitationSerializer(invitation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def join_requests(self, request, slug=None):
        group = self.get_object()
        
        # Only creator and admins can see join requests
        if group.creator != request.user:
            membership = GroupMembership.objects.filter(
                group=group, 
                user=request.user, 
                role__in=['admin', 'moderator']
            ).first()
            if not membership:
                return Response({'detail': 'No tienes permisos'}, status=status.HTTP_403_FORBIDDEN)
        
        requests = GroupJoinRequest.objects.filter(group=group, status='pending')
        serializer = GroupJoinRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve_request(self, request, slug=None):
        group = self.get_object()
        request_id = request.data.get('request_id')
        
        if not request_id:
            return Response({'detail': 'request_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Only creator and admins can approve
        if group.creator != request.user:
            membership = GroupMembership.objects.filter(
                group=group, 
                user=request.user, 
                role__in=['admin', 'moderator']
            ).first()
            if not membership:
                return Response({'detail': 'No tienes permisos'}, status=status.HTTP_403_FORBIDDEN)
        
        join_request = GroupJoinRequest.objects.filter(id=request_id, group=group).first()
        if not join_request:
            return Response({'detail': 'Solicitud no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        # Add user to group first
        GroupMembership.objects.get_or_create(
            group=group,
            user=join_request.user,
            defaults={'role': 'member'}
        )
        
        # Update status (this will trigger notification signal)
        join_request.status = 'approved'
        join_request.save()
        
        return Response({'detail': 'Solicitud aprobada'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject_request(self, request, slug=None):
        group = self.get_object()
        request_id = request.data.get('request_id')
        
        if not request_id:
            return Response({'detail': 'request_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Only creator and admins can reject
        if group.creator != request.user:
            membership = GroupMembership.objects.filter(
                group=group, 
                user=request.user, 
                role__in=['admin', 'moderator']
            ).first()
            if not membership:
                return Response({'detail': 'No tienes permisos'}, status=status.HTTP_403_FORBIDDEN)
        
        join_request = GroupJoinRequest.objects.filter(id=request_id, group=group).first()
        if not join_request:
            return Response({'detail': 'Solicitud no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        join_request.status = 'rejected'
        join_request.save()
        
        return Response({'detail': 'Solicitud rechazada'})


class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.filter(is_active=True)
    serializer_class = ForumSerializer
    permission_classes = [IsGoatOrReadOnly]
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by group
        group_slug = self.request.query_params.get('group')
        if group_slug:
            queryset = queryset.filter(group__slug=group_slug)
        
        # Filter by game
        game_id = self.request.query_params.get('game')
        if game_id:
            queryset = queryset.filter(game_id=game_id)
        
        return queryset


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.filter(is_active=True)
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TopicDetailSerializer
        return TopicSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by forum
        forum_slug = self.request.query_params.get('forum')
        if forum_slug:
            queryset = queryset.filter(forum__slug=forum_slug)
        
        return queryset.select_related('author', 'forum')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def lock(self, request, slug=None):
        topic = self.get_object()
        
        if not request.user.can_edit_content:
            return Response({'detail': 'No tienes permisos'}, status=status.HTTP_403_FORBIDDEN)
        
        topic.is_locked = True
        topic.save()
        return Response({'detail': 'Topic bloqueado'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlock(self, request, slug=None):
        topic = self.get_object()
        
        if not request.user.can_edit_content:
            return Response({'detail': 'No tienes permisos'}, status=status.HTTP_403_FORBIDDEN)
        
        topic.is_locked = False
        topic.save()
        return Response({'detail': 'Topic desbloqueado'})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by topic
        topic_slug = self.request.query_params.get('topic')
        if topic_slug:
            queryset = queryset.filter(topic__slug=topic_slug)
        
        return queryset.select_related('author', 'topic')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupPostViewSet(viewsets.ModelViewSet):
    queryset = GroupPost.objects.filter(is_active=True)
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by group
        group_slug = self.request.query_params.get('group')
        if group_slug:
            queryset = queryset.filter(group__slug=group_slug)
            
            # Check if user is member
            group = Group.objects.filter(slug=group_slug).first()
            if group and not group.members.filter(id=self.request.user.id).exists():
                # Not a member, return empty queryset
                return queryset.none()
        
        return queryset.select_related('author', 'group')
    
    def perform_create(self, serializer):
        group = serializer.validated_data.get('group')
        
        # Check if user is a member
        if not group.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied('Debes ser miembro del grupo para publicar')
        
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def pin(self, request, pk=None):
        post = self.get_object()
        
        # Only group admins can pin
        membership = GroupMembership.objects.filter(
            group=post.group,
            user=request.user,
            role__in=['admin', 'moderator']
        ).first()
        
        if not membership and not request.user.can_edit_content:
            return Response({'detail': 'No tienes permisos'}, status=status.HTTP_403_FORBIDDEN)
        
        post.is_pinned = not post.is_pinned
        post.save()
        return Response({'detail': 'Post fixed' if post.is_pinned else 'Post unfixed'})


class GroupPostCommentViewSet(viewsets.ModelViewSet):
    queryset = GroupPostComment.objects.all()
    serializer_class = GroupPostCommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by post
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        return queryset.select_related('author', 'post')
    
    def perform_create(self, serializer):
        post = serializer.validated_data.get('post')
        
        # Check if user is a member of the group
        if not post.group.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied('Debes ser miembro del grupo para comentar')
        
        serializer.save(author=self.request.user)


from rest_framework.decorators import api_view, permission_classes as perm_classes
from rest_framework.permissions import AllowAny
from users.serializers import UserSerializer


@api_view(['GET'])
@perm_classes([AllowAny])
def community_stats(request):
    """Get community statistics including most active members"""
    User = get_user_model()
    
    # Calculate activity score for each user based on their community contributions
    active_users = User.objects.annotate(
        # Count forum topics created
        topics_count=Count('forum_topics', distinct=True),
        # Count forum posts
        posts_count=Count('forum_posts', distinct=True),
        # Count group posts
        group_posts_count=Count('group_posts', distinct=True),
        # Count group post comments
        group_comments_count=Count('group_post_comments', distinct=True),
        # Total activity score
        activity_score=(
            Count('forum_topics', distinct=True) * 5 +  # Topics worth more
            Count('forum_posts', distinct=True) * 2 +
            Count('group_posts', distinct=True) * 3 +
            Count('group_post_comments', distinct=True)
        )
    ).filter(
        activity_score__gt=0
    ).order_by('-activity_score')[:20]
    
    active_members_data = []
    for user in active_users:
        # Get full avatar URL
        avatar_url = None
        if user.avatar:
            avatar_url = request.build_absolute_uri(user.avatar.url)
        
        active_members_data.append({
            'id': user.id,
            'username': user.username,
            'avatar': avatar_url,
            'role': user.role,
            'activity_score': user.activity_score,
            'contributions': {
                'topics': user.topics_count,
                'posts': user.posts_count,
                'group_posts': user.group_posts_count,
                'comments': user.group_comments_count
            }
        })
    
    return Response({
        'active_members': active_members_data,
        'total_groups': Group.objects.filter(is_active=True).count(),
        'total_forums': Forum.objects.filter(is_active=True).count(),
        'total_topics': Topic.objects.filter(is_active=True).count(),
        'total_members': User.objects.filter(is_active=True).count()
    })
