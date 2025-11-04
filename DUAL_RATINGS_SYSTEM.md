# Sistema de Valoraciones Duales

## Descripción General

El sistema de valoraciones duales permite distinguir entre:
- **Valoración Profesional GOAT** (0-10): Asignada por usuarios con rol GOAT o Administrador
- **Valoración de Comunidad** (1-5): Calculada automáticamente como promedio de todas las valoraciones de usuarios normales

## Arquitectura

### Backend

#### Modelo `Game` (games/models.py)
```python
# Valoración profesional (solo GOAT/Admin)
professional_rating = DecimalField(0-10, null=True)
professional_review = TextField(blank=True)

# Valoración de comunidad (calculada automáticamente)
community_rating = DecimalField(0-5, default=0.0)
```

#### Endpoints

**POST `/api/games/{slug}/set_professional_rating/`**
- Requiere autenticación y permisos GOAT/Admin
- Establece la valoración profesional y reseña
- Body: `{ "rating": 8.5, "review": "Análisis profesional..." }`

**POST `/api/games/{slug}/rate/`**
- Requiere autenticación (usuarios normales)
- Actualiza la valoración del usuario (1-5)
- Recalcula automáticamente `community_rating`
- Retorna: `{ "rating": 4, "community_rating": 4.2, "professional_rating": 8.5, "total_ratings": 127 }`

#### Serializers (games/serializers.py)

**GameListSerializer**
- Incluye: `professional_rating`, `community_rating`, `is_favorite`

**GameDetailSerializer**
- Todos los campos del juego
- `can_edit_professional`: booleano que indica si el usuario actual puede editar la valoración profesional
- `user_rating`: valoración actual del usuario autenticado
- `is_favorite`: si está en favoritos del usuario

### Frontend

#### Componentes

**DualRating.vue**
- Muestra ambas valoraciones lado a lado (versión completa)
- Iconos distintivos: estrella dorada (GOAT) y usuarios (comunidad)
- Tooltips informativos
- Uso: En detalles de juego

**DualRatingCompact.vue**
- Versión compacta para tarjetas de juegos
- Badges apilados verticalmente
- Mismo estilo visual pero más pequeño

#### Vistas

**GameDetailView.vue**
- Muestra `DualRating` en la sección hero
- Formulario separado para valoración profesional (solo visible para GOAT/Admin)
- Formulario de valoración de comunidad (estrellas 1-5) para usuarios normales
- Muestra reseña profesional en sidebar si existe

**GameFormView.vue**
- Sección de valoración profesional solo visible para GOAT/Admin
- Permite editar/crear valoración profesional al crear/editar juego
- Campos: `professional_rating` (0-10) y `professional_review` (textarea)

**GameCard.vue**
- Badges de valoración en esquina superior derecha
- Badge dorado para valoración GOAT (si existe)
- Badge azul para valoración comunidad (si > 0)

## Permisos y Roles

### Usuario Normal
- Puede votar juegos (1-5 estrellas)
- Ve ambas valoraciones
- NO puede establecer valoración profesional

### Usuario GOAT / Administrador
- Puede votar como usuario normal
- Puede establecer/editar valoración profesional (0-10)
- Puede escribir reseña profesional
- Acceso a formulario especial en GameDetailView y GameFormView

## Estilos Visuales

### Colores
- **GOAT Rating**: Gradiente amber/orange con borde dorado
  - Color texto: `text-amber-400`
  - Fondo: `from-amber-500/10 to-orange-500/10`
  - Borde: `border-amber-500/30`

- **Community Rating**: Tema azul con fondo oscuro
  - Color texto: `text-blue-400`
  - Fondo: `bg-dark-800/50`
  - Borde: `border-dark-700`

### Iconos
- GOAT: Estrella dorada con texto "GOAT"
- Comunidad: Grupo de usuarios con texto "Users"

## Flujo de Datos

### Creación de Valoración Profesional
1. Usuario GOAT/Admin accede a detalle de juego o formulario de edición
2. Ingresa rating (0-10) y reseña opcional
3. POST a `/games/{slug}/set_professional_rating/`
4. Backend valida permisos y rango (0-10)
5. Actualiza `professional_rating` y `professional_review`
6. Frontend actualiza vista automáticamente

### Creación de Valoración de Comunidad
1. Usuario normal accede a detalle de juego
2. Selecciona estrellas (1-5)
3. POST a `/games/{slug}/rate/`
4. Backend crea/actualiza `GameRating` del usuario
5. Backend recalcula `community_rating` (promedio de todos los ratings)
6. Actualiza también campo legacy `rating` para compatibilidad
7. Frontend actualiza vista con nuevo promedio

## Validaciones

### Backend
- Valoración profesional: debe estar entre 0 y 10
- Valoración comunidad: debe estar entre 1 y 5
- Solo usuarios con `can_edit_content=True` pueden establecer valoración profesional
- Todos los usuarios autenticados pueden valorar (comunidad)

### Frontend
- Input de valoración profesional tiene min="0" max="10" step="0.1"
- Componente StarRating solo permite 1-5 estrellas
- Botones deshabilitados si valores fuera de rango

## Próximas Mejoras Sugeridas

1. **Sistema de Logros**
   - Logro por votar X juegos
   - Logro por escribir X reseñas profesionales (GOAT)

2. **Estadísticas**
   - Mostrar distribución de votos (cuántos 5★, 4★, etc.)
   - Mostrar tendencias de valoración en el tiempo

3. **Filtros y Ordenamiento**
   - Filtrar juegos por valoración GOAT
   - Filtrar por valoración comunidad
   - Ordenar por cualquiera de las dos

4. **Notificaciones**
   - Notificar a usuarios cuando un GOAT valora un juego de sus favoritos
   - Notificar cuando su juego favorito recibe valoración alta

5. **Historial**
   - Guardar historial de cambios en valoraciones profesionales
   - Mostrar evolución de valoración de comunidad
