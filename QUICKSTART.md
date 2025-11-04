# 🚀 Inicio Rápido - GameForum

Esta guía te ayudará a poner en marcha el proyecto en menos de 5 minutos.

## ⚡ Pasos Rápidos

### 1. Backend (Terminal 1)

```bash
# Navegar al backend
cd backend

# Crear entorno virtual (primera vez)
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Instalar dependencias (primera vez)
pip install -r requirements.txt

# Crear base de datos (primera vez)
python manage.py migrate

# Crear superusuario (primera vez)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

✅ Backend corriendo en: http://localhost:8000

### 2. Frontend (Terminal 2)

```bash
# Navegar al frontend
cd frontend

# Instalar dependencias (primera vez)
npm install

# Iniciar servidor de desarrollo
npm run dev
```

✅ Frontend corriendo en: http://localhost:5173

## 🎯 Próximos Pasos

1. **Accede al Panel Admin**: http://localhost:8000/admin
   - Usa las credenciales del superusuario
   - Crea algunos juegos, categorías y contenido de prueba

2. **Explora la Aplicación**: http://localhost:5173
   - Regístrate como nuevo usuario
   - Navega por las diferentes secciones

3. **Prueba la API**: http://localhost:8000/api/
   - Endpoints disponibles en el README

## 🔧 Solución de Problemas

### Backend no inicia
- Verifica que el entorno virtual esté activado
- Asegúrate de haber ejecutado las migraciones
- Revisa que el puerto 8000 esté libre

### Frontend no inicia
- Verifica que Node.js esté instalado (`node -v`)
- Elimina `node_modules` y ejecuta `npm install` nuevamente
- Revisa que el puerto 5173 esté libre

### Error de CORS
- Verifica que el backend esté corriendo en el puerto 8000
- Revisa la configuración de CORS en `backend/backend/settings.py`

## 📝 Comandos Útiles

### Backend
```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar shell de Django
python manage.py shell
```

### Frontend
```bash
# Instalar nueva dependencia
npm install nombre-paquete

# Construir para producción
npm run build

# Vista previa de producción
npm run preview
```

## 🎮 ¡Listo para Desarrollar!

Ahora puedes comenzar a desarrollar tu plataforma de videojuegos. Consulta el README.md para más información sobre la arquitectura y características del proyecto.

---

¿Necesitas ayuda? Revisa la documentación completa en README.md
