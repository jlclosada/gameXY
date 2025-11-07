<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <div v-else-if="forum" class="space-y-6">
      <!-- Forum Header -->
      <div class="card p-6">
        <div class="flex items-start gap-4">
          <div class="text-5xl">{{ forum.icon }}</div>
          <div class="flex-1">
            <h1 class="text-3xl font-display font-bold mb-2">{{ forum.name }}</h1>
            <p class="text-dark-400 mb-4">{{ forum.description }}</p>
            <div class="flex items-center gap-6 text-sm text-dark-500">
              <span>{{ forum.topic_count }} temas</span>
              <span>{{ forum.post_count }} respuestas</span>
              <span class="px-2 py-1 bg-dark-700 rounded">{{ getCategoryLabel(forum.category) }}</span>
            </div>
          </div>

          <button
            v-if="authStore.isAuthenticated"
            @click="showCreateTopicModal = true"
            class="btn btn-primary"
          >
            <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Nuevo Tema
          </button>
        </div>
      </div>

      <!-- Topics List -->
      <div class="card">
        <div class="p-4 border-b border-dark-700">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-display font-bold">Temas de Discusión</h2>
            
            <!-- Filters -->
            <div class="flex items-center gap-2">
              <select v-model="sortBy" class="input py-2 text-sm">
                <option value="recent">Más Recientes</option>
                <option value="popular">Más Populares</option>
                <option value="unsolved">Sin Resolver</option>
              </select>
            </div>
          </div>
          
          <!-- Search Bar -->
          <div class="relative">
            <input
              v-model="topicSearchQuery"
              type="text"
              placeholder="Buscar temas..."
              class="input pl-10 w-full"
            />
            <svg class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </div>

        <div v-if="loadingTopics" class="text-center py-12">
          <div class="inline-block w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
        </div>

        <div v-else-if="filteredTopics.length === 0" class="text-center py-12 text-dark-400">
          {{ topicSearchQuery ? 'No se encontraron temas.' : 'No hay temas aún. ¡Sé el primero en crear uno!' }}
        </div>

        <div v-else class="divide-y divide-dark-700">
          <div
            v-for="topic in filteredTopics"
            :key="topic.id"
            @click="viewTopic(topic)"
            class="p-6 hover:bg-dark-800 transition cursor-pointer"
            :class="topic.is_pinned && 'bg-dark-800/50'"
          >
            <div class="flex items-start gap-4">
              <UserAvatar :user="topic.author" size="md" />

              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <span v-if="topic.is_pinned" class="text-xs bg-primary-600 text-white px-2 py-1 rounded">📌</span>
                  <span v-if="topic.is_locked" class="text-xs bg-dark-700 text-dark-300 px-2 py-1 rounded">🔒</span>
                  <h3 class="font-display font-bold text-lg hover:text-primary-400 transition">
                    {{ topic.title }}
                  </h3>
                </div>

                <p class="text-sm text-dark-400 mb-2 line-clamp-2">{{ topic.content }}</p>

                <div class="flex items-center gap-4 text-xs text-dark-500">
                  <span class="flex items-center gap-1">
                    <UserAvatar :user="topic.author" size="xs" />
                    {{ topic.author.username }}
                  </span>
                  <span>{{ formatDate(topic.created_at) }}</span>
                  <span>👁️ {{ topic.views }} vistas</span>
                  <span>💬 {{ topic.reply_count }} respuestas</span>
                  <span v-if="topic.latest_post" class="ml-auto">
                    Última respuesta: {{ formatDate(topic.latest_post.created_at) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Topic Modal -->
    <CreateTopicModal
      v-if="showCreateTopicModal"
      :forum="forum"
      @close="showCreateTopicModal = false"
      @created="onTopicCreated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import UserAvatar from '@/components/common/UserAvatar.vue'
import CreateTopicModal from '@/components/community/CreateTopicModal.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const forum = ref(null)
const topics = ref([])
const loading = ref(true)
const loadingTopics = ref(false)
const showCreateTopicModal = ref(false)
const sortBy = ref('recent')
const topicSearchQuery = ref('')

const categoryLabels = {
  'general': 'General',
  'games': 'Juegos',
  'news': 'Noticias',
  'guides': 'Guías',
  'support': 'Soporte',
  'off_topic': 'Off Topic'
}

const filteredTopics = computed(() => {
  if (!topicSearchQuery.value.trim()) {
    return topics.value
  }
  const query = topicSearchQuery.value.toLowerCase()
  return topics.value.filter(topic => 
    topic.title.toLowerCase().includes(query) || 
    topic.content.toLowerCase().includes(query)
  )
})

function getCategoryLabel(category) {
  return categoryLabels[category] || category
}

async function loadForum() {
  try {
    const response = await api.get(`/community/forums/${route.params.slug}/`)
    forum.value = response.data
  } catch (error) {
    console.error('Error loading forum:', error)
  } finally {
    loading.value = false
  }
}

async function loadTopics() {
  loadingTopics.value = true
  try {
    const response = await api.get('/community/topics/', {
      params: {
        forum: route.params.slug,
        ordering: sortBy.value === 'recent' ? '-last_post_at' : '-views'
      }
    })
    topics.value = response.data.results || response.data
  } catch (error) {
    console.error('Error loading topics:', error)
  } finally {
    loadingTopics.value = false
  }
}

function viewTopic(topic) {
  router.push(`/community/forums/${route.params.slug}/topics/${topic.slug}`)
}

function onTopicCreated(newTopic) {
  topics.value.unshift(newTopic)
  showCreateTopicModal.value = false
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
  
  return d.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}

watch(sortBy, () => {
  loadTopics()
})

onMounted(async () => {
  await loadForum()
  await loadTopics()
})
</script>
