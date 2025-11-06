from rest_framework import permissions


class IsGoatUser(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es GOAT o Admin
    """
    message = 'Solo los usuarios GOAT o Admin pueden realizar esta acción.'

    def has_permission(self, request, view):
        # Los métodos de lectura están permitidos para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Solo usuarios autenticados y con rol GOAT o Admin pueden crear/editar
        return request.user and request.user.is_authenticated and request.user.can_edit_content


class IsGoatOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite lectura a todos pero escritura solo a GOAT o Admin
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.can_edit_content

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.can_edit_content
