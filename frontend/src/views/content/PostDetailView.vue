<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <article v-if="post" class="card p-8">
      <h1 class="text-4xl font-display font-bold mb-4">{{ post.title }}</h1>
      
      <div class="flex items-center text-sm text-dark-400 mb-8 space-x-4">
        <span>{{ post.author?.username }}</span>
        <span>•</span>
        <span>{{ formatDate(post.created_at) }}</span>
        <span>•</span>
        <span>❤️ {{ post.likes_count || 0 }}</span>
      </div>
      
      <div class="prose prose-invert max-w-none whitespace-pre-line mb-8">
        {{ post.content }}
      </div>
      
      <button 
        v-if="authStore.isAuthenticated"
        @click="toggleLike"
        class="btn"
        :class="post.is_liked ? 'btn-primary' : 'btn-secondary'"
      >
        {{ post.is_liked ? '❤️ Te gusta' : '🤍 Me gusta' }}
      </button>
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const route = useRoute()
const authStore = useAuthStore()
const post = ref(null)

function formatDate(date) {
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

async function toggleLike() {
  try {
    await api.post(`/content/posts/${route.params.slug}/like/`)
    const response = await api.get(`/content/posts/${route.params.slug}/`)
    post.value = response.data
  } catch (error) {
    console.error('Error toggling like:', error)
  }
}

onMounted(async () => {
  const response = await api.get(`/content/posts/${route.params.slug}/`)
  post.value = response.data
})
</script>
