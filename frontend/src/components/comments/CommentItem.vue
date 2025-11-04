<template>
  <div class="comment-item">
    <div class="bg-dark-850 hover:bg-dark-850/80 transition rounded-lg p-4 border border-dark-800">
      <div class="flex gap-4">
        <!-- Contenido -->
        <div class="flex-1">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-full overflow-hidden border-2 border-dark-700 flex-shrink-0">
              <img
                v-if="comment.user?.avatar"
                :src="comment.user.avatar"
                :alt="comment.user.username"
                class="w-full h-full object-cover"
              >
              <div v-else class="w-full h-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold text-xs">
                {{ comment.user?.username?.charAt(0).toUpperCase() }}
              </div>
            </div>
            <span class="font-semibold">{{ comment.user.username }}</span>
            <span class="text-xs text-gray-500">•</span>
            <span class="text-xs text-gray-500">{{ formattedDate }}</span>
            <span v-if="comment.created_at !== comment.updated_at" class="text-xs text-gray-500">
              (editado)
            </span>
          </div>

          <!-- Modo edición -->
          <div v-if="isEditing">
            <CommentForm
              :resource-type="resourceType"
              :resource-id="resourceId"
              :edit-comment="comment"
              @comment-updated="handleUpdated"
              @cancel="isEditing = false"
            />
          </div>

          <!-- Modo normal -->
          <div v-else>
            <p class="text-gray-200 whitespace-pre-wrap mb-4 leading-relaxed">{{ comment.content }}</p>

            <!-- Acciones -->
            <div class="flex items-center gap-4 text-sm">
              <button
                v-if="authStore.isAuthenticated"
                @click="toggleReply"
                class="text-gray-500 hover:text-primary-400 transition flex items-center gap-1.5"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"/>
                </svg>
                Responder
              </button>

              <button
                v-if="canEdit"
                @click="isEditing = true"
                class="text-gray-500 hover:text-blue-400 transition flex items-center gap-1.5"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
                Editar
              </button>

              <button
                v-if="canDelete"
                @click="handleDelete"
                class="text-gray-500 hover:text-red-400 transition flex items-center gap-1.5"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                Eliminar
              </button>
            </div>
          </div>

          <!-- Formulario de respuesta -->
          <div v-if="showReplyForm" class="mt-4">
            <CommentForm
              :resource-type="resourceType"
              :resource-id="resourceId"
              :parent-id="comment.id"
              @comment-added="handleReplyAdded"
              @cancel="showReplyForm = false"
            />
          </div>

          <!-- Respuestas anidadas -->
          <div v-if="comment.replies && comment.replies.length > 0" class="mt-4 space-y-3 pl-6 border-l-2 border-primary-500/30">
            <CommentItem
              v-for="reply in comment.replies"
              :key="reply.id"
              :comment="reply"
              :resource-type="resourceType"
              :resource-id="resourceId"
              @comment-updated="$emit('comment-updated')"
              @comment-deleted="$emit('comment-deleted')"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import CommentForm from './CommentForm.vue'

const props = defineProps({
  comment: {
    type: Object,
    required: true
  },
  resourceType: {
    type: String,
    required: true
  },
  resourceId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['comment-updated', 'comment-deleted'])

const authStore = useAuthStore()
const isEditing = ref(false)
const showReplyForm = ref(false)

const formattedDate = computed(() => {
  return new Date(props.comment.created_at).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})

const scoreClass = computed(() => {
  if (props.comment.score > 0) return 'text-green-400'
  if (props.comment.score < 0) return 'text-red-400'
  return 'text-gray-400'
})

const canEdit = computed(() => {
  return authStore.user?.id === props.comment.user.id || authStore.user?.can_edit_content
})

const canDelete = computed(() => {
  return authStore.user?.id === props.comment.user.id || authStore.user?.can_edit_content
})

const vote = async (voteType) => {
  if (!authStore.isAuthenticated) return

  try {
    // Si el usuario ya votó lo mismo, remover el voto
    const actualVoteType = props.comment.user_vote === voteType ? 'remove' : voteType
    
    const response = await api.post(`/content/comments/${props.comment.id}/vote/`, {
      vote_type: actualVoteType
    })

    props.comment.score = response.data.score
    props.comment.user_vote = response.data.status === 'liked' ? 'like' : 
                               response.data.status === 'disliked' ? 'dislike' : null
  } catch (error) {
    console.error('Error voting:', error)
  }
}

const toggleReply = () => {
  showReplyForm.value = !showReplyForm.value
}

const handleReplyAdded = () => {
  showReplyForm.value = false
  emit('comment-updated')
}

const handleUpdated = () => {
  isEditing.value = false
  emit('comment-updated')
}

const handleDelete = async () => {
  if (!confirm('¿Estás seguro de que quieres eliminar este comentario?')) return

  try {
    await api.delete(`/content/comments/${props.comment.id}/`)
    emit('comment-deleted')
  } catch (error) {
    console.error('Error deleting comment:', error)
    alert('Error al eliminar el comentario')
  }
}
</script>
