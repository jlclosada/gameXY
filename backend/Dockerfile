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

# Ejecuta migraciones y arranca Gunicorn con logs visibles
CMD echo "🚀 Iniciando despliegue..." && \
    echo "🔹 Aplicando migraciones de base de datos..." && \
    python manage.py migrate --noinput && \
    echo "✅ Migraciones completadas." && \
    echo "🔹 Ejecutando verificación de salud..." && \
    python manage.py check --deploy && \
    echo "✅ Verificación OK. Iniciando servidor Gunicorn..." && \
    gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} \
    --log-level debug \
    --access-logfile - \
    --error-logfile -
