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

    <div v-else-if="guide">
      <!-- Hero Section -->
      <div class="relative h-[400px] md:h-[500px] overflow-hidden">
        <div 
          v-if="guide.thumbnail" 
          class="absolute inset-0 bg-cover bg-center transform scale-105"
          :style="{ backgroundImage: `url(${guide.thumbnail})` }"
        >
          <div class="absolute inset-0 bg-gradient-to-b from-dark-950/40 via-dark-950/70 to-dark-950"></div>
        </div>
        <div v-else class="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-dark-950 to-dark-950"></div>
        
        <!-- Content over banner -->
        <div class="relative h-full max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col justify-end pb-8">
          <div class="space-y-4">
            <div class="flex items-center gap-3">
              <span class="badge badge-primary text-xs px-3 py-1">📖 Guía</span>
              <span class="badge badge-accent text-xs px-3 py-1">{{ difficultyLabel }}</span>
            </div>
            <h1 class="text-4xl md:text-5xl font-display font-bold text-white drop-shadow-lg leading-tight">
              {{ guide.title }}
            </h1>
            <p class="text-lg text-gray-300 max-w-3xl">{{ guide.description }}</p>
            <div class="flex items-center gap-4 text-sm flex-wrap">
              <div class="flex items-center gap-2 bg-dark-900/80 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-dark-700">
                <div class="w-8 h-8 rounded-full overflow-hidden border-2 border-dark-600 flex-shrink-0">
                  <img
                    v-if="guide.author?.avatar"
                    :src="guide.author.avatar"
                    :alt="guide.author.username"
                    class="w-full h-full object-cover"
                  >
                  <div v-else class="w-full h-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold text-xs">
                    {{ guide.author?.username?.charAt(0).toUpperCase() }}
                  </div>
                </div>
                <span class="text-gray-300 font-medium">{{ guide.author?.username }}</span>
                <span class="text-gray-500">·</span>
                <span class="text-gray-400">{{ formatDate(guide.created_at) }}</span>
              </div>
              <div class="flex items-center gap-2 bg-dark-900/80 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-dark-700">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                <span class="text-gray-400">{{ guide.views_count || 0 }} vistas</span>
              </div>
              <div class="flex items-center gap-2 bg-dark-900/80 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-dark-700">
                <svg class="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
                </svg>
                <span class="text-gray-400">{{ guide.likes_count || 0 }} me gusta</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Video (si existe) -->
        <div v-if="guide.video_url" class="card p-6 mb-8">
          <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Video tutorial</h3>
          <div class="aspect-video rounded-lg overflow-hidden">
            <iframe :src="guide.video_url" class="w-full h-full" allowfullscreen></iframe>
          </div>
        </div>

        <!-- Content -->
        <article class="card p-8 mb-8">
          <div class="prose prose-invert prose-lg max-w-none" v-html="renderedContent"></div>
        </article>

        <!-- Actions -->
        <div class="card p-6 mb-8">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <button
                v-if="authStore.isAuthenticated"
                @click="toggleLike"
                class="btn inline-flex items-center gap-2"
                :class="guide.is_liked ? 'btn-primary' : 'btn-secondary'"
              >
                <svg class="w-5 h-5" :class="guide.is_liked ? 'text-white' : 'text-gray-400'" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
                </svg>
                <span>{{ guide.is_liked ? 'Te gusta' : 'Me gusta' }}</span>
              </button>
              
              <button
                v-if="authStore.isAuthenticated"
                @click="toggleSave"
                class="btn inline-flex items-center gap-2"
                :class="guide.is_saved ? 'btn-accent' : 'btn-ghost'"
              >
                <svg class="w-5 h-5" :fill="guide.is_saved ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
                </svg>
                <span>{{ guide.is_saved ? 'Guardada' : 'Guardar' }}</span>
              </button>
            </div>
            
            <!-- Edit/Delete buttons for author -->
            <div v-if="guide && (authStore.user?.id === guide.author.id || authStore.user?.can_edit_content)" class="flex gap-2">
              <button @click="handleEdit" class="btn btn-ghost text-sm">
                ✏️ Editar
              </button>
              <button @click="handleDelete" class="btn btn-ghost text-sm text-red-400 hover:text-red-300">
                🗑️ Eliminar
              </button>
            </div>
          </div>
        </div>

        <!-- Related Game -->
        <div v-if="guide.game" class="card p-6 mb-8">
          <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Juego</h3>
          <RouterLink 
            :to="`/games/${guide.game.slug}`"
            class="flex items-center gap-4 p-4 bg-dark-850 rounded-lg hover:bg-dark-800 transition group"
          >
            <div v-if="guide.game.cover_image" class="w-16 h-20 rounded overflow-hidden flex-shrink-0">
              <img :src="guide.game.cover_image" :alt="guide.game.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
            </div>
            <div class="flex-1">
              <p class="font-display font-semibold text-gray-100 group-hover:text-primary-400 transition">{{ guide.game.title }}</p>
              <p class="text-xs text-gray-500 mt-1">Ver más sobre este juego</p>
            </div>
            <svg class="w-5 h-5 text-gray-600 group-hover:text-primary-400 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </RouterLink>
        </div>

        <!-- Comentarios -->
        <CommentSection
          resource-type="guide"
          :resource-id="guide.id"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { marked } from 'marked'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import CommentSection from '@/components/comments/CommentSection.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const guide = ref(null)
