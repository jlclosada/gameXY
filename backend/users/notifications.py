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
