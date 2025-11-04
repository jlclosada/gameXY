<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-display font-bold mb-3">
        ❤️ Mis Juegos Favoritos
      </h1>
      <p class="text-gray-400">Todos los juegos que has marcado como favoritos</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      <div v-for="n in 10" :key="n" class="card-elevated animate-pulse">
        <div class="aspect-[2/3] bg-dark-700"></div>
        <div class="p-3 space-y-2">
          <div class="h-4 bg-dark-700 rounded"></div>
          <div class="h-3 bg-dark-700 rounded w-2/3"></div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="games.length === 0" class="card p-12 text-center">
      <div class="text-6xl mb-4">🎮</div>
      <h2 class="text-2xl font-display font-bold mb-3">No tienes juegos favoritos</h2>
      <p class="text-gray-400 mb-6">Explora el catálogo de juegos y marca tus favoritos para tenerlos siempre a mano</p>
      <RouterLink to="/games" class="btn btn-primary inline-flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        Explorar Juegos
      </RouterLink>
    </div>

    <!-- Games Grid -->
    <div v-else class="space-y-6">
      <div class="flex items-center justify-between">
        <p class="text-gray-400">{{ games.length }} {{ games.length === 1 ? 'juego favorito' : 'juegos favoritos' }}</p>
      </div>
      
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        <div v-for="game in games" :key="game.id" class="card-elevated group relative">
          <RouterLink :to="`/games/${game.slug}`" class="block">
            <!-- Cover Image -->
            <div class="aspect-[2/3] relative overflow-hidden bg-dark-850">
              <img 
                v-if="game.cover_image" 
                :src="game.cover_image" 
                :alt="game.title"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              >
              <div v-else class="w-full h-full flex items-center justify-center">
                <svg class="w-12 h-12 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z"/>
                </svg>
              </div>
              
              <!-- Rating Badge -->
              <div v-if="Number(game.rating) > 0" class="absolute top-2 right-2 bg-dark-900/90 backdrop-blur-sm border border-dark-700 px-2 py-1 rounded-lg flex items-center gap-1">
                <svg class="w-3 h-3 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <span class="text-xs font-bold text-gray-100">{{ Number(game.rating).toFixed(1) }}</span>
              </div>
              
              <!-- Overlay gradient -->
              <div class="absolute inset-0 bg-gradient-to-t from-dark-900 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            
            <!-- Content -->
            <div class="p-3">
              <h3 class="font-display font-semibold text-sm mb-2 line-clamp-2 group-hover:text-primary-400 transition-colors">
                {{ game.title }}
              </h3>
              <div v-if="game.categories && game.categories.length > 0" class="flex flex-wrap gap-1">
                <span 
                  v-for="category in game.categories.slice(0, 2)" 
                  :key="category.id"
                  class="text-xs bg-dark-850 text-gray-400 px-2 py-0.5 rounded border border-dark-800"
                >
                  {{ category.name }}
                </span>
              </div>
              <div v-else class="h-5"></div>
            </div>
          </RouterLink>
          
          <!-- Remove Favorite Button -->
          <button
            @click.prevent="removeFavorite(game)"
            class="absolute top-2 left-2 bg-dark-900/90 backdrop-blur-sm border border-dark-700 p-2 rounded-lg hover:bg-red-500/20 hover:border-red-500 transition-all z-10"
            title="Quitar de favoritos"
          >
            <svg class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 24 24">
              <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/api/axios'

const games = ref([])
const loading = ref(true)

const loadFavoriteGames = async () => {
  loading.value = true
  try {
    const response = await api.get('/auth/users/me/')
    const user = response.data
    
    // Cargar detalles de los juegos favoritos
    if (user.favorite_games && user.favorite_games.length > 0) {
      const gamesResponse = await api.get('/games/', {
        params: {
          id__in: user.favorite_games.join(',')
        }
      })
      games.value = gamesResponse.data.results || gamesResponse.data
    }
  } catch (error) {
    console.error('Error loading favorite games:', error)
  } finally {
    loading.value = false
  }
}

const removeFavorite = async (game) => {
  try {
    await api.post(`/games/${game.slug}/toggle_favorite/`)
    games.value = games.value.filter(g => g.id !== game.id)
  } catch (error) {
    console.error('Error removing favorite:', error)
  }
}

onMounted(() => {
  loadFavoriteGames()
})
</script>
