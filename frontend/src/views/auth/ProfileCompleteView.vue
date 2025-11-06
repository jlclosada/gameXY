<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950 flex items-center justify-center px-4 py-12">
    <div class="card max-w-3xl w-full p-8 shadow-2xl">
      <div class="text-center mb-8">
        <div class="inline-block p-3 bg-primary-600/20 rounded-full mb-4">
          <svg class="w-12 h-12 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
        </div>
        <h1 class="text-4xl font-display font-bold mb-2 bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">
          ¡Bienvenido a GameXY!
        </h1>
        <p class="text-dark-400 text-lg">Completa tu perfil para comenzar tu aventura gaming</p>
      </div>

      <form @submit.prevent="handleCompleteProfile" class="space-y-6">
        <div v-if="error" class="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <!-- Información Personal (Requerida) -->
        <div class="bg-dark-800/50 p-6 rounded-lg border border-dark-700">
          <h2 class="text-xl font-display font-bold mb-4 flex items-center gap-2">
            <span class="text-primary-400">👤</span>
            Información Personal
          </h2>

          <div class="space-y-4">
            <!-- Username -->
            <div>
              <label for="username" class="block text-sm font-medium mb-2">
                Nombre de Usuario <span class="text-red-400">*</span>
              </label>
              <input
                id="username"
                v-model="form.username"
                type="text"
                required
                pattern="[a-zA-Z0-9_]{3,20}"
                class="input"
                placeholder="Ej: gamer_pro"
                @input="validateUsername"
              >
              <p class="text-xs text-dark-400 mt-1">
                3-20 caracteres. Solo letras, números y guiones bajos.
              </p>
              <p v-if="usernameError" class="text-xs text-red-400 mt-1">
                {{ usernameError }}
              </p>
              <p v-else-if="usernameAvailable && form.username.length >= 3" class="text-xs text-green-400 mt-1">
                ✓ Nombre de usuario disponible
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Nombre -->
              <div>
                <label for="first_name" class="block text-sm font-medium mb-2">
                  Nombre <span class="text-red-400">*</span>
                </label>
                <input
                  id="first_name"
                  v-model="form.first_name"
                  type="text"
                  required
                  class="input"
                  placeholder="Tu nombre"
                >
              </div>

              <!-- Apellidos -->
              <div>
                <label for="last_name" class="block text-sm font-medium mb-2">
                  Apellidos <span class="text-red-400">*</span>
                </label>
                <input
                  id="last_name"
                  v-model="form.last_name"
                  type="text"
                  required
                  class="input"
                  placeholder="Tus apellidos"
                >
              </div>

              <!-- Fecha de Nacimiento -->
              <div>
                <label for="birth_date" class="block text-sm font-medium mb-2">
                  Fecha de Nacimiento <span class="text-red-400">*</span>
                </label>
                <input
                  id="birth_date"
                  v-model="form.birth_date"
                  type="date"
                  required
                  :max="maxDate"
                  class="input cursor-pointer"
                >
                <p v-if="calculatedAge" class="text-xs text-dark-400 mt-1">
                  Edad: {{ calculatedAge }} años
                </p>
              </div>

              <!-- Género -->
              <div>
                <label for="gender" class="block text-sm font-medium mb-2">
                  Género <span class="text-dark-500">(opcional)</span>
                </label>
                <select
                  id="gender"
                  v-model="form.gender"
                  class="input"
                >
                  <option value="">Selecciona...</option>
                  <option value="male">Masculino</option>
                  <option value="female">Femenino</option>
                  <option value="other">Otro</option>
                  <option value="prefer_not_to_say">Prefiero no decir</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Ubicación (Opcional) -->
        <div class="bg-dark-800/50 p-6 rounded-lg border border-dark-700">
          <h2 class="text-xl font-display font-bold mb-4 flex items-center gap-2">
            <span class="text-primary-400">🌍</span>
            Ubicación
          </h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- País -->
            <div>
              <label for="country" class="block text-sm font-medium mb-2">
                País <span class="text-dark-500">(opcional)</span>
              </label>
              <input
                id="country"
                v-model="form.country"
                type="text"
                class="input"
                placeholder="Ej: España, México, Argentina..."
              >
            </div>

            <!-- Ciudad -->
            <div>
              <label for="city" class="block text-sm font-medium mb-2">
                Ciudad <span class="text-dark-500">(opcional)</span>
              </label>
              <input
                id="city"
                v-model="form.city"
                type="text"
                class="input"
                placeholder="Tu ciudad"
              >
            </div>
          </div>
        </div>

        <!-- Avatar y Bio -->
        <div class="bg-dark-800/50 p-6 rounded-lg border border-dark-700">
          <h2 class="text-xl font-display font-bold mb-4 flex items-center gap-2">
            <span class="text-primary-400">✨</span>
            Personaliza tu Perfil
          </h2>

          <!-- Avatar -->
          <div class="mb-6">
            <label class="block text-sm font-medium mb-2">Foto de Perfil <span class="text-dark-500">(opcional)</span></label>
            <div class="flex items-center gap-4">
              <div class="w-24 h-24 rounded-full bg-dark-700 flex items-center justify-center overflow-hidden border-2 border-dark-600">
                <img v-if="previewAvatar" :src="previewAvatar" alt="Avatar" class="w-full h-full object-cover" />
                <svg v-else class="w-12 h-12 text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
              </div>
              <div class="flex-1">
                <input
                  type="file"
                  ref="avatarInput"
                  @change="handleAvatarChange"
                  accept="image/*"
                  class="hidden"
                >
                <button
                  type="button"
                  @click="$refs.avatarInput.click()"
                  class="btn btn-secondary"
                >
                  <svg class="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  Seleccionar Imagen
                </button>
                <p class="text-xs text-dark-400 mt-1">JPG, PNG o GIF (máx. 2MB)</p>
              </div>
            </div>
          </div>

          <!-- Bio -->
          <div>
            <label for="bio" class="block text-sm font-medium mb-2">
              Sobre ti <span class="text-dark-500">(opcional)</span>
            </label>
            <textarea
              id="bio"
              v-model="form.bio"
              rows="4"
              maxlength="500"
              class="input resize-none"
              placeholder="Cuéntanos un poco sobre ti, tus juegos favoritos, tu estilo de juego..."
            ></textarea>
            <p class="text-xs text-dark-400 mt-1 text-right">{{ form.bio.length }}/500</p>
          </div>
        </div>

        <!-- Preferencias Gaming -->
        <div class="bg-dark-800/50 p-6 rounded-lg border border-dark-700">
          <h2 class="text-xl font-display font-bold mb-4 flex items-center gap-2">
            <span class="text-primary-400">🎮</span>
            Preferencias Gaming
          </h2>

          <!-- Géneros Favoritos -->
          <div class="mb-6">
            <label class="block text-sm font-medium mb-3">
              Géneros Favoritos <span class="text-red-400">*</span>
            </label>
            <p class="text-sm text-dark-400 mb-3">Selecciona al menos un género (máximo 5)</p>

            <div v-if="loadingGenres" class="text-center py-4">
              <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
            </div>

            <div v-else class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <button
                v-for="genre in availableGenres"
                :key="genre.value"
                type="button"
                @click="toggleGenre(genre.value)"
                class="px-4 py-3 rounded-lg border-2 transition text-left"
                :class="form.favorite_genres.includes(genre.value)
                  ? 'border-primary-500 bg-primary-600/20 text-primary-300'
                  : 'border-dark-600 bg-dark-700/50 text-dark-300 hover:border-dark-500'"
              >
                <div class="text-lg mb-1">{{ genre.icon }}</div>
                <div class="text-sm font-medium">{{ genre.label }}</div>
              </button>
            </div>

            <p v-if="form.favorite_genres.length > 0" class="text-xs text-primary-400 mt-2">
              {{ form.favorite_genres.length }}/5 géneros seleccionados
            </p>
          </div>

          <!-- Juegos Favoritos -->
          <div>
            <label class="block text-sm font-medium mb-2">
              Juegos Favoritos <span class="text-dark-500">(opcional)</span>
            </label>
            <p class="text-sm text-dark-400 mb-3">Añade hasta 10 juegos que te gusten</p>

            <!-- Búsqueda de juegos -->
            <div class="relative mb-3">
              <input
                v-model="gameSearchQuery"
                @input="searchGames"
                type="text"
                class="input"
                placeholder="Buscar juegos..."
              >
              <div
                v-if="searchResults.length > 0 && gameSearchQuery"
                class="absolute z-10 w-full mt-1 bg-dark-800 border border-dark-700 rounded-lg shadow-xl max-h-60 overflow-y-auto"
              >
                <button
                  v-for="game in searchResults"
                  :key="game.id"
                  type="button"
                  @click="addFavoriteGame(game)"
                  :disabled="selectedGames.length >= 10"
                  class="w-full flex items-center gap-3 px-4 py-3 hover:bg-dark-700 transition text-left disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <img
                    v-if="game.cover_image"
                    :src="game.cover_image"
                    :alt="game.title"
                    class="w-10 h-10 rounded object-cover"
                  >
                  <div class="w-10 h-10 bg-dark-700 rounded flex items-center justify-center" v-else>
                    <span class="text-xs">🎮</span>
                  </div>
                  <span>{{ game.title }}</span>
                </button>
              </div>
            </div>

            <!-- Juegos seleccionados -->
            <div v-if="selectedGames.length > 0" class="flex flex-wrap gap-2">
              <div
                v-for="game in selectedGames"
                :key="game.id"
                class="flex items-center gap-2 px-3 py-2 bg-dark-700 rounded-lg"
              >
                <span class="text-sm">{{ game.title }}</span>
                <button
                  type="button"
                  @click="removeFavoriteGame(game.id)"
                  class="text-dark-400 hover:text-red-400 transition"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Botones -->
        <div class="flex gap-3 pt-6">
          <button
            type="button"
            @click="skipProfile"
            class="btn btn-secondary flex-1 py-3"
          >
            <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7"/>
            </svg>
            Omitir por ahora
          </button>
          <button
            type="button"
            :disabled="loading || !isFormValid"
            class="btn btn-primary flex-1 py-3"
            @click="handleCompleteProfile"
          >
            <svg v-if="!loading" class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            <div v-else class="inline-block w-5 h-5 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            {{ loading ? 'Guardando...' : 'Completar Perfil' }}
          </button>
        </div>

        <p class="text-center text-dark-500 text-sm mt-4">
          <span class="text-red-400">*</span> Campos obligatorios
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  first_name: '',
  last_name: '',
  birth_date: '',
  gender: '',
  country: '',
  city: '',
  bio: '',
  avatar: null,
  favorite_genres: []
})

