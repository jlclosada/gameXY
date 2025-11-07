<template>
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="$emit('close')">
    <div class="card max-w-3xl w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-display font-bold">Crear Nuevo Tema</h2>
          <button @click="$emit('close')" class="text-dark-400 hover:text-white transition">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div v-if="error" class="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg text-sm">
            {{ error }}
          </div>

          <!-- Title -->
          <div>
            <label class="block text-sm font-medium mb-2">Título del Tema *</label>
            <input
              v-model="form.title"
              type="text"
              required
              class="input"
              placeholder="Ej: ¿Cómo resolver el bug de..."
              maxlength="200"
            >
            <p class="text-xs text-dark-400 mt-1">{{ form.title.length }}/200 caracteres</p>
          </div>

          <!-- Content -->
          <div>
            <label class="block text-sm font-medium mb-2">Descripción *</label>
            <textarea
              v-model="form.content"
              required
              class="input min-h-[200px]"
              placeholder="Describe tu tema con detalle..."
            ></textarea>
            <p class="text-xs text-dark-400 mt-1">Puedes incluir detalles, pasos para reproducir, capturas, etc.</p>
          </div>

          <!-- Actions -->
          <div class="flex gap-4">
            <button
              type="submit"
              :disabled="loading || !form.title.trim() || !form.content.trim()"
              class="btn btn-primary flex-1"
            >
              {{ loading ? 'Creando...' : 'Crear Tema' }}
            </button>
            <button
              type="button"
              @click="$emit('close')"
              class="btn btn-secondary"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/axios'

const props = defineProps({
  forum: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'created'])

const form = ref({
  title: '',
  content: ''
})

const loading = ref(false)
const error = ref(null)

async function handleSubmit() {
  loading.value = true
  error.value = null

  try {
    const response = await api.post('/community/topics/', {
      forum: props.forum.id,
      title: form.value.title,
      content: form.value.content
    })

    emit('created', response.data)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al crear el tema'
  } finally {
    loading.value = false
  }
}
</script>
