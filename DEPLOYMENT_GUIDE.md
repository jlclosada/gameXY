# Guía de Deployment - GameXY

## Opción 1: Railway (Recomendado - Más Fácil)

### Backend Django en Railway

**Ventajas**: Fácil, gratis para empezar, PostgreSQL incluido, despliegue automático desde Git

1. **Preparar el proyecto**
   ```bash
   cd backend
   pip freeze > requirements.txt
   ```

2. **Crear archivo `railway.toml`**
   ```toml
   [build]
   builder = "NIXPACKS"
   
   [deploy]
   startCommand = "gunicorn backend.wsgi --bind 0.0.0.0:$PORT"
   ```

3. **Crear `Procfile`**
   ```
   web: gunicorn backend.wsgi --bind 0.0.0.0:$PORT
   release: python manage.py migrate
   ```

4. **Actualizar `settings.py`**
   ```python
   import os
   import dj_database_url
   
   ALLOWED_HOSTS = ['*']  # Después especifica tu dominio
   
   # Database
   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///db.sqlite3',
           conn_max_age=600
       )
   }
   
   # Static files
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATIC_URL = '/static/'
   
   # Media files (usar servicio externo como AWS S3 o Cloudinary)
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   MEDIA_URL = '/media/'
   ```

5. **Instalar dependencias adicionales**
   ```bash
   pip install gunicorn dj-database-url psycopg2-binary whitenoise
   pip freeze > requirements.txt
   ```

6. **Deployment en Railway**
   - Ve a [railway.app](https://railway.app)
   - Conecta tu repositorio GitHub
   - Selecciona el backend
   - Railway detectará automáticamente que es Django
   - Añade PostgreSQL desde "Add Service"
   - Configura variables de entorno:
     - `SECRET_KEY`: tu clave secreta
     - `DEBUG`: False
     - `ALLOWED_HOSTS`: tu-app.railway.app
   - Deploy automático

### Frontend Vue en Vercel

**Ventajas**: Gratis, CDN global, SSL automático, despliegue instantáneo

1. **Preparar el proyecto**
   ```bash
   cd frontend
   ```

2. **Crear `vercel.json`**
   ```json
   {
     "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
   }
   ```

3. **Actualizar variable de entorno**
   - Crear archivo `.env.production`
   ```
   VITE_API_URL=https://tu-backend.railway.app/api
   ```

4. **Deployment en Vercel**
   - Ve a [vercel.com](https://vercel.com)
   - Importa tu repositorio
   - Framework: Vue.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Añade variable de entorno `VITE_API_URL`
   - Deploy

---

## Opción 2: Render (Alternativa Gratuita)

### Backend Django en Render

1. **Crear `render.yaml`**
   ```yaml
   services:
     - type: web
       name: gamexy-backend
       env: python
       buildCommand: "pip install -r requirements.txt"
       startCommand: "gunicorn backend.wsgi:application"
       envVars:
         - key: PYTHON_VERSION
           value: 3.9.0
         - key: SECRET_KEY
           generateValue: true
         - key: DEBUG
           value: False
   
   databases:
     - name: gamexy-db
       databaseName: gamexy
       user: gamexy
   ```

2. **Deploy**
   - Ve a [render.com](https://render.com)
   - Conecta GitHub
   - Selecciona el repositorio
   - Sigue las instrucciones

### Frontend en Render Static Site

1. **Deploy**
   - New > Static Site
   - Conecta repositorio
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

---

## Opción 3: VPS (Servidor Propio) - Avanzado

### Usando DigitalOcean, Linode o AWS EC2

**Mejor para**: Producción profesional, control total

#### 1. Configurar Servidor (Ubuntu 22.04)

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install python3-pip python3-venv nginx postgresql git -y

# Instalar Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

#### 2. Configurar PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE gamexy;
CREATE USER gamexy WITH PASSWORD 'tu_password_segura';
GRANT ALL PRIVILEGES ON DATABASE gamexy TO gamexy;
\q
```

#### 3. Desplegar Backend

```bash
# Clonar repositorio
cd /var/www
sudo git clone tu-repositorio.git gamexy
cd gamexy/backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn

# Configurar Django
python manage.py collectstatic
python manage.py migrate

# Crear servicio systemd
sudo nano /etc/systemd/system/gamexy.service
```

**Contenido del servicio:**
```ini
[Unit]
Description=GameXY Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/gamexy/backend
Environment="PATH=/var/www/gamexy/backend/venv/bin"
ExecStart=/var/www/gamexy/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 backend.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start gamexy
sudo systemctl enable gamexy
```

#### 4. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/gamexy
```

**Contenido:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /media/ {
        alias /var/www/gamexy/backend/media/;
    }

    location /static/ {
        alias /var/www/gamexy/backend/staticfiles/;
    }

    location / {
        root /var/www/gamexy/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/gamexy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Desplegar Frontend

```bash
cd /var/www/gamexy/frontend
npm install
npm run build
```

#### 6. SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

---

## Configuraciones Importantes

### CORS en Django

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "https://tu-frontend.vercel.app",
    "https://tu-dominio.com",
]
```

### Variables de Entorno

**Backend (.env)**
```
SECRET_KEY=tu-secret-key-muy-segura
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname
ALLOWED_HOSTS=tu-dominio.com,tu-backend.railway.app
```

**Frontend (.env.production)**
```
VITE_API_URL=https://tu-backend.railway.app/api
```

---

## Gestión de Archivos Estáticos y Media

### Opción 1: Cloudinary (Recomendado para imágenes)

```bash
pip install cloudinary django-cloudinary-storage
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'cloudinary_storage',
    'cloudinary',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'tu-cloud-name',
    'API_KEY': 'tu-api-key',
    'API_SECRET': 'tu-api-secret'
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

### Opción 2: AWS S3

```bash
pip install boto3 django-storages
```

---

## Checklist Pre-Deployment

- [ ] `DEBUG = False` en producción
- [ ] `SECRET_KEY` segura y en variables de entorno
- [ ] `ALLOWED_HOSTS` configurado
- [ ] CORS configurado correctamente
- [ ] Base de datos PostgreSQL configurada
- [ ] Migraciones aplicadas
- [ ] Archivos estáticos recolectados
- [ ] SSL/HTTPS habilitado
- [ ] Variables de entorno configuradas
- [ ] Backup de base de datos configurado

---

## Monitoreo y Mantenimiento

### Logs en Railway
```bash
railway logs
```

### Logs en VPS
```bash
sudo journalctl -u gamexy -f
sudo tail -f /var/log/nginx/error.log
```

---

## Costos Estimados

| Servicio | Plan Gratuito | Plan Pago |
|----------|---------------|-----------|
| **Railway** | $5 crédito/mes | Desde $5/mes |
| **Vercel** | Ilimitado (hobby) | Desde $20/mes |
| **Render** | 750h/mes | Desde $7/mes |
| **DigitalOcean** | - | Desde $4/mes |
| **Cloudinary** | 25 GB | Desde $89/mes |

---

## Recomendación Final

**Para empezar (Gratis)**:
- Backend: Railway
- Frontend: Vercel
- Media: Cloudinary Free Tier

**Para producción**:
- VPS (DigitalOcean) con Nginx + PostgreSQL
- CDN para frontend
- S3 para archivos media