const selectedGames = ref([])
const gameSearchQuery = ref('')
const searchResults = ref([])
const previewAvatar = ref(null)
const avatarInput = ref(null)
const loading = ref(false)
const loadingGenres = ref(false)
const error = ref(null)
const availableGenres = ref([])
const usernameError = ref('')
const usernameAvailable = ref(false)

let searchTimeout = null
let usernameCheckTimeout = null

// Fecha máxima (13 años atrás)
const maxDate = computed(() => {
  const date = new Date()
  date.setFullYear(date.getFullYear() - 13)
  return date.toISOString().split('T')[0]
})

// Calcular edad
const calculatedAge = computed(() => {
  if (!form.value.birth_date) return null
  const today = new Date()
  const birthDate = new Date(form.value.birth_date)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  return age
})

// Validación del formulario
const isFormValid = computed(() => {
  return form.value.username.trim() !== '' &&
         form.value.username.length >= 3 &&
         !usernameError.value &&
         form.value.first_name.trim() !== '' &&
         form.value.last_name.trim() !== '' &&
         form.value.birth_date !== '' &&
         form.value.favorite_genres.length > 0
})

// Cargar géneros disponibles desde el backend
async function loadGenres() {
  loadingGenres.value = true
  try {
    const response = await api.get('/games/genres/')
    // Mapear los géneros del backend al formato que usa el frontend
    availableGenres.value = response.data.map(genre => ({
      value: genre.slug,
      label: genre.name,
      icon: genre.icon || '🎮'
    }))
  } catch (err) {
    console.error('Error loading genres:', err)
    // Fallback a géneros por defecto si falla la carga
    availableGenres.value = [
      { value: 'action', label: 'Acción', icon: '💥' },
      { value: 'adventure', label: 'Aventura', icon: '🏝️' },
      { value: 'rpg', label: 'RPG', icon: '⚔️' },
      { value: 'strategy', label: 'Estrategia', icon: '🧠' },
      { value: 'shooter', label: 'Shooter', icon: '🔫' },
    ]
  } finally {
    loadingGenres.value = false
  }
}

