<template>
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="$emit('close')">
    <div class="card max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-display font-bold">Crear Nuevo Grupo</h2>
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

          <!-- Name -->
          <div>
            <label class="block text-sm font-medium mb-2">Nombre del Grupo *</label>
            <input
              v-model="form.name"
              type="text"
              required
              class="input"
              placeholder="Ej: Liga de Legends Pro"
            >
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium mb-2">Descripción *</label>
            <textarea
              v-model="form.description"
              required
              class="input min-h-[120px]"
              placeholder="Describe tu grupo, objetivos, estilo de juego..."
            ></textarea>
          </div>

          <!-- Game (optional) -->
          <div>
            <label class="block text-sm font-medium mb-2">Juego (opcional)</label>
            <select v-model="form.game" class="input">
              <option :value="null">Sin juego específico</option>
              <option v-for="game in games" :key="game.id" :value="game.id">
                {{ game.title }}
              </option>
            </select>
          </div>

          <!-- Icon Upload -->
          <div>
            <label class="block text-sm font-medium mb-2">Icono del Grupo</label>
            <div class="flex items-center gap-4">
              <div class="w-20 h-20 rounded-lg bg-dark-700 flex items-center justify-center overflow-hidden">
                <img v-if="previewIcon" :src="previewIcon" alt="Preview" class="w-full h-full object-cover" />
                <svg v-else class="w-10 h-10 text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
              <div class="flex-1">
                <input
                  type="file"
                  ref="iconInput"
                  @change="handleIconChange"
                  accept="image/*"
                  class="hidden"
                >
                <button
                  type="button"
                  @click="$refs.iconInput.click()"
                  class="btn btn-secondary"
                >
                  Seleccionar Imagen
                </button>
                <p class="text-xs text-dark-400 mt-1">JPG, PNG (máx. 2MB)</p>
              </div>
            </div>
          </div>

          <!-- Privacy -->
          <div>
            <label class="block text-sm font-medium mb-3">Privacidad del Grupo *</label>
            <div class="grid grid-cols-2 gap-4">
              <button
                type="button"
                @click="form.is_public = true"
                class="p-4 rounded-lg border-2 transition text-left"
                :class="form.is_public 
                  ? 'border-primary-600 bg-primary-900/20' 
                  : 'border-dark-700 hover:border-dark-600'"
              >
                <div class="flex items-center gap-3 mb-2">
                  <div class="w-10 h-10 rounded-lg bg-green-600/20 flex items-center justify-center">
                    <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                    </svg>
                  </div>
                  <div>
                    <div class="font-bold">Público</div>
                  </div>
                </div>
                <p class="text-xs text-dark-400">Cualquiera puede unirse y ver el contenido</p>
              </button>

              <button
                type="button"
                @click="form.is_public = false"
                class="p-4 rounded-lg border-2 transition text-left"
                :class="!form.is_public 
                  ? 'border-primary-600 bg-primary-900/20' 
                  : 'border-dark-700 hover:border-dark-600'"
              >
                <div class="flex items-center gap-3 mb-2">
                  <div class="w-10 h-10 rounded-lg bg-orange-600/20 flex items-center justify-center">
                    <svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                  </div>
                  <div>
                    <div class="font-bold">Privado</div>
                  </div>
                </div>
                <p class="text-xs text-dark-400">Requiere aprobación para unirse</p>
              </button>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex gap-4">
            <button
              type="submit"
              :disabled="loading"
              class="btn btn-primary flex-1"
            >
              {{ loading ? 'Creando...' : 'Crear Grupo' }}
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
import { ref, onMounted } from 'vue'
import api from '@/api/axios'

const emit = defineEmits(['close', 'created'])

const form = ref({
  name: '',
  description: '',
  game: null,
  icon: null,
  is_public: true
})

const games = ref([])
const previewIcon = ref(null)
const loading = ref(false)
const error = ref(null)

function handleIconChange(event) {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 2 * 1024 * 1024) {
      error.value = 'La imagen no puede superar los 2MB'
      return
    }
    form.value.icon = file
    previewIcon.value = URL.createObjectURL(file)
  }
}

async function handleSubmit() {
  loading.value = true
  error.value = null

  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('description', form.value.description)
    formData.append('is_public', form.value.is_public)
    
    if (form.value.game) {
      formData.append('game', form.value.game)
    }
    
    if (form.value.icon) {
      formData.append('icon', form.value.icon)
    }

    const response = await api.post('/community/groups/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    emit('created', response.data)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al crear el grupo'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const response = await api.get('/games/')
    games.value = response.data.results || response.data
  } catch (err) {
    console.error('Error loading games:', err)
  }
})
</script>
