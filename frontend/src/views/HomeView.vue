<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-dark-800 via-dark-900 to-black py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-5xl md:text-6xl font-display font-bold mb-6">
            Bienvenido a <span class="text-white">Game</span><span class="bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">XY</span>
          </h1>
          <p class="text-xl text-dark-300 mb-8 max-w-2xl mx-auto">
            La comunidad definitiva para gamers. Descubre juegos, lee noticias, aprende con guías y comparte tu pasión.
          </p>
          <div class="flex justify-center space-x-4">
            <RouterLink to="/games" class="btn btn-primary px-8 py-3 text-lg">
              Explorar Juegos
            </RouterLink>
            <RouterLink to="/guides" class="btn btn-secondary px-8 py-3 text-lg">
              Ver Guías
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Games -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="flex justify-between items-center mb-8">
        <h2 class="text-3xl font-display font-bold">Juegos Destacados</h2>
        <RouterLink to="/games" class="link">Ver todos →</RouterLink>
      </div>
      
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div v-for="i in 4" :key="i" class="card h-64 animate-pulse bg-dark-700"></div>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <GameCard v-for="game in featuredGames" :key="game.id" :game="game" />
      </div>
    </section>

    <!-- Latest News -->
    <section class="bg-dark-800 py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-display font-bold">Últimas Noticias</h2>
          <RouterLink to="/news" class="link">Ver todas →</RouterLink>
        </div>
        
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 3" :key="i" class="card h-80 animate-pulse bg-dark-700"></div>
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <NewsCard v-for="news in latestNews" :key="news.id" :news="news" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/api/axios'
import GameCard from '@/components/cards/GameCard.vue'
import NewsCard from '@/components/cards/NewsCard.vue'

const featuredGames = ref([])
const latestNews = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [gamesRes, newsRes] = await Promise.all([
      api.get('/games/?is_featured=true&page_size=4'),
      api.get('/content/news/?page_size=3')
    ])
    
    featuredGames.value = gamesRes.data.results || []
    latestNews.value = newsRes.data.results || []
  } catch (error) {
    console.error('Error loading home data:', error)
  } finally {
    loading.value = false
  }
})
</script>