function toggleGenre(genreValue) {
  const index = form.value.favorite_genres.indexOf(genreValue)
  if (index > -1) {
    form.value.favorite_genres.splice(index, 1)
  } else {
    if (form.value.favorite_genres.length < 5) {
      form.value.favorite_genres.push(genreValue)
    }
  }
}

async function validateUsername() {
  const username = form.value.username

  // Reset estados
  usernameError.value = ''
  usernameAvailable.value = false

  if (!username || username.length < 3) {
    return
  }

  // Validar formato
  const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/
  if (!usernameRegex.test(username)) {
    usernameError.value = 'Solo letras, números y guiones bajos (3-20 caracteres)'
    return
  }

  // Por ahora marcar como disponible (el backend validará en el submit)
  usernameAvailable.value = true

  // Comentado temporalmente hasta que el backend soporte esta búsqueda
  /*
  clearTimeout(usernameCheckTimeout)
  usernameCheckTimeout = setTimeout(async () => {
    try {
      const response = await api.get(`/auth/users/?username=${username}`)
      if (response.data && response.data.length > 0) {
        usernameError.value = 'Este nombre de usuario ya está en uso'
      } else {
        usernameAvailable.value = true
      }
    } catch (err) {
      usernameAvailable.value = true
    }
  }, 500)
  */
}

