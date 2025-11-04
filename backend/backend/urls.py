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

def cloudinary_check(request):
    """Endpoint para verificar configuración de Cloudinary"""
    from django.conf import settings
    import os
    
    cloudinary_url = os.getenv('CLOUDINARY_URL')
    default_storage = settings.DEFAULT_FILE_STORAGE if hasattr(settings, 'DEFAULT_FILE_STORAGE') else 'Not set'
    
    return JsonResponse({
        "cloudinary_url_set": bool(cloudinary_url),
        "cloudinary_url_preview": cloudinary_url[:30] + '...' if cloudinary_url else None,
        "default_file_storage": default_storage,
        "cloudinary_storage_set": hasattr(settings, 'CLOUDINARY_STORAGE'),
    })


urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('health', healthcheck, name='healthcheck_no_slash'),  # Sin barra final también
    path('cloudinary-check/', cloudinary_check, name='cloudinary_check'),  # TEMPORAL
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/games/', include('games.urls')),
    path('api/content/', include('content.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
