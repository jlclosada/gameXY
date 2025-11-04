<template>
  <div class="relative" ref="searchRef">
    <!-- Search Input -->
    <div class="relative">
      <input
        v-model="searchQuery"
        @focus="showResults = true"
        @input="handleSearch"
        type="text"
        placeholder="Buscar juegos, guías, noticias..."
        class="w-full pl-10 pr-4 py-2 bg-dark-850 border border-dark-700 rounded-lg text-gray-200 placeholder-gray-500 focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition"
      >
      <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
      
      <!-- Loading Spinner -->
      <div v-if="searching" class="absolute right-3 top-1/2 -translate-y-1/2">
        <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-500"></div>
      </div>
      
      <!-- Clear Button -->
      <button
        v-if="searchQuery && !searching"
        @click="clearSearch"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Search Results Dropdown -->
    <div
      v-if="showResults && searchQuery.length >= 2"
      class="absolute top-full left-0 right-0 mt-2 bg-dark-850 border border-dark-700 rounded-lg shadow-2xl max-h-[500px] overflow-y-auto z-50"
    >
      <!-- No Results -->
      <div v-if="!searching && !hasResults" class="p-6 text-center text-gray-400">
        <svg class="w-12 h-12 mx-auto mb-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <p class="font-medium">No se encontraron resultados</p>
        <p class="text-sm mt-1">Intenta con otros términos de búsqueda</p>
      </div>

      <!-- Games Results -->
      <div v-if="results.games.length > 0" class="border-b border-dark-800">
        <div class="px-4 py-2 bg-dark-900/50 text-xs font-semibold text-gray-400 uppercase tracking-wider">
          🎮 Juegos ({{ results.games.length }})
        </div>
        <RouterLink
          v-for="game in results.games"
          :key="`game-${game.id}`"
          :to="`/games/${game.slug}`"
          @click="closeSearch"
          class="flex items-center gap-3 px-4 py-3 hover:bg-dark-800 transition group"
        >
          <div class="w-12 h-16 rounded overflow-hidden flex-shrink-0 bg-dark-900">
            <img v-if="game.cover_image" :src="game.cover_image" :alt="game.title" class="w-full h-full object-cover">
            <div v-else class="w-full h-full flex items-center justify-center text-gray-600">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z"/>
              </svg>
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium text-gray-200 group-hover:text-primary-400 transition truncate">{{ game.title }}</p>
            <div class="flex items-center gap-1.5 mt-0.5">
              <span v-if="game.official_rating !== null && game.official_rating !== undefined" class="inline-flex items-center px-1.5 py-0.5 bg-gradient-to-br from-amber-400 to-amber-600 rounded text-[10px] font-black text-white">
                {{ Number(game.official_rating).toFixed(1) }}
              </span>
              <span v-if="game.community_rating && Number(game.community_rating) > 0" class="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-gradient-to-br from-red-500 to-red-600 rounded text-[10px] font-black text-white">
                <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
                </svg>
                {{ Number(game.community_rating).toFixed(1) }}
              </span>
            </div>
          </div>
        </RouterLink>
      </div>

      <!-- Guides Results -->
      <div v-if="results.guides.length > 0" class="border-b border-dark-800">
        <div class="px-4 py-2 bg-dark-900/50 text-xs font-semibold text-gray-400 uppercase tracking-wider">
          📖 Guías ({{ results.guides.length }})
        </div>
        <RouterLink
          v-for="guide in results.guides"
          :key="`guide-${guide.id}`"
          :to="`/guides/${guide.slug}`"
          @click="closeSearch"
          class="flex items-center gap-3 px-4 py-3 hover:bg-dark-800 transition group"
        >
          <div class="w-20 h-12 rounded overflow-hidden flex-shrink-0 bg-dark-900">
            <img v-if="guide.thumbnail" :src="guide.thumbnail" :alt="guide.title" class="w-full h-full object-cover">
            <div v-else class="w-full h-full flex items-center justify-center text-gray-600 text-2xl">
              📖
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium text-gray-200 group-hover:text-primary-400 transition truncate">{{ guide.title }}</p>
            <div class="flex items-center gap-3 text-xs text-gray-500 mt-0.5">
              <span>Por {{ guide.author.username }}</span>
              <span>❤️ {{ guide.likes_count }}</span>
            </div>
          </div>
        </RouterLink>
      </div>

      <!-- News Results -->
      <div v-if="results.news.length > 0" class="border-b border-dark-800">
        <div class="px-4 py-2 bg-dark-900/50 text-xs font-semibold text-gray-400 uppercase tracking-wider">
          📰 Noticias ({{ results.news.length }})
        </div>
        <RouterLink
          v-for="newsItem in results.news"
          :key="`news-${newsItem.id}`"
          :to="`/news/${newsItem.slug}`"
          @click="closeSearch"
          class="flex items-center gap-3 px-4 py-3 hover:bg-dark-800 transition group"
        >
          <div class="w-20 h-12 rounded overflow-hidden flex-shrink-0 bg-dark-900">
            <img v-if="newsItem.featured_image" :src="newsItem.featured_image" :alt="newsItem.title" class="w-full h-full object-cover">
            <div v-else class="w-full h-full flex items-center justify-center text-gray-600 text-2xl">
              📰
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium text-gray-200 group-hover:text-primary-400 transition truncate">{{ newsItem.title }}</p>
            <p class="text-xs text-gray-500 mt-0.5 truncate">{{ newsItem.excerpt }}</p>
          </div>
        </RouterLink>
      </div>

      <!-- View All Results -->
      <div v-if="hasResults" class="p-3 text-center border-t border-dark-800">
        <button
          @click="viewAllResults"
          class="text-sm text-primary-400 hover:text-primary-300 font-medium"
        >
          Ver todos los resultados →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()
const searchQuery = ref('')
const showResults = ref(false)
const searching = ref(false)
const searchRef = ref(null)

const results = ref({
  games: [],
  guides: [],
  news: []
})

let searchTimeout = null

const hasResults = computed(() => {
  return results.value.games.length > 0 || 
         results.value.guides.length > 0 || 
         results.value.news.length > 0
})

const handleSearch = () => {
  if (searchQuery.value.length < 2) {
    results.value = { games: [], guides: [], news: [] }
    return
  }

  // Debounce search
  clearTimeout(searchTimeout)
  searching.value = true

  searchTimeout = setTimeout(async () => {
    try {
      const [gamesRes, guidesRes, newsRes] = await Promise.all([
        api.get('/games/', { params: { search: searchQuery.value, page_size: 5 } }),
        api.get('/content/guides/', { params: { search: searchQuery.value, page_size: 5 } }),
        api.get('/content/news/', { params: { search: searchQuery.value, page_size: 5 } })
      ])

      results.value = {
        games: gamesRes.data.results || gamesRes.data || [],
        guides: guidesRes.data.results || guidesRes.data || [],
        news: newsRes.data.results || newsRes.data || []
      }
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      searching.value = false
    }
  }, 300)
}

const clearSearch = () => {
  searchQuery.value = ''
  results.value = { games: [], guides: [], news: [] }
  showResults.value = false
}

const closeSearch = () => {
  showResults.value = false
}

const viewAllResults = () => {
  router.push({ name: 'search', query: { q: searchQuery.value } })
  closeSearch()
}

const handleClickOutside = (event) => {
  if (searchRef.value && !searchRef.value.contains(event.target)) {
    showResults.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  clearTimeout(searchTimeout)
})
</script>
