<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-display font-bold mb-3">
        📚 Guías Guardadas
      </h1>
      <p class="text-gray-400">Accede rápidamente a las guías que has guardado para consultar más tarde</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="n in 6" :key="n" class="card animate-pulse">
        <div class="h-48 bg-dark-700"></div>
        <div class="p-4 space-y-3">
          <div class="h-4 bg-dark-700 rounded w-3/4"></div>
          <div class="h-3 bg-dark-700 rounded w-full"></div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="guides.length === 0" class="card p-12 text-center">
      <div class="text-6xl mb-4">📖</div>
      <h2 class="text-2xl font-display font-bold mb-3">No has guardado ninguna guía</h2>
      <p class="text-gray-400 mb-6">Explora las guías disponibles y guarda las que te interesen para acceder a ellas más tarde</p>
      <RouterLink to="/guides" class="btn btn-primary inline-flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        Explorar Guías
      </RouterLink>
    </div>

    <!-- Guides Grid -->
    <div v-else class="space-y-6">
      <div class="flex items-center justify-between">
        <p class="text-gray-400">{{ guides.length }} {{ guides.length === 1 ? 'guía guardada' : 'guías guardadas' }}</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="guide in guides" :key="guide.id" class="card group relative">
          <RouterLink :to="`/guides/${guide.slug}`" class="block">
            <!-- Thumbnail -->
            <div class="aspect-video relative overflow-hidden bg-dark-850">
              <img 
                v-if="guide.thumbnail" 
                :src="guide.thumbnail" 
                :alt="guide.title"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              >
              <div v-else class="w-full h-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
                <span class="text-white text-5xl">📖</span>
              </div>
              
              <!-- Difficulty Badge -->
              <div class="absolute top-2 right-2 badge text-xs px-2 py-1"
                   :class="getDifficultyClass(guide.difficulty)">
                {{ getDifficultyLabel(guide.difficulty) }}
              </div>
            </div>
            
            <!-- Content -->
            <div class="p-4">
              <h3 class="font-display font-semibold text-lg mb-2 line-clamp-2 group-hover:text-primary-400 transition">
                {{ guide.title }}
              </h3>
              
              <p class="text-sm text-gray-400 line-clamp-2 mb-3">
                {{ guide.description }}
              </p>
              
              <!-- Meta Info -->
              <div class="flex items-center justify-between text-xs text-gray-500">
                <span>Por {{ guide.author.username }}</span>
                <div class="flex items-center gap-3">
                  <span>❤️ {{ guide.likes_count }}</span>
                  <span>👁️ {{ guide.views_count }}</span>
                </div>
              </div>
            </div>
          </RouterLink>
          
          <!-- Unsave Button -->
          <button
            @click.prevent="unsaveGuide(guide)"
            class="absolute top-2 left-2 bg-dark-900/90 backdrop-blur-sm border border-dark-700 p-2 rounded-lg hover:bg-red-500/20 hover:border-red-500 transition-all z-10"
            title="Quitar de guardados"
          >
            <svg class="w-4 h-4 text-accent-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
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

const guides = ref([])
const loading = ref(true)

const getDifficultyLabel = (difficulty) => {
  const labels = {
    beginner: 'Principiante',
    intermediate: 'Intermedio',
    advanced: 'Avanzado'
  }
  return labels[difficulty] || difficulty
}

const getDifficultyClass = (difficulty) => {
  const classes = {
    beginner: 'badge-accent',
    intermediate: 'badge-primary',
    advanced: 'badge-secondary'
  }
  return classes[difficulty] || 'badge-primary'
}

const loadSavedGuides = async () => {
  loading.value = true
  try {
    const response = await api.get('/content/guides/saved/')
    guides.value = response.data
  } catch (error) {
    console.error('Error loading saved guides:', error)
  } finally {
    loading.value = false
  }
}

const unsaveGuide = async (guide) => {
  try {
    await api.post(`/content/guides/${guide.slug}/save_guide/`)
    guides.value = guides.value.filter(g => g.id !== guide.id)
  } catch (error) {
    console.error('Error unsaving guide:', error)
  }
}

onMounted(() => {
  loadSavedGuides()
})
</script>
