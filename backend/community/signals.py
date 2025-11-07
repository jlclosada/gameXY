from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, GroupPostComment, GroupJoinRequest, GroupInvitation
from users.notifications import NotificationService


@receiver(post_save, sender=Post)
def notify_on_topic_reply(sender, instance, created, **kwargs):
    """Notificar al autor del tema cuando alguien responde"""
    if created and instance.topic.author != instance.author:
        NotificationService.notify_forum_post_reply(instance, instance.topic.author)


@receiver(post_save, sender=GroupPostComment)
def notify_on_group_post_comment(sender, instance, created, **kwargs):
    """Notificar al autor del post cuando alguien comenta"""
    if created and instance.post.author != instance.author:
        NotificationService.notify_group_post_comment(instance, instance.post.author)


@receiver(post_save, sender=GroupJoinRequest)
def notify_on_join_request(sender, instance, created, **kwargs):
    """Notificar al creador del grupo sobre nuevas solicitudes"""
    if created and instance.status == 'pending':
        NotificationService.notify_join_request(instance, instance.group.creator)
        
        # También notificar a admins y moderadores
        from .models import GroupMembership
        admins_and_mods = GroupMembership.objects.filter(
            group=instance.group,
            role__in=['admin', 'moderator']
        ).exclude(user=instance.group.creator)
        
        for membership in admins_and_mods:
            NotificationService.notify_join_request(instance, membership.user)
    
    # Notificar cuando se aprueba o rechaza
    elif not created:
        if instance.status == 'approved':
            NotificationService.notify_join_approved(instance)
        elif instance.status == 'rejected':
            NotificationService.notify_join_rejected(instance)


@receiver(post_save, sender=GroupInvitation)
def notify_on_invitation(sender, instance, created, **kwargs):
    """Notificar cuando se envía, acepta o rechaza una invitación"""
    if created:
        # New invitation
        NotificationService.notify_group_invitation(instance)
    else:
        # Status changed
        if instance.status == 'accepted':
            NotificationService.notify_invitation_accepted(instance)
        elif instance.status == 'rejected':
            NotificationService.notify_invitation_rejected(instance)
