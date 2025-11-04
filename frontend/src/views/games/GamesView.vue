<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-display font-bold mb-3 bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">Explorar Juegos</h1>
      <p class="text-gray-400 text-sm">Descubre los mejores juegos de la comunidad</p>
    </div>
    
    <!-- Search Bar -->
    <div class="mb-6">
      <div class="relative">
        <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input
          v-model="searchQuery"
          @input="searchGames"
          type="text"
          class="input pl-12"
          placeholder="Buscar juegos..."
        >
      </div>
    </div>
    
    <!-- Stats -->
    <div class="mb-6 flex items-center gap-4 text-sm text-gray-400">
      <span>{{ total }} juegos disponibles</span>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
      <div v-for="i in 12" :key="i" class="animate-pulse">
        <div class="aspect-[2/3] bg-dark-850 rounded-xl mb-2"></div>
        <div class="h-4 bg-dark-850 rounded w-3/4 mb-2"></div>
        <div class="h-3 bg-dark-850 rounded w-1/2"></div>
      </div>
    </div>
    
    <!-- Games Grid -->
    <div v-else-if="games.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
      <GameCard v-for="game in games" :key="game.id" :game="game" />
    </div>
    
    <!-- Empty State -->
    <div v-else class="text-center py-16">
      <svg class="w-16 h-16 mx-auto text-gray-700 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p class="text-gray-400">No se encontraron juegos</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import GameCard from '@/components/cards/GameCard.vue'

const games = ref([])
const loading = ref(true)
const searchQuery = ref('')
const total = ref(0)
let searchTimeout = null

async function loadGames(search = '') {
  loading.value = true
  try {
    const response = await api.get('/games/', {
      params: {
        search: search || undefined,
        page_size: 24
      }
    })
    console.log('Games response:', response.data)
    console.log('Is array?', Array.isArray(response.data))
    
    // Manejar tanto respuestas paginadas como arrays directos
    if (Array.isArray(response.data)) {
      games.value = response.data
      total.value = response.data.length
    } else if (response.data && response.data.results) {
      games.value = response.data.results
      total.value = response.data.count || response.data.results.length
    } else {
      games.value = []
      total.value = 0
    }
    
    console.log('Loaded games:', games.value)
    console.log('Games count:', games.value.length)
  } catch (error) {
    console.error('Error loading games:', error)
    console.error('Error details:', error.response)
  } finally {
    loading.value = false
  }
}

function searchGames() {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadGames(searchQuery.value)
  }, 300)
}

onMounted(() => {
  loadGames()
})
</script>
