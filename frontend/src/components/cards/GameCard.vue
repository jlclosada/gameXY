<template>
  <div class="group relative block overflow-hidden rounded-xl bg-dark-850 border border-dark-800 hover:border-dark-700 transition-all duration-300 hover:shadow-2xl hover:shadow-primary-500/10">
    <RouterLink :to="`/games/${game.slug}`" class="block">
      <div class="aspect-[1/1.2] relative overflow-hidden bg-dark-850">
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
        
        <!-- Rating Badges -->
        <div class="absolute top-3 right-3 flex flex-col gap-2">
          <!-- Official Rating (nota 0-10) -->
          <div 
            v-if="game.official_rating !== null && game.official_rating !== undefined" 
            class="bg-gradient-to-br from-amber-400 to-amber-600 backdrop-blur-md shadow-xl rounded-full w-10 h-10 flex items-center justify-center border-2 border-white/20"
            title="Valoración Oficial"
          >
            <span class="text-sm font-black text-white">{{ Number(game.official_rating).toFixed(1) }}</span>
          </div>
          
          <!-- Community Rating (corazones) - Solo visible en hover -->
          <div 
            v-if="Number(game.community_rating) > 0" 
            class="bg-red-500/90 backdrop-blur-md shadow-xl rounded-full w-10 h-10 flex items-center justify-center border-2 border-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
            title="Valoración Comunidad"
          >
            <div class="flex flex-col items-center justify-center">
              <svg class="w-3.5 h-3.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
              </svg>
              <span class="text-[9px] font-bold text-white leading-none mt-0.5">{{ Number(game.community_rating).toFixed(1) }}</span>
            </div>
          </div>
        </div>
        
        <!-- Favorite Button -->
        <button
          v-if="authStore.isAuthenticated"
          @click.prevent="toggleFavorite"
          class="absolute top-3 left-3 bg-dark-900/80 backdrop-blur-md p-2.5 rounded-full hover:scale-110 transition-all z-10 border border-dark-700/50"
          :class="isFavorite ? 'text-red-500' : 'text-gray-400 hover:text-red-400'"
          :title="isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos'"
        >
          <svg class="w-4 h-4" :fill="isFavorite ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
          </svg>
        </button>
      
        <!-- Overlay gradient -->
        <div class="absolute inset-0 bg-gradient-to-t from-dark-900 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      </div>
      
      <div class="p-4">
        <h3 class="font-display font-bold text-base mb-2 line-clamp-2 group-hover:text-primary-400 transition-colors">{{ game.title }}</h3>
        <div v-if="game.categories && game.categories.length > 0" class="flex flex-wrap gap-1.5">
          <span 
            v-for="category in game.categories.slice(0, 2)" 
            :key="category.id"
            class="text-xs bg-dark-800/50 text-gray-300 px-2.5 py-1 rounded-full border border-dark-700"
          >
            {{ category.name }}
          </span>
        </div>
        <div v-else class="h-5"></div>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const props = defineProps({
  game: {
    type: Object,
    required: true
  }
})

const authStore = useAuthStore()
const isFavorite = ref(props.game.is_favorite || false)

const toggleFavorite = async () => {
  if (!authStore.isAuthenticated) return
  
  try {
    const response = await api.post(`/games/${props.game.slug}/toggle_favorite/`)
    isFavorite.value = response.data.is_favorite
  } catch (error) {
    console.error('Error toggling favorite:', error)
  }
}
</script>
