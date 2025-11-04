<template>
  <div class="comment-section">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-display font-bold">
        💬 Comentarios
      </h2>
      <span class="badge badge-primary text-sm px-3 py-1">
        {{ comments.length }}
      </span>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-10 w-10 border-b-2 border-primary-500"></div>
      <p class="text-gray-400 mt-4">Cargando comentarios...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="comments.length === 0" class="card p-8 mb-8 text-center">
      <div class="text-5xl mb-4">💭</div>
      <p class="text-gray-400 text-lg mb-2">Aún no hay comentarios</p>
      <p class="text-gray-500 text-sm">¡Sé el primero en compartir tu opinión!</p>
    </div>

    <!-- Lista de comentarios -->
    <div v-else class="space-y-3 mb-8">
      <CommentItem
        v-for="comment in topLevelComments"
        :key="comment.id"
        :comment="comment"
        :resource-type="resourceType"
        :resource-id="resourceId"
        @comment-updated="loadComments"
        @comment-deleted="loadComments"
      />
    </div>

    <!-- Divider -->
    <div class="border-t border-dark-800 my-8"></div>

    <!-- Formulario para nuevo comentario -->
    <div class="mb-6">
      <h3 class="text-lg font-display font-semibold mb-4">Agregar un comentario</h3>
      <div v-if="authStore.isAuthenticated">
        <CommentForm
          :resource-type="resourceType"
          :resource-id="resourceId"
          @comment-added="handleCommentAdded"
        />
      </div>
      <div v-else class="card p-8 text-center bg-dark-850">
        <div class="text-4xl mb-3">🔒</div>
        <p class="text-gray-400 mb-4">Debes iniciar sesión para comentar</p>
        <RouterLink to="/login" class="btn btn-primary inline-flex items-center gap-2">
          <span>Iniciar sesión</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import CommentForm from './CommentForm.vue'
import CommentItem from './CommentItem.vue'

const props = defineProps({
  resourceType: {
    type: String,
    required: true,
    validator: (value) => ['game', 'news', 'post', 'guide'].includes(value)
  },
  resourceId: {
    type: Number,
    required: true
  }
})

const authStore = useAuthStore()
const comments = ref([])
const loading = ref(false)

const topLevelComments = computed(() => {
  return comments.value.filter(c => !c.parent)
})

const loadComments = async () => {
  loading.value = true
  try {
    const response = await api.get('/content/comments/', {
      params: { [props.resourceType]: props.resourceId }
    })
    comments.value = response.data.results || response.data
  } catch (error) {
    console.error('Error loading comments:', error)
  } finally {
    loading.value = false
  }
}

const handleCommentAdded = () => {
  loadComments()
}

onMounted(() => {
  loadComments()
})
</script>
