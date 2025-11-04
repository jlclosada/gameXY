# Usa una imagen base ligera de Python
FROM python:3.9-slim

# Evita que Python genere archivos .pyc y usa salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de dependencias e instálalas
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Recoge archivos estáticos (sin interrumpir el build si falla)
RUN python manage.py collectstatic --noinput || true

# Expón el puerto (Railway usa la variable $PORT) ok
EXPOSE 8000

# Ejecuta migraciones y arranca Gunicorn con logs visibles goooooo
CMD echo "🚀 Iniciando despliegue..." && \
    echo "🔹 Variables de entorno detectadas:" && \
    echo "PORT=${PORT}" && \
    echo "DATABASE_URL presente: $(if [ -n "$DATABASE_URL" ]; then echo 'SI'; else echo 'NO'; fi)" && \
    echo "🔹 Aplicando migraciones de base de datos..." && \
    python manage.py migrate --noinput && \
    echo "✅ Migraciones completadas." && \
    echo "🔹 Colectando archivos estáticos..." && \
    python manage.py collectstatic --noinput && \
    echo "✅ Estáticos OK. Iniciando servidor Gunicorn en puerto ${PORT:-8000}..." && \
    gunicorn backend.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --capture-output
