import os
import sys
from django.core.wsgi import get_wsgi_application

print("🔹 [WSGI] Iniciando aplicación Django...", flush=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

try:
    application = get_wsgi_application()
    print("✅ [WSGI] Django application cargada correctamente.", flush=True)
except Exception as e:
    print("❌ [WSGI ERROR] Fallo al iniciar Django:", e, file=sys.stderr, flush=True)
    raise
