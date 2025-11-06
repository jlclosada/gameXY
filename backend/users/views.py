from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .serializers import UserSerializer, UserPublicSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'list', 'complete_profile']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] and self.request.user != self.get_object():
            return UserPublicSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def follow_game(self, request, pk=None):
        user = request.user
        game_id = request.data.get('game_id')
        if game_id:
            user.favorite_games.add(game_id)
            return Response({'status': 'game followed'})
        return Response({'error': 'game_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unfollow_game(self, request, pk=None):
        user = request.user
        game_id = request.data.get('game_id')
        if game_id:
            user.favorite_games.remove(game_id)
            return Response({'status': 'game unfollowed'})
        return Response({'error': 'game_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Actualizar información del perfil del usuario autenticado"""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        # No permitir cambiar username y email
        if 'username' in request.data:
            return Response(
                {'error': 'No puedes cambiar tu nombre de usuario'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if 'email' in request.data:
            return Response(
                {'error': 'No puedes cambiar tu correo electrónico'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def complete_profile(self, request):
        """Completar información adicional del perfil tras el registro y hacer login"""
        from rest_framework_simplejwt.tokens import RefreshToken
        from django.contrib.auth import authenticate
        
        # Obtener credenciales
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email y contraseña son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Autenticar usuario
        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Validar que el username no esté en uso
        new_username = request.data.get('username')
        if new_username:
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                return Response(
                    {'error': 'Este nombre de usuario ya está en uso'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Actualizar perfil
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Marcar perfil como completado
            serializer.save(profile_completed=True)
            
            # Generar tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data,
                'message': 'Perfil completado exitosamente'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Cambiar contraseña del usuario autenticado"""
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        # Validaciones
        if not current_password or not new_password or not confirm_password:
            return Response(
                {'error': 'Todos los campos son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(current_password):
            return Response(
                {'error': 'La contraseña actual es incorrecta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_password != confirm_password:
            return Response(
                {'error': 'Las contraseñas nuevas no coinciden'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar la nueva contraseña con las validaciones de Django
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response(
                {'error': list(e.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cambiar la contraseña
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Contraseña actualizada correctamente'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def achievements(self, request):
        """Obtener progreso de logros del usuario"""
        from .achievement_service import AchievementService
        progress = AchievementService.get_user_progress(request.user)
        return Response(progress)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def check_achievements(self, request):
        """Verificar y desbloquear logros del usuario"""
        from .achievement_service import AchievementService
        newly_unlocked = AchievementService.check_all_achievements(request.user)
        
        if newly_unlocked:
            achievements_data = [{
                'id': ach.achievement.id,
                'code': ach.achievement.code,
                'name': ach.achievement.name,
                'description': ach.achievement.description,
                'icon': ach.achievement.icon,
                'points': ach.achievement.points,
            } for ach in newly_unlocked]
            
            return Response({
                'newly_unlocked': achievements_data,
                'message': f'¡Has desbloqueado {len(newly_unlocked)} logro(s)!'
            })
        
        return Response({
            'newly_unlocked': [],
            'message': 'No hay nuevos logros desbloqueados'
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def notifications(self, request):
        """Obtener notificaciones del usuario"""
        from .models import Notification
        notifications = request.user.notifications.all()[:50]  # Últimas 50
        
        data = [{
            'id': n.id,
            'type': n.notification_type,
            'title': n.title,
            'message': n.message,
            'action_url': n.action_url,
            'is_read': n.is_read,
            'created_at': n.created_at,
            'sender': {
                'username': n.sender.username,
                'avatar': n.sender.avatar.url if n.sender and n.sender.avatar else None
            } if n.sender else None
        } for n in notifications]
        
        return Response(data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def unread_notifications_count(self, request):
        """Obtener contador de notificaciones no leídas"""
        from .notifications import NotificationService
        count = NotificationService.get_unread_count(request.user)
        return Response({'unread_count': count})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_notification_read(self, request, pk=None):
        """Marcar una notificación como leída"""
        from .models import Notification
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
            notification.mark_as_read()
            return Response({'status': 'marked as read'})
        except Notification.DoesNotExist:
            return Response({'error': 'Notificación no encontrada'}, status=404)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_all_notifications_read(self, request):
        """Marcar todas las notificaciones como leídas"""
        from .notifications import NotificationService
        NotificationService.mark_all_as_read(request.user)
        return Response({'status': 'all marked as read'})
