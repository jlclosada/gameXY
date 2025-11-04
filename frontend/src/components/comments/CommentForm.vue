<template>
  <div class="comment-form card p-4">
    <textarea
      v-model="content"
      :placeholder="placeholder"
      class="input min-h-[100px] mb-3"
      :disabled="submitting"
    ></textarea>
    <div class="flex justify-end gap-2">
      <button
        v-if="isEditing || parentId"
        @click="handleCancel"
        type="button"
        class="btn btn-ghost"
        :disabled="submitting"
      >
        Cancelar
      </button>
      <button
        @click="handleSubmit"
        type="button"
        class="btn btn-primary"
        :disabled="!content.trim() || submitting"
      >
        {{ submitting ? 'Enviando...' : (isEditing ? 'Actualizar' : 'Comentar') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '@/api/axios'

const props = defineProps({
  resourceType: {
    type: String,
    required: true
  },
  resourceId: {
    type: Number,
    required: true
  },
  parentId: {
    type: Number,
    default: null
  },
  editComment: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['comment-added', 'comment-updated', 'cancel'])

const content = ref(props.editComment?.content || '')
const submitting = ref(false)

const isEditing = computed(() => !!props.editComment)

const placeholder = computed(() => {
  if (props.parentId) return 'Escribe una respuesta...'
  return 'Escribe un comentario...'
})

const handleSubmit = async () => {
  if (!content.value.trim()) return

  submitting.value = true

  try {
    const data = {
      content: content.value,
      [props.resourceType]: props.resourceId
    }

    if (props.parentId) {
      data.parent = props.parentId
    }

    if (isEditing.value) {
      await api.patch(`/content/comments/${props.editComment.id}/`, data)
      emit('comment-updated')
    } else {
      await api.post('/content/comments/', data)
      emit('comment-added')
    }

    content.value = ''
  } catch (error) {
    console.error('Error submitting comment:', error)
    alert('Error al enviar el comentario')
  } finally {
    submitting.value = false
  }
}

const handleCancel = () => {
  content.value = ''
  emit('cancel')
}
</script>
