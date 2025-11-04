<template>
  <div class="relative">
    <!-- Loading State -->
    <div v-if="loading" class="animate-pulse">
      <div class="h-[400px] bg-dark-700 mb-8"></div>
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="h-12 bg-dark-700 rounded w-3/4 mb-4"></div>
        <div class="h-64 bg-dark-700 rounded"></div>
      </div>
    </div>

    <div v-else-if="news">
      <!-- Hero Section -->
      <div class="relative h-[400px] md:h-[500px] overflow-hidden">
        <div 
          v-if="news.featured_image" 
          class="absolute inset-0 bg-cover bg-center transform scale-105"
          :style="{ backgroundImage: `url(${news.featured_image})` }"
        >
          <div class="absolute inset-0 bg-gradient-to-b from-dark-950/40 via-dark-950/70 to-dark-950"></div>
        </div>
        <div v-else class="absolute inset-0 bg-gradient-to-br from-primary-900/20 via-dark-950 to-dark-950"></div>
        
        <!-- Content over banner -->
        <div class="relative h-full max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col justify-end pb-8">
          <div class="space-y-4">
            <div class="inline-block">
              <span class="badge badge-accent text-xs px-3 py-1">📰 Noticia</span>
            </div>
            <h1 class="text-4xl md:text-5xl font-display font-bold text-white drop-shadow-lg leading-tight">
              {{ news.title }}
            </h1>
            <div class="flex items-center gap-4 text-sm">
              <div class="flex items-center gap-2 bg-dark-900/80 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-dark-700">
                <div class="w-8 h-8 rounded-full overflow-hidden border-2 border-dark-600 flex-shrink-0">
                  <img
                    v-if="news.author?.avatar"
                    :src="news.author.avatar"
                    :alt="news.author.username"
                    class="w-full h-full object-cover"
                  >
                  <div v-else class="w-full h-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold text-xs">
                    {{ news.author?.username?.charAt(0).toUpperCase() }}
                  </div>
                </div>
                <span class="text-gray-300 font-medium">{{ news.author?.username }}</span>
                <span class="text-gray-500">·</span>
                <span class="text-gray-400">{{ formatDate(news.created_at) }}</span>
              </div>
              <div class="flex items-center gap-2 bg-dark-900/80 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-dark-700">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                <span class="text-gray-400">{{ news.views_count || 0 }} vistas</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Excerpt -->
        <div v-if="news.excerpt" class="card p-6 mb-8 border-l-4 border-primary-500">
          <p class="text-lg text-gray-300 leading-relaxed italic">{{ news.excerpt }}</p>
        </div>

        <!-- Content -->
        <article class="card p-8 mb-8">
          <div class="prose prose-invert prose-lg max-w-none">
            <div v-html="renderedContent" class="leading-relaxed"></div>
          </div>
        </article>

        <!-- Related Game -->
        <div v-if="news.game" class="card p-6 mb-8">
          <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Juego relacionado</h3>
          <RouterLink 
            :to="`/games/${news.game.slug}`"
            class="flex items-center gap-4 p-4 bg-dark-850 rounded-lg hover:bg-dark-800 transition group"
          >
            <div v-if="news.game.cover_image" class="w-16 h-20 rounded overflow-hidden flex-shrink-0">
              <img :src="news.game.cover_image" :alt="news.game.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
            </div>
            <div class="flex-1">
              <p class="font-display font-semibold text-gray-100 group-hover:text-primary-400 transition">{{ news.game.title }}</p>
              <p class="text-xs text-gray-500 mt-1">Ver más información</p>
            </div>
            <svg class="w-5 h-5 text-gray-600 group-hover:text-primary-400 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </RouterLink>
        </div>

        <!-- Comentarios -->
        <CommentSection
          resource-type="news"
          :resource-id="news.id"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { marked } from 'marked'
import api from '@/api/axios'
import CommentSection from '@/components/comments/CommentSection.vue'

const route = useRoute()
const news = ref(null)
const loading = ref(true)

// Computed property para renderizar el markdown
const renderedContent = computed(() => {
  if (!news.value?.content) return ''
  return marked(news.value.content)
})

function formatDate(date) {
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(async () => {
  try {
    const response = await api.get(`/content/news/${route.params.slug}/`)
    news.value = response.data
  } catch (error) {
    console.error('Error loading news:', error)
  } finally {
    loading.value = false
  }
})
</script>
