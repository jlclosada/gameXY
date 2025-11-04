from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse


def healthcheck(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path('', healthcheck),
    path('api/', healthcheck),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/games/', include('games.urls')),
    path('api/content/', include('content.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
