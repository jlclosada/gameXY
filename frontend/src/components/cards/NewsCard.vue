<template>
  <RouterLink :to="`/news/${news.slug}`" class="card group cursor-pointer hover:shadow-2xl transition-shadow duration-200">
    <div class="aspect-video relative overflow-hidden">
      <img 
        v-if="news.featured_image" 
        :src="news.featured_image" 
        :alt="news.title"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      >
      <div v-else class="w-full h-full bg-gradient-to-br from-primary-600 to-primary-800 flex items-center justify-center">
        <span class="text-white text-5xl">📰</span>
      </div>
    </div>
    
    <div class="p-6">
      <div class="flex items-center text-xs text-dark-400 mb-3 space-x-3">
        <span>{{ news.author.username }}</span>
        <span>•</span>
        <span>{{ formatDate(news.created_at) }}</span>
      </div>
      
      <h3 class="font-display font-semibold text-xl mb-2 line-clamp-2 group-hover:text-primary-400 transition-colors">
        {{ news.title }}
      </h3>
      
      <p class="text-dark-400 text-sm line-clamp-3 mb-4">
        {{ news.excerpt }}
      </p>
      
      <div class="flex items-center text-xs text-dark-500 space-x-4">
        <span>👁️ {{ news.views_count }}</span>
        <span>💬 {{ news.comments_count || 0 }}</span>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  news: {
    type: Object,
    required: true
  }
})

function formatDate(date) {
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
