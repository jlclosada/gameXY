<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <div v-else-if="topic" class="space-y-6">
      <!-- Breadcrumb -->
      <div class="flex items-center gap-2 text-sm text-dark-400">
        <RouterLink to="/community" class="hover:text-white transition">Comunidad</RouterLink>
        <span>›</span>
        <RouterLink :to="`/community/forums/${forumSlug}`" class="hover:text-white transition">
          {{ topic.forum_name }}
        </RouterLink>
        <span>›</span>
        <span class="text-white">{{ topic.title }}</span>
      </div>

      <!-- Topic Header -->
      <div class="card p-6">
        <div class="flex items-start gap-4">
          <UserAvatar :user="topic.author" size="xl" />

          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <span v-if="topic.is_pinned" class="text-xs bg-primary-600 text-white px-2 py-1 rounded">📌 Fijado</span>
              <span v-if="topic.is_locked" class="text-xs bg-dark-700 text-dark-300 px-2 py-1 rounded">🔒 Cerrado</span>
            </div>
            
            <h1 class="text-3xl font-display font-bold mb-3">{{ topic.title }}</h1>
            
            <div class="flex items-center gap-4 text-sm text-dark-400 mb-4">
              <span class="font-semibold text-white">{{ topic.author.username }}</span>
              <span>{{ formatDate(topic.created_at) }}</span>
              <span>👁️ {{ topic.views }} vistas</span>
              <span>💬 {{ topic.reply_count }} respuestas</span>
            </div>

            <div class="prose prose-invert max-w-none">
              <p class="whitespace-pre-wrap text-dark-200">{{ topic.content }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Replies Section -->
      <div class="card">
        <div class="p-4 border-b border-dark-700 flex items-center justify-between">
          <h2 class="text-xl font-display font-bold">
            {{ topic.reply_count }} Respuestas
          </h2>
          <select v-model="sortPosts" class="input py-2 text-sm">
            <option value="oldest">Más Antiguas Primero</option>
            <option value="newest">Más Recientes Primero</option>
          </select>
        </div>

        <!-- Posts List -->
        <div v-if="sortedPosts.length === 0" class="text-center py-12 text-dark-400">
          Sin respuestas aún. ¡Sé el primero en responder!
        </div>

        <div v-else class="divide-y divide-dark-700">
          <div
            v-for="(post, index) in sortedPosts"
            :key="post.id"
            class="p-6"
            :class="post.is_solution && 'bg-green-900/10 border-l-4 border-green-500'"
          >
            <div class="flex items-start gap-4">
              <!-- User Info Sidebar -->
              <div class="w-32 flex-shrink-0">
                <div class="text-center">
                  <UserAvatar :user="post.author" size="lg" class="mx-auto mb-2" />
                  <p class="font-semibold text-sm mb-1">{{ post.author.username }}</p>
                  <p v-if="post.author.role === 'admin'" class="text-xs bg-red-600 text-white px-2 py-1 rounded mb-1">Admin</p>
                  <p v-else-if="post.author.role === 'goat'" class="text-xs bg-primary-600 text-white px-2 py-1 rounded mb-1">GOAT</p>
                  <p class="text-xs text-dark-500">{{ post.author.comments_count || 0 }} posts</p>
                </div>
              </div>

              <!-- Post Content -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center gap-2">
                    <span v-if="post.is_solution" class="text-xs bg-green-600 text-white px-2 py-1 rounded">
                      ✓ Solución
                    </span>
                    <span class="text-xs text-dark-500">
                      #{{ index + 1 }} · {{ formatDate(post.created_at) }}
                    </span>
                    <span v-if="post.is_edited" class="text-xs text-dark-500">(editado)</span>
                  </div>

                  <!-- Post Actions -->
                  <div v-if="authStore.isAuthenticated" class="flex items-center gap-2">
                    <button
                      v-if="topic.author.id === authStore.user?.id && !post.is_solution && !topic.is_locked"
                      @click="markAsSolution(post.id)"
                      class="text-xs text-green-400 hover:text-green-300 transition"
                      title="Marcar como solución"
                    >
                      ✓ Marcar como solución
                    </button>
                    <button
                      v-if="post.can_edit"
                      class="text-xs text-dark-400 hover:text-white transition"
                    >
                      Editar
                    </button>
                  </div>
                </div>

                <div class="prose prose-invert max-w-none">
                  <p class="whitespace-pre-wrap text-dark-200">{{ post.content }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Reply Form -->
        <div v-if="authStore.isAuthenticated && !topic.is_locked" class="p-6 border-t border-dark-700 bg-dark-800">
          <div class="flex items-start gap-4">
            <UserAvatar :user="authStore.user" size="md" />
            <div class="flex-1">
              <textarea
                v-model="replyContent"
                placeholder="Escribe tu respuesta..."
                class="input min-h-[120px] mb-3"
              ></textarea>
              <button
                @click="submitReply"
                :disabled="!replyContent.trim() || submittingReply"
                class="btn btn-primary"
              >
                {{ submittingReply ? 'Enviando...' : 'Publicar Respuesta' }}
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="topic.is_locked" class="p-6 border-t border-dark-700 bg-dark-800 text-center text-dark-400">
          🔒 Este tema está cerrado y no acepta nuevas respuestas
        </div>

        <div v-else class="p-6 border-t border-dark-700 bg-dark-800 text-center">
          <RouterLink to="/login" class="btn btn-primary">
            Inicia sesión para responder
          </RouterLink>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 text-dark-400">
      Tema no encontrado
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import UserAvatar from '@/components/common/UserAvatar.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const topic = ref(null)
const loading = ref(true)
const sortPosts = ref('oldest')
const replyContent = ref('')
const submittingReply = ref(false)

const forumSlug = computed(() => route.params.forumSlug)

const sortedPosts = computed(() => {
  if (!topic.value?.posts) return []
  
  const posts = [...topic.value.posts]
  
  if (sortPosts.value === 'newest') {
    return posts.reverse()
  }
  
  return posts
})

async function loadTopic() {
  try {
    const response = await api.get(`/community/topics/${route.params.topicSlug}/`)
    topic.value = response.data
  } catch (error) {
    console.error('Error loading topic:', error)
  } finally {
    loading.value = false
  }
}

async function submitReply() {
  if (!replyContent.value.trim()) return

  submittingReply.value = true
  try {
    const response = await api.post('/community/posts/', {
      topic: topic.value.id,
      content: replyContent.value
    })

    // Add new post to the list
    if (!topic.value.posts) topic.value.posts = []
    topic.value.posts.push(response.data)
    topic.value.reply_count = topic.value.posts.length

    replyContent.value = ''
    
    // Scroll to bottom
    setTimeout(() => {
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    }, 100)
  } catch (error) {
    console.error('Error submitting reply:', error)
    alert(error.response?.data?.detail || 'Error al enviar la respuesta')
  } finally {
    submittingReply.value = false
  }
}

async function markAsSolution(postId) {
  try {
    await api.patch(`/community/posts/${postId}/`, {
      is_solution: true
    })

    // Update local state
    const post = topic.value.posts.find(p => p.id === postId)
    if (post) {
      // Remove solution from other posts
      topic.value.posts.forEach(p => p.is_solution = false)
      post.is_solution = true
    }
  } catch (error) {
    console.error('Error marking as solution:', error)
    alert('Error al marcar como solución')
  }
}

function formatDate(date) {
  const d = new Date(date)
  const now = new Date()
  const diff = now - d
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return 'Ahora mismo'
  if (minutes < 60) return `Hace ${minutes}m`
  if (hours < 24) return `Hace ${hours}h`
  if (days < 7) return `Hace ${days}d`
  
  return d.toLocaleDateString('es-ES', { 
    day: 'numeric', 
    month: 'short', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  await loadTopic()
})
</script>
