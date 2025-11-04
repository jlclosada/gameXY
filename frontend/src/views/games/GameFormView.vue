<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="card p-8">
      <h1 class="text-3xl font-display font-bold mb-8">
        {{ isEdit ? 'Editar Juego' : 'Añadir Nuevo Juego' }}
      </h1>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Título -->
        <div>
          <label class="block text-sm font-medium mb-2">Título del Juego *</label>
          <input v-model="form.title" type="text" required class="input" placeholder="Ej: The Legend of Zelda">
        </div>

        <!-- Slug -->
        <div>
          <label class="block text-sm font-medium mb-2">Slug (URL) *</label>
          <input v-model="form.slug" type="text" required class="input" placeholder="the-legend-of-zelda">
          <p class="text-xs text-dark-400 mt-1">Se usa en la URL del juego (sin espacios, todo minúsculas)</p>
        </div>

        <!-- Descripción -->
        <div>
          <label class="block text-sm font-medium mb-2">Descripción *</label>
          <textarea v-model="form.description" required class="input min-h-[150px]" placeholder="Descripción completa del juego..."></textarea>
        </div>

        <!-- Imágenes -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium mb-2">Imagen de Tarjeta</label>
            <input @change="handleFileChange($event, 'cover_image')" type="file" accept="image/*" class="input">
            <p class="text-xs text-dark-400 mt-1">Imagen vertical para las tarjetas</p>
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Imagen Wallpaper</label>
            <input @change="handleFileChange($event, 'banner_image')" type="file" accept="image/*" class="input">
            <p class="text-xs text-dark-400 mt-1">Imagen horizontal para el banner</p>
          </div>
        </div>

        <!-- Desarrollador y Publisher -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium mb-2">Desarrollador</label>
            <input v-model="form.developer" type="text" class="input" placeholder="Ej: Nintendo">
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Publisher</label>
            <input v-model="form.publisher" type="text" class="input" placeholder="Ej: Nintendo">
          </div>
        </div>

        <!-- Género y Estilo -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium mb-2">Género</label>
            <select v-model="form.genre" class="input">
              <option value="">Selecciona un género</option>
              <option value="action">Acción</option>
              <option value="adventure">Aventura</option>
              <option value="rpg">RPG</option>
              <option value="strategy">Estrategia</option>
              <option value="shooter">Shooter</option>
              <option value="sports">Deportes</option>
              <option value="racing">Carreras</option>
              <option value="fighting">Pelea</option>
              <option value="puzzle">Puzzle</option>
              <option value="simulation">Simulación</option>
              <option value="horror">Terror</option>
              <option value="platform">Plataformas</option>
              <option value="mmorpg">MMORPG</option>
              <option value="moba">MOBA</option>
              <option value="battle_royale">Battle Royale</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Estilo Visual</label>
            <select v-model="form.style" class="input">
              <option value="">Selecciona un estilo</option>
              <option value="2d">2D</option>
              <option value="3d">3D</option>
              <option value="pixel_art">Pixel Art</option>
              <option value="realistic">Realista</option>
              <option value="cartoon">Cartoon</option>
              <option value="anime">Anime</option>
            </select>
          </div>
        </div>

        <!-- Plataformas -->
        <div>
          <label class="block text-sm font-medium mb-2">Plataformas</label>
          <div class="flex flex-wrap gap-3">
            <label v-for="platform in availablePlatforms" :key="platform" class="flex items-center space-x-2">
              <input v-model="form.platforms" type="checkbox" :value="platform" class="rounded">
              <span>{{ platform }}</span>
            </label>
          </div>
        </div>

        <!-- Fecha de lanzamiento -->
        <div>
          <label class="block text-sm font-medium mb-2">Fecha de Lanzamiento</label>
          <input v-model="form.release_date" type="date" class="input">
        </div>

        <!-- Jugadores -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium mb-2">Mínimo de Jugadores</label>
            <input v-model.number="form.min_players" type="number" min="1" class="input" placeholder="1">
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Máximo de Jugadores</label>
            <input v-model.number="form.max_players" type="number" min="1" class="input" placeholder="4">
          </div>
        </div>

        <!-- Opciones -->
        <div class="flex flex-wrap gap-6">
          <label class="flex items-center space-x-2">
            <input v-model="form.multiplayer" type="checkbox" class="rounded">
            <span>Multijugador</span>
          </label>
          <label class="flex items-center space-x-2">
            <input v-model="form.online" type="checkbox" class="rounded">
            <span>Online</span>
          </label>
          <label class="flex items-center space-x-2">
            <input v-model="form.is_featured" type="checkbox" class="rounded">
            <span>Destacado</span>
          </label>
        </div>

        <!-- URLs -->
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">URL del Trailer</label>
            <input v-model="form.trailer_url" type="url" class="input" placeholder="https://youtube.com/...">
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Sitio Web</label>
            <input v-model="form.website_url" type="url" class="input" placeholder="https://...">
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Steam URL</label>
            <input v-model="form.steam_url" type="url" class="input" placeholder="https://store.steampowered.com/...">
          </div>
        </div>

        <!-- Valoración Oficial (solo GOAT/Admin) -->
        <div v-if="authStore.user?.can_edit_content" class="border-t border-dark-700 pt-6">
          <h3 class="text-lg font-display font-bold mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            Valoración Oficial de la Plataforma
          </h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">Nota Oficial (0-10)</label>
              <input 
                v-model.number="form.official_rating" 
                type="number" 
                min="0" 
                max="10" 
                step="0.1" 
                class="input" 
                placeholder="Ej: 8.5"
              >
              <p class="text-xs text-dark-400 mt-1">Nota oficial del equipo (0-10)</p>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">Reseña Oficial</label>
              <textarea 
                v-model="form.official_review" 
                class="input min-h-[120px]" 
                placeholder="Reseña oficial del juego, aspectos destacados, puntos fuertes y débiles..."
              ></textarea>
              <p class="text-xs text-dark-400 mt-1">Reseña oficial del equipo</p>
            </div>
          </div>
        </div>

        <!-- Error mensaje -->
        <div v-if="error" class="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg">
          {{ error }}
        </div>

        <!-- Botones -->
        <div class="flex gap-4">
          <button type="submit" :disabled="loading" class="btn btn-primary flex-1">
            {{ loading ? 'Guardando...' : isEdit ? 'Actualizar Juego' : 'Crear Juego' }}
          </button>
          <button @click="$router.back()" type="button" class="btn btn-secondary">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isEdit = ref(false)
