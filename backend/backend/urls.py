from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse

import sys

def healthcheck(request):
    """Healthcheck endpoint para Railway y otros servicios de deployment."""
    from django.db import connection
    try:
        # Verificar que la BD está accesible
        connection.ensure_connection()
        print("🩺 [HEALTHCHECK] OK - Base de datos conectada ✅", flush=True)
        return JsonResponse({"status": "healthy", "database": "connected"})
    except Exception as e:
        print(f"❌ [HEALTHCHECK] ERROR - {str(e)}", flush=True, file=sys.stderr)
        return JsonResponse({"status": "unhealthy", "error": str(e)}, status=503)

def create_admin(request):
    """Endpoint temporal para crear superuser. ELIMINAR después de usar."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Verificar si ya existe
    if User.objects.filter(username='admin').exists():
        return JsonResponse({
            "status": "exists",
            "message": "Admin user already exists",
            "login_url": "https://gamexy-production-9e2b.up.railway.app/admin/"
        })
    
    # Crear superuser
    try:
        user = User.objects.create_superuser(
            username='admin',
            email='admin@gamexy.com',
            password='Admin123456!'  # CAMBIAR DESPUÉS
        )
        return JsonResponse({
            "status": "created",
            "message": "Superuser created successfully",
            "username": "admin",
            "password": "Admin123456!",
            "login_url": "https://gamexy-production-9e2b.up.railway.app/admin/",
            "warning": "Change password immediately after login!"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e)
        }, status=500)

urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('health', healthcheck, name='healthcheck_no_slash'),  # Sin barra final también
    path('create-admin-temp/', create_admin, name='create_admin'),  # TEMPORAL - ELIMINAR DESPUÉS
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/games/', include('games.urls')),
    path('api/content/', include('content.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
