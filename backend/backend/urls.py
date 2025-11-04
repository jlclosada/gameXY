from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse

import sys
import os

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

def media_check(request):
    """Endpoint para verificar archivos media"""
    from django.conf import settings
    import os
    
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    
    # Listar archivos en media
    files = []
    try:
        if os.path.exists(media_root):
            for root, dirs, filenames in os.walk(media_root):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    rel_path = os.path.relpath(filepath, media_root)
                    files.append({
                        'path': rel_path,
                        'size': os.path.getsize(filepath),
                        'exists': True
                    })
    except Exception as e:
        files.append({'error': str(e)})
    
    return JsonResponse({
        "media_root": str(media_root),
        "media_url": media_url,
        "media_root_exists": os.path.exists(media_root),
        "media_root_writable": os.access(media_root, os.W_OK) if os.path.exists(media_root) else False,
        "files_count": len(files),
        "files": files[:20],  # Mostrar solo los primeros 20
        "railway_environment": os.getenv('RAILWAY_ENVIRONMENT'),
    })


urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('health', healthcheck, name='healthcheck_no_slash'),  # Sin barra final también
    path('media-check/', media_check, name='media_check'),  # TEMPORAL
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/games/', include('games.urls')),
    path('api/content/', include('content.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Crear vista personalizada para servir media con logging
def serve_media(request, path):
    """Vista personalizada para servir archivos media con logging"""
    import os
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    print(f"[MEDIA] Requested: {path}", flush=True)
    print(f"[MEDIA] Full path: {full_path}", flush=True)
    print(f"[MEDIA] Exists: {os.path.exists(full_path)}", flush=True)
    print(f"[MEDIA] MEDIA_ROOT: {settings.MEDIA_ROOT}", flush=True)
    return serve(request, path, document_root=settings.MEDIA_ROOT)

# Servir archivos media
if settings.DEBUG:
    # En desarrollo, usar el helper estándar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # En producción, servir explícitamente con vista personalizada
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve_media),
    ]
