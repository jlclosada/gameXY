from .models import Notification


class NotificationService:
    """Servicio para crear notificaciones"""
    
    @staticmethod
    def create_notification(recipient, notification_type, title, message, sender=None, content_object=None, action_url=''):
        """Crear una nueva notificación"""
        # No notificar al mismo usuario
        if sender and recipient == sender:
            return None
        
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            title=title,
            message=message,
            content_object=content_object,
            action_url=action_url
        )
        return notification
    
    @staticmethod
    def notify_comment_reply(comment, reply_author):
        """Notificar cuando alguien responde a un comentario"""
        parent_comment = comment.parent
        if parent_comment and parent_comment.user != reply_author:
            NotificationService.create_notification(
                recipient=parent_comment.user,
                sender=reply_author,
                notification_type='comment_reply',
                title='Nueva respuesta a tu comentario',
                message=f'{reply_author.username} respondió a tu comentario',
                content_object=comment,
                action_url=f'/guides/{comment.guide.slug}' if comment.guide else ''
            )
    
    @staticmethod
    def notify_guide_like(guide, liker):
        """Notificar cuando alguien da like a una guía"""
        NotificationService.create_notification(
            recipient=guide.author,
            sender=liker,
            notification_type='guide_like',
            title='¡Nueva reacción en tu guía!',
            message=f'A {liker.username} le gustó tu guía "{guide.title}"',
            content_object=guide,
            action_url=f'/guides/{guide.slug}'
        )
    
    @staticmethod
    def notify_guide_rating(guide, rater, rating_value):
        """Notificar cuando alguien valora una guía"""
        stars = '⭐' * rating_value
        NotificationService.create_notification(
            recipient=guide.author,
            sender=rater,
            notification_type='guide_rating',
            title='Nueva valoración en tu guía',
            message=f'{rater.username} valoró tu guía "{guide.title}" con {stars}',
            content_object=guide,
            action_url=f'/guides/{guide.slug}'
        )
    
    @staticmethod
    def notify_achievement_unlocked(user, achievement):
        """Notificar cuando un usuario desbloquea un logro"""
        NotificationService.create_notification(
            recipient=user,
            notification_type='achievement',
            title=f'¡Logro desbloqueado! {achievement.icon}',
            message=f'Has desbloqueado "{achievement.name}": {achievement.description}',
            content_object=achievement,
            action_url='/profile'
        )
    
    @staticmethod
    def notify_new_guide_favorite_game(guide):
        """Notificar a usuarios que tienen el juego como favorito sobre nueva guía"""
        if guide.game:
            # Obtener usuarios que tienen este juego como favorito (excepto el autor)
            users_with_favorite = guide.game.favorited_by.exclude(id=guide.author.id)
            
            for user in users_with_favorite[:100]:  # Limitar a 100 para no saturar
                NotificationService.create_notification(
                    recipient=user,
                    sender=guide.author,
                    notification_type='new_guide_favorite_game',
                    title=f'Nueva guía de {guide.game.title}',
                    message=f'{guide.author.username} publicó una nueva guía: "{guide.title}"',
                    content_object=guide,
                    action_url=f'/guides/{guide.slug}'
                )
    
    @staticmethod
    def get_unread_count(user):
        """Obtener cantidad de notificaciones no leídas"""
        return Notification.objects.filter(recipient=user, is_read=False).count()
    
    @staticmethod
    def mark_all_as_read(user):
        """Marcar todas las notificaciones como leídas"""
        from django.utils import timezone
        Notification.objects.filter(recipient=user, is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
    
    @staticmethod
    def notify_forum_post_reply(post, topic_author):
        """Notificar al autor del tema cuando alguien responde"""
        NotificationService.create_notification(
            recipient=topic_author,
            sender=post.author,
            notification_type='post_reply',
            title='Nueva respuesta en tu tema',
            message=f'{post.author.username} respondió a tu tema',
            content_object=post,
            action_url=f'/community/forums/{post.topic.forum.slug}/topics/{post.topic.slug}'
        )
    
    @staticmethod
    def notify_group_post_comment(comment, post_author):
        """Notificar al autor del post cuando alguien comenta"""
        NotificationService.create_notification(
            recipient=post_author,
            sender=comment.author,
            notification_type='group_post_comment',
            title='Nuevo comentario en tu publicación',
            message=f'{comment.author.username} comentó tu publicación',
            content_object=comment,
            action_url=f'/community/groups/{comment.post.group.slug}'
        )
    
    @staticmethod
    def notify_join_request(join_request, group_creator):
        """Notificar al creador del grupo sobre solicitud de ingreso"""
        NotificationService.create_notification(
            recipient=group_creator,
            sender=join_request.user,
            notification_type='join_request',
            title='Nueva solicitud para unirse a tu grupo',
            message=f'{join_request.user.username} quiere unirse a {join_request.group.name}',
            content_object=join_request,
            action_url=f'/community/groups/{join_request.group.slug}'
        )
    
    @staticmethod
    def notify_join_approved(join_request):
        """Notificar al usuario que su solicitud fue aprobada"""
        NotificationService.create_notification(
            recipient=join_request.user,
            sender=None,
            notification_type='join_approved',
            title='Solicitud aprobada',
            message=f'Tu solicitud para unirte a {join_request.group.name} fue aprobada',
            content_object=join_request.group,
            action_url=f'/community/groups/{join_request.group.slug}'
        )
    
    @staticmethod
    def notify_join_rejected(join_request):
        """Notificar al usuario que su solicitud fue rechazada"""
        NotificationService.create_notification(
            recipient=join_request.user,
            sender=None,
            notification_type='join_rejected',
            title='Solicitud rechazada',
            message=f'Tu solicitud para unirte a {join_request.group.name} fue rechazada',
            content_object=join_request.group,
            action_url='/community'
        )
    
    @staticmethod
    def notify_group_invitation(invitation):
        """Notificar al usuario sobre invitación a grupo"""
        NotificationService.create_notification(
            recipient=invitation.invitee,
            sender=invitation.inviter,
            notification_type='group_invitation',
            title='Invitación a grupo',
            message=f'{invitation.inviter.username} te ha invitado a unirte a {invitation.group.name}',
            content_object=invitation,
            action_url=f'/community/groups/{invitation.group.slug}'
        )
    
    @staticmethod
    def notify_invitation_accepted(invitation):
        """Notificar al invitador que se aceptó la invitación"""
        NotificationService.create_notification(
            recipient=invitation.inviter,
            sender=invitation.invitee,
            notification_type='invitation_accepted',
            title='Invitación aceptada',
            message=f'{invitation.invitee.username} ha aceptado tu invitación a {invitation.group.name}',
            content_object=invitation.group,
            action_url=f'/community/groups/{invitation.group.slug}'
        )
    
    @staticmethod
    def notify_invitation_rejected(invitation):
        """Notificar al invitador que se rechazó la invitación"""
        NotificationService.create_notification(
            recipient=invitation.inviter,
            sender=invitation.invitee,
            notification_type='invitation_rejected',
            title='Invitación rechazada',
            message=f'{invitation.invitee.username} ha rechazado tu invitación a {invitation.group.name}',
            content_object=invitation.group,
            action_url=f'/community/groups/{invitation.group.slug}'
        )
