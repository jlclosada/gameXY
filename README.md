# 🎮 GameForum

Una plataforma moderna y elegante para la comunidad de videojuegos, donde los usuarios pueden explorar juegos, leer noticias, seguir guías y compartir contenido.

## ✨ Características

- 🎯 **Exploración de Juegos**: Navega por una base de datos completa de videojuegos con información detallada
- 📰 **Noticias**: Mantente al día con las últimas noticias del mundo gaming
- 📖 **Guías**: Aprende con guías detalladas creadas por la comunidad
- 💬 **Posts y Comentarios**: Comparte tus experiencias y opiniones
- 👤 **Sistema de Usuarios**: Registro, autenticación y perfiles personalizados
- ❤️ **Interacciones Sociales**: Sigue juegos, da likes y comenta
- 🎨 **Diseño Moderno**: Interfaz elegante y minimalista con Tailwind CSS

## 🛠️ Tecnologías

### Backend
- **Django 4.2**: Framework web de Python
- **Django REST Framework**: API REST completa
- **Django Simple JWT**: Autenticación con tokens JWT
- **Django CORS Headers**: Manejo de CORS
- **Pillow**: Procesamiento de imágenes
- **SQLite**: Base de datos (fácil de cambiar a PostgreSQL)

### Frontend
- **Vue 3**: Framework JavaScript progresivo con Composition API
- **Vite**: Herramienta de construcción ultra rápida
- **Vue Router**: Enrutamiento SPA
- **Pinia**: Gestión de estado moderna
- **Axios**: Cliente HTTP
- **Tailwind CSS**: Framework CSS utility-first
- **Headless UI**: Componentes UI accesibles
- **Heroicons**: Iconos SVG

## 📋 Requisitos Previos

- Python 3.8+
- Node.js 16+
- npm o yarn

## 🚀 Instalación

### Backend (Django)

1. Navega al directorio del backend:
```bash
cd backend
```

2. Crea y activa un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta las migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crea un superusuario:
```bash
python manage.py createsuperuser
```

6. Inicia el servidor de desarrollo:
```bash
python manage.py runserver
```

El backend estará disponible en `http://localhost:8000`

### Frontend (Vue)

1. Navega al directorio del frontend:
```bash
cd frontend
```

2. Instala las dependencias:
```bash
npm install
```

3. Inicia el servidor de desarrollo:
```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

## 📁 Estructura del Proyecto

```
gameforum/
├── backend/
│   ├── backend/           # Configuración principal de Django
│   ├── users/            # App de usuarios personalizados
│   ├── games/            # App de juegos y categorías
│   ├── content/          # App de noticias, posts y guías
│   ├── media/            # Archivos multimedia subidos
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── api/          # Configuración de Axios
    │   ├── assets/       # CSS y archivos estáticos
    │   ├── components/   # Componentes Vue reutilizables
    │   ├── router/       # Configuración de rutas
    │   ├── stores/       # Stores de Pinia
    │   ├── views/        # Vistas/páginas principales
    │   ├── App.vue
    │   └── main.js
    ├── index.html
    ├── package.json
    ├── tailwind.config.js
    └── vite.config.js
```

## 🔌 API Endpoints

### Autenticación
- `POST /api/auth/login/` - Iniciar sesión
- `POST /api/auth/users/` - Registrar usuario
- `GET /api/auth/users/me/` - Obtener usuario actual
- `POST /api/token/refresh/` - Refrescar token JWT

### Juegos
- `GET /api/games/` - Listar juegos
- `GET /api/games/{slug}/` - Detalle de juego
- `GET /api/games/categories/` - Listar categorías

### Contenido
- `GET /api/content/news/` - Listar noticias
- `GET /api/content/news/{slug}/` - Detalle de noticia
- `GET /api/content/guides/` - Listar guías
- `GET /api/content/guides/{slug}/` - Detalle de guía
- `GET /api/content/posts/` - Listar posts
- `GET /api/content/posts/{slug}/` - Detalle de post
- `POST /api/content/posts/{slug}/like/` - Toggle like en post
- `POST /api/content/guides/{slug}/like/` - Toggle like en guía
- `GET /api/content/comments/` - Listar comentarios

## 👨‍💼 Panel de Administración

Accede al panel de administración de Django en `http://localhost:8000/admin` usando las credenciales del superusuario.

Desde aquí puedes:
- Gestionar usuarios
- Crear y editar juegos
- Publicar noticias
- Moderar contenido
- Gestionar categorías

## 🎨 Personalización

### Colores (Tailwind)
Edita `frontend/tailwind.config.js` para personalizar los colores del tema:

```javascript
colors: {
  primary: { /* tus colores */ },
  dark: { /* tus colores */ }
}
```

### Fuentes
Las fuentes actuales son **Inter** y **Outfit** desde Google Fonts. Cámbielas en `frontend/index.html`.

## 🔒 Seguridad

Antes de desplegar en producción:

1. Cambia `SECRET_KEY` en `backend/backend/settings.py`
2. Establece `DEBUG = False`
3. Configura `ALLOWED_HOSTS` correctamente
4. Usa una base de datos de producción (PostgreSQL)
5. Configura HTTPS
6. Implementa rate limiting
7. Revisa la configuración de CORS

## 🚢 Despliegue

### Backend
- **Railway**, **Render**, **Heroku** o **DigitalOcean**
- Usa **Gunicorn** como servidor WSGI
- Configura variables de entorno
- Usa **PostgreSQL** o **MySQL**

### Frontend
- **Vercel**, **Netlify** o **Cloudflare Pages**
- Ejecuta `npm run build`
- Despliega el directorio `dist/`

## 📝 Datos de Ejemplo

Para poblar la base de datos con datos de prueba, usa el panel de administración o crea un comando personalizado de Django.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🙏 Agradecimientos

- Django y Django REST Framework por el poderoso backend
- Vue.js por el increíble framework frontend
- Tailwind CSS por el sistema de diseño
- La comunidad de desarrollo open source

---

Desarrollado con ❤️ para la comunidad gamer