const loading = ref(true)

// Computed property para renderizar el markdown
const renderedContent = computed(() => {
  if (!guide.value?.content) return ''
  return marked(guide.value.content)
})

const difficultyLabel = computed(() => {
  const labels = {
    beginner: 'Principiante',
    intermediate: 'Intermedio',
    advanced: 'Avanzado'
  }
  return labels[guide.value?.difficulty] || guide.value?.difficulty
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(async () => {
  try {
    const response = await api.get(`/content/guides/${route.params.slug}/`)
    guide.value = response.data
    console.log('Loaded guide:', guide.value)
  } catch (error) {
    console.error('Error loading guide:', error)
    router.push('/guides')
  } finally {
    loading.value = false
  }
})

const handleEdit = () => {
  router.push(`/guides/${guide.value.slug}/edit`)
}

const handleDelete = async () => {
  if (!confirm('¿Estás seguro de que quieres eliminar esta guía?')) return

  try {
    await api.delete(`/content/guides/${guide.value.slug}/`)
    router.push('/guides')
  } catch (error) {
    console.error('Error deleting guide:', error)
    alert('Error al eliminar la guía')
  }
}

const toggleLike = async () => {
  try {
    const response = await api.post(`/content/guides/${guide.value.slug}/like/`)
    guide.value.is_liked = response.data.status === 'liked'
    guide.value.likes_count = response.data.likes_count
  } catch (error) {
    console.error('Error toggling like:', error)
  }
}

const toggleSave = async () => {
  try {
    const response = await api.post(`/content/guides/${guide.value.slug}/save_guide/`)
    guide.value.is_saved = response.data.is_saved
  } catch (error) {
    console.error('Error toggling save:', error)
  }
}
</script>

<style scoped>
/* Estilos para el contenido renderizado desde el editor */
:deep(.prose) {
  @apply text-gray-200;
}

:deep(.prose h2) {
  @apply text-2xl font-display font-bold mt-8 mb-4 text-white;
}

:deep(.prose h3) {
  @apply text-xl font-display font-semibold mt-6 mb-3 text-white;
}

:deep(.prose p) {
  @apply my-4 leading-relaxed;
}

:deep(.prose ul),
:deep(.prose ol) {
  @apply my-4 pl-6;
}

:deep(.prose li) {
  @apply my-2;
}

:deep(.prose img) {
  @apply rounded-lg my-6 max-w-full;
}

:deep(.prose iframe) {
  @apply rounded-lg my-6;
}

:deep(.prose a) {
  @apply text-primary-400 hover:text-primary-300 underline;
}

:deep(.prose strong) {
  @apply font-bold text-white;
}

:deep(.prose em) {
  @apply italic;
}
</style>
