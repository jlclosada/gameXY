<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-8 gap-4">
      <h1 class="text-4xl font-display font-bold">📖 Guías de Videojuegos</h1>
      
      <!-- Filters -->
      <div class="flex gap-3">
        <!-- Game Filter -->
        <select 
          v-model="selectedGame"
          @change="loadGuides"
          class="input w-full md:w-64"
        >
          <option value="">Todos los juegos</option>
          <option v-for="game in games" :key="game.id" :value="game.id">
            {{ game.title }}
          </option>
        </select>
        
        <!-- Difficulty Filter -->
        <select 
          v-model="selectedDifficulty"
          @change="loadGuides"
          class="input w-full md:w-48"
        >
          <option value="">Todas las dificultades</option>
          <option value="beginner">Principiante</option>
          <option value="intermediate">Intermedio</option>
          <option value="advanced">Avanzado</option>
        </select>
      </div>
    </div>
    
    <!-- Results Count -->
    <div v-if="!loading" class="mb-6">
      <p class="text-gray-400 text-sm">
        {{ guides.length }} {{ guides.length === 1 ? 'guía encontrada' : 'guías encontradas' }}
      </p>
    </div>
    
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="card h-72 animate-pulse bg-dark-700"></div>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="guide in guides" :key="guide.id" class="card cursor-pointer hover:shadow-2xl transition-shadow">
        <RouterLink :to="`/guides/${guide.slug}`">
          <div class="aspect-video relative overflow-hidden">
            <img v-if="guide.thumbnail" :src="guide.thumbnail" :alt="guide.title" class="w-full h-full object-cover">
            <div v-else class="w-full h-full bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center">
              <span class="text-white text-5xl">📖</span>
            </div>
            <span class="absolute top-2 right-2 bg-dark-800 text-white px-3 py-1 rounded-full text-xs">
              {{ guide.difficulty }}
            </span>
          </div>
          <div class="p-6">
            <h3 class="font-display font-semibold text-xl mb-2 line-clamp-2">{{ guide.title }}</h3>
            <p class="text-dark-400 text-sm line-clamp-2 mb-4">{{ guide.description }}</p>
            <div class="flex items-center justify-between text-xs text-dark-500">
              <span>{{ guide.author.username }}</span>
              <span>❤️ {{ guide.likes_count || 0 }}</span>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/api/axios'

const guides = ref([])
const games = ref([])
const loading = ref(true)
const selectedGame = ref('')
const selectedDifficulty = ref('')

const loadGames = async () => {
  try {
    const response = await api.get('/games/')
    games.value = response.data.results || response.data
  } catch (error) {
    console.error('Error loading games:', error)
  }
}

const loadGuides = async () => {
  loading.value = true
  try {
    const params = {}
    if (selectedGame.value) {
      params.game = selectedGame.value
    }
    if (selectedDifficulty.value) {
      params.difficulty = selectedDifficulty.value
    }
    
    const response = await api.get('/content/guides/', { params })
    
    // Manejar tanto respuestas paginadas como arrays directos
    if (Array.isArray(response.data)) {
      guides.value = response.data
    } else if (response.data && response.data.results) {
      guides.value = response.data.results
    } else {
      guides.value = []
    }
  } catch (error) {
    console.error('Error loading guides:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadGames()
  await loadGuides()
})
</script>