async function searchGames() {
  if (!gameSearchQuery.value || gameSearchQuery.value.length < 2) {
    searchResults.value = []
    return
  }

  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    try {
      const response = await api.get('/games/', {
        params: { search: gameSearchQuery.value }
      })
      searchResults.value = response.data.results || response.data
    } catch (err) {
      console.error('Error searching games:', err)
    }
  }, 300)
}

function addFavoriteGame(game) {
  if (!selectedGames.value.find(g => g.id === game.id)) {
    selectedGames.value.push(game)
  }
  gameSearchQuery.value = ''
  searchResults.value = []
}

function removeFavoriteGame(gameId) {
  selectedGames.value = selectedGames.value.filter(g => g.id !== gameId)
}

function handleAvatarChange(event) {
  const file = event.target.files[0]
  if (!file) return

  // Validar tamaño (2MB)
  if (file.size > 2 * 1024 * 1024) {
    error.value = 'La imagen no puede superar los 2MB'
    return
  }

  form.value.avatar = file

  // Preview
  const reader = new FileReader()
  reader.onload = (e) => {
    previewAvatar.value = e.target.result
  }
  reader.readAsDataURL(file)
}

async function handleCompleteProfile() {
  console.log('handleCompleteProfile called')
  console.log('Form values:', form.value)
  console.log('isFormValid:', isFormValid.value)

  if (!isFormValid.value) {
    error.value = 'Por favor completa todos los campos obligatorios'
    console.error('Form is not valid')
    return
  }

  loading.value = true
  error.value = null

  try {
    // Obtener credenciales guardadas
    const email = sessionStorage.getItem('pendingEmail')
    const password = sessionStorage.getItem('pendingPassword')

    if (!email || !password) {
      error.value = 'Sesión expirada. Por favor, regresa al registro.'
      return
    }

    const formData = new FormData()

    // Credenciales para autenticación
    formData.append('email', email)
    formData.append('password', password)

    // Campos obligatorios
    formData.append('username', form.value.username)
    formData.append('first_name', form.value.first_name)
    formData.append('last_name', form.value.last_name)
    formData.append('birth_date', form.value.birth_date)

    // Campos opcionales
    if (form.value.gender) {
      formData.append('gender', form.value.gender)
    }
    if (form.value.country) {
      formData.append('country', form.value.country)
    }
    if (form.value.city) {
      formData.append('city', form.value.city)
    }
    if (form.value.bio) {
      formData.append('bio', form.value.bio)
    }
    if (form.value.avatar) {
      formData.append('avatar', form.value.avatar)
    }

    // Géneros favoritos (JSON)
    formData.append('favorite_genres', JSON.stringify(form.value.favorite_genres))

    // Agregar juegos favoritos
    if (selectedGames.value.length > 0) {
      selectedGames.value.forEach(game => {
        formData.append('favorite_games', game.id)
      })
    }

    // Enviar datos para completar perfil (sin interceptor de autenticación)
    const apiURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await axios.post(`${apiURL}/api/auth/users/complete_profile/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // El backend devolverá tokens y datos del usuario
    //otrooo
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      authStore.user = response.data.user

      // Limpiar credenciales temporales
      sessionStorage.removeItem('pendingEmail')
      sessionStorage.removeItem('pendingPassword')

      router.push('/')
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Error al completar el perfil'
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } finally {
    loading.value = false
  }
}

function skipProfile() {
  router.push('/')
}

onMounted(async () => {
  console.log('ProfileCompleteView mounted')

  // Verificar si hay credenciales pendientes
  const pendingEmail = sessionStorage.getItem('pendingEmail')
  if (!pendingEmail && !authStore.user) {
    console.log('No pending registration, redirecting to register')
    router.push('/register')
    return
  }

  // Si el usuario ya está autenticado y completó su perfil, redirigir al home
  if (authStore.user?.profile_completed) {
    console.log('Profile already completed, redirecting to home')
    router.push('/')
    return
  }

  console.log('Loading genres...')
  // Cargar géneros disponibles
  await loadGenres()
  console.log('Genres loaded:', availableGenres.value.length)
})
</script>