const loading = ref(false)
const error = ref(null)

const availablePlatforms = ['PC', 'PlayStation 5', 'PlayStation 4', 'Xbox Series X/S', 'Xbox One', 'Nintendo Switch', 'Mobile', 'Mac', 'Linux']

const form = ref({
  title: '',
  slug: '',
  description: '',
  developer: '',
  publisher: '',
  genre: '',
  style: '',
  platforms: [],
  release_date: '',
  min_players: null,
  max_players: null,
  multiplayer: false,
  online: false,
  trailer_url: '',
  website_url: '',
  steam_url: '',
  is_featured: false,
  cover_image: null,
  banner_image: null,
  official_rating: null,
  official_review: ''
})

function handleFileChange(event, field) {
  const file = event.target.files[0]
  if (file) {
    form.value[field] = file
  }
}

async function handleSubmit() {
  loading.value = true
  error.value = null

  try {
    const formData = new FormData()
    
    // Añadir todos los campos al FormData
    Object.keys(form.value).forEach(key => {
      if (key === 'platforms') {
        formData.append(key, JSON.stringify(form.value[key]))
      } else if (form.value[key] !== null && form.value[key] !== '') {
        if (key === 'cover_image' || key === 'banner_image') {
          if (form.value[key] instanceof File) {
            formData.append(key, form.value[key])
          }
        } else {
          formData.append(key, form.value[key])
        }
      }
    })

    if (isEdit.value) {
      await api.put(`/games/${route.params.slug}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      await api.post('/games/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }

    router.push('/games')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al guardar el juego'
    console.error('Error:', err.response?.data)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (route.params.slug) {
    isEdit.value = true
    try {
      const response = await api.get(`/games/${route.params.slug}/`)
      Object.assign(form.value, response.data)
    } catch (err) {
      error.value = 'Error al cargar el juego'
    }
  }
})
</script>
