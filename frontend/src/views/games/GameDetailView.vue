<template>
  <div class="relative">
    <!-- Hero Section con Banner -->
    <div v-if="loading" class="animate-pulse">
      <div class="h-[500px] bg-dark-700 mb-8"></div>
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="h-8 bg-dark-700 rounded w-1/2 mb-4"></div>
        <div class="h-32 bg-dark-700 rounded"></div>
      </div>
    </div>
    
    <div v-else-if="error" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="card p-8 text-center">
        <p class="text-red-400 mb-4">{{ error }}</p>
        <button @click="$router.push('/games')" class="btn btn-primary">Volver a juegos</button>
      </div>
    </div>

    <div v-else-if="game">
      <!-- Hero Banner -->
      <div class="relative h-[400px] md:h-[500px] overflow-hidden">
        <div 
          v-if="game.banner_image" 
          class="absolute inset-0 bg-cover bg-center transform scale-105"
          :style="{ backgroundImage: `url(${game.banner_image})` }"
        >
          <div class="absolute inset-0 bg-gradient-to-b from-dark-950/60 via-dark-950/80 to-dark-950"></div>
        </div>
        <div v-else class="absolute inset-0 bg-gradient-to-br from-primary-900/20 to-dark-950"></div>
        
        <!-- Content over banner -->
        <div class="relative h-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col justify-end pb-8">
          <div class="flex items-end gap-6">
            <!-- Cover Image -->
            <div v-if="game.cover_image" class="hidden md:block w-48 h-64 rounded-lg overflow-hidden shadow-2xl border-2 border-dark-700 flex-shrink-0">
              <img :src="game.cover_image" :alt="game.title" class="w-full h-full object-cover">
            </div>
            
            <!-- Title and Quick Info -->
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-3">
                <span 
                  v-for="category in game.categories.slice(0, 2)" 
                  :key="category.id"
                  class="badge badge-primary text-xs"
                >
                  {{ category.name }}
                </span>
              </div>
              <h1 class="text-4xl md:text-5xl font-display font-bold mb-3 text-white drop-shadow-lg">{{ game.title }}</h1>
              
              <!-- Valoraciones -->
              <div class="flex items-center gap-3">
                <!-- Valoración Oficial GOAT -->
                <div v-if="game.official_rating !== null && game.official_rating !== undefined" class="bg-gradient-to-br from-amber-500/10 to-orange-500/10 border border-amber-500/30 rounded-lg px-4 py-2">
                  <div class="flex flex-col items-center">
                    <div class="text-3xl font-bold text-amber-400">{{ Number(game.official_rating).toFixed(1) }}</div>
                    <span class="text-[10px] uppercase tracking-wider text-amber-400/70 font-medium">Nota Oficial</span>
                  </div>
                </div>

                <!-- Valoración Comunidad -->
                <div class="bg-dark-800/50 border border-dark-700 rounded-lg px-3 py-2">
                  <div class="flex items-center gap-2">
                    <RatingBar
                      :value="Number(game.community_rating)"
                      icon="heart"
                      :size="14"
                      activeColor="#ef4444"
                      inactiveColor="#374151"
                    />
                    <span class="text-lg font-bold text-red-500">{{ Number(game.community_rating).toFixed(1) }}</span>
                  </div>
                  <span class="text-[10px] uppercase tracking-wider text-gray-500 font-medium">{{ game.ratings_count || 0 }} votos</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Main Column -->
          <div class="lg:col-span-2 space-y-8">
            <!-- Description -->
            <div class="card p-6">
              <h2 class="text-xl font-display font-bold mb-4">Acerca del juego</h2>
              <p class="text-gray-300 leading-relaxed">{{ game.description }}</p>
            </div>

            <!-- Valoración Oficial (solo GOAT/Admin) -->
            <div v-if="game.can_edit_official" class="card p-6">
              <h2 class="text-xl font-display font-bold mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                Valoración Oficial de la Plataforma
              </h2>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-300 mb-2">Nota (0-10)</label>
                  <input
                    v-model.number="officialRatingInput"
                    type="number"
                    min="0"
                    max="10"
                    step="0.1"
                    class="w-full bg-dark-800 border border-dark-700 rounded-lg px-4 py-2 text-white focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
                    placeholder="Ej: 8.5"
                  />
                  <p class="text-xs text-gray-400 mt-1">Nota de 0 a 10 (puedes usar decimales)</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-300 mb-2">Reseña oficial</label>
                  <textarea
                    v-model="officialReviewInput"
                    rows="4"
                    class="w-full bg-dark-800 border border-dark-700 rounded-lg px-4 py-2 text-white focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
                    placeholder="Escribe la reseña oficial del equipo..."
                  ></textarea>
                </div>
                <button
                  @click="handleOfficialRating"
                  :disabled="officialRatingInput === null || officialRatingInput === undefined || officialRatingInput < 0 || officialRatingInput > 10"
                  class="btn btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Publicar valoración oficial
                </button>
              </div>
            </div>

            <!-- Valoración de Comunidad -->
            <div v-if="authStore.isAuthenticated" class="card p-6">
              <h2 class="text-xl font-display font-bold mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
                </svg>
                Tu valoración de comunidad
              </h2>
              <div class="flex flex-col items-center py-6">
                <p class="text-gray-400 text-sm mb-4">¿Qué te pareció este juego?</p>
                <div class="flex items-center gap-2">
                  <button
                    v-for="i in 5"
                    :key="i"
                    @click="handleRate(i)"
                    class="transition-all transform hover:scale-110"
                  >
                    <svg class="w-10 h-10" :class="i <= (game.user_rating || 0) ? 'text-red-500' : 'text-gray-600 hover:text-red-400'" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
                <p v-if="game.user_rating" class="text-sm text-gray-400 mt-3">Tu valoración: {{ game.user_rating }}/5</p>
              </div>
            </div>
            <div v-else class="card p-6 text-center">
              <p class="text-gray-400 mb-4">Inicia sesión para valorar este juego</p>
              <RouterLink to="/login" class="btn btn-primary">Iniciar sesión</RouterLink>
            </div>

            <!-- Comentarios -->
            <CommentSection
              resource-type="game"
              :resource-id="game.id"
            />
          </div>

          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Info del juego -->
            <div class="card p-6">
              <h3 class="font-display font-bold mb-4">Información</h3>
              <div class="space-y-4">
                <div v-if="game.developer">
                  <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Desarrollador</p>
                  <p class="text-gray-200 font-medium">{{ game.developer }}</p>
                </div>
                <div v-if="game.publisher">
                  <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Distribuidor</p>
                  <p class="text-gray-200 font-medium">{{ game.publisher }}</p>
                </div>
                <div v-if="game.release_date">
                  <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Lanzamiento</p>
                  <p class="text-gray-200 font-medium">{{ formatReleaseDate(game.release_date) }}</p>
                </div>
                <div v-if="game.genre">
                  <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Género</p>
                  <p class="text-gray-200 font-medium">{{ formatGenre(game.genre) }}</p>
                </div>
                <div v-if="game.platforms && game.platforms.length > 0">
                  <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Plataformas</p>
                  <div class="flex flex-wrap gap-2 mt-2">
                    <span 
                      v-for="platform in game.platforms" 
                      :key="platform"
                      class="text-xs bg-dark-800 text-gray-300 px-2 py-1 rounded border border-dark-700"
                    >
                      {{ platform }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Reseña Oficial -->
            <div v-if="game.official_review" class="card p-6">
              <h3 class="font-display font-bold mb-3 flex items-center gap-2">
                <svg class="w-4 h-4 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                Reseña Oficial
              </h3>
              <p class="text-gray-300 text-sm leading-relaxed">{{ game.official_review }}</p>
            </div>

            <!-- Enlaces externos -->
            <div v-if="game.website_url || game.steam_url" class="card p-6">
              <h3 class="font-display font-bold mb-4">Enlaces</h3>
              <div class="space-y-2">
                <a 
                  v-if="game.website_url" 
                  :href="game.website_url" 
                  target="_blank"
                  class="flex items-center gap-2 text-primary-400 hover:text-primary-300 transition text-sm"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.03 11H4.083a6.004 6.004 0 002.783 4.118z" clip-rule="evenodd"/>
                  </svg>
                  <span>Sitio oficial</span>
                </a>
                <a 
                  v-if="game.steam_url" 
                  :href="game.steam_url" 
                  target="_blank"
                  class="flex items-center gap-2 text-primary-400 hover:text-primary-300 transition text-sm"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z"/>
                  </svg>
                  <span>Ver en Steam</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import CommentSection from '@/components/comments/CommentSection.vue'
import RatingBar from '@/components/common/RatingBar.vue'

const route = useRoute()
const authStore = useAuthStore()
const game = ref(null)
const loading = ref(true)
const error = ref(null)
const officialRatingInput = ref(null)
const officialReviewInput = ref('')

const formatReleaseDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatGenre = (genre) => {
  const genreMap = {
    'action': 'Acción',
    'adventure': 'Aventura',
    'rpg': 'RPG',
    'strategy': 'Estrategia',
    'shooter': 'Shooter',
    'sports': 'Deportes',
    'racing': 'Carreras',
    'fighting': 'Pelea',
    'puzzle': 'Puzzle',
    'simulation': 'Simulación',
    'horror': 'Terror',
    'platform': 'Plataformas',
    'mmorpg': 'MMORPG',
    'moba': 'MOBA',
    'battle_royale': 'Battle Royale'
  }
  return genreMap[genre] || genre
}

const handleRate = async (rating) => {
  try {
    const response = await api.post(`/games/${game.value.slug}/rate/`, { rating })
    game.value.community_rating = response.data.community_rating
    game.value.user_rating = response.data.rating
    game.value.ratings_count = response.data.total_ratings
  } catch (error) {
    console.error('Error rating game:', error)
    alert('Error al valorar el juego')
  }
}

const handleOfficialRating = async () => {
  if (officialRatingInput.value === null || officialRatingInput.value === undefined || officialRatingInput.value < 0 || officialRatingInput.value > 10) {
    alert('La valoración debe estar entre 0 y 10')
    return
  }
  
  try {
    const response = await api.post(`/games/${game.value.slug}/set_official_rating/`, {
      rating: officialRatingInput.value,
      review: officialReviewInput.value
    })
    game.value.official_rating = response.data.official_rating
    game.value.official_review = response.data.official_review
    alert('Valoración oficial publicada correctamente')
  } catch (error) {
    console.error('Error setting official rating:', error)
    alert(error.response?.data?.error || 'Error al publicar la valoración oficial')
  }
}

onMounted(async () => {
  try {
    console.log('Loading game:', route.params.slug)
    const response = await api.get(`/games/${route.params.slug}/`)
    console.log('Game data:', response.data)
    game.value = response.data
    
    // Pre-cargar valores de valoración oficial si existen
    if (game.value.official_rating) {
      officialRatingInput.value = game.value.official_rating
    }
    if (game.value.official_review) {
      officialReviewInput.value = game.value.official_review
    }
  } catch (err) {
    console.error('Error loading game:', err)
    error.value = err.response?.data?.detail || 'Error al cargar el juego'
  } finally {
    loading.value = false
  }
})
</script>
