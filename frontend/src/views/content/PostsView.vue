<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-4xl font-display font-bold mb-8">Posts de la Comunidad</h1>
    
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 5" :key="i" class="card h-32 animate-pulse bg-dark-700"></div>
    </div>
    
    <div v-else class="space-y-4">
      <RouterLink 
        v-for="post in posts" 
        :key="post.id" 
        :to="`/posts/${post.slug}`"
        class="card p-6 block hover:shadow-2xl transition-shadow"
      >
        <h3 class="font-display font-semibold text-2xl mb-3 hover:text-primary-400 transition-colors">
          {{ post.title }}
        </h3>
        <div class="flex items-center text-sm text-dark-400 space-x-4">
          <span>{{ post.author.username }}</span>
          <span>•</span>
          <span>{{ post.game_title }}</span>
          <span>•</span>
          <span>❤️ {{ post.likes_count || 0 }}</span>
          <span>•</span>
          <span>💬 {{ post.comments_count || 0 }}</span>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/api/axios'

const posts = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await api.get('/content/posts/')
    posts.value = response.data.results || []
  } catch (error) {
    console.error('Error loading posts:', error)
  } finally {
    loading.value = false
  }
})
</script>
