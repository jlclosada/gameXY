<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="card p-8">
      <h1 class="text-3xl font-display font-bold mb-8">
        {{ isEditing ? 'Editar Guía' : 'Crear Nueva Guía' }}
      </h1>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Selector de Juego -->
        <div>
          <label class="block text-sm font-medium mb-2">Juego *</label>
          <select v-model="form.game" class="input" required :disabled="isEditing">
            <option value="">Selecciona un juego</option>
            <option v-for="game in games" :key="game.id" :value="game.id">
              {{ game.title }}
            </option>
          </select>
        </div>

        <!-- Título -->
        <div>
          <label class="block text-sm font-medium mb-2">Título *</label>
          <input v-model="form.title" type="text" class="input" required placeholder="Título de la guía">
        </div>

        <!-- Descripción -->
        <div>
          <label class="block text-sm font-medium mb-2">Descripción corta *</label>
          <textarea 
            v-model="form.description" 
            class="input" 
            rows="3" 
            required 
            maxlength="500"
            placeholder="Breve descripción de la guía"
          ></textarea>
          <p class="text-xs text-gray-500 mt-1">{{ form.description.length }}/500 caracteres</p>
        </div>

        <!-- Dificultad -->
        <div>
          <label class="block text-sm font-medium mb-2">Dificultad *</label>
          <select v-model="form.difficulty" class="input" required>
            <option value="beginner">Principiante</option>
            <option value="intermediate">Intermedio</option>
            <option value="advanced">Avanzado</option>
          </select>
        </div>

        <!-- URL del video -->
        <div>
          <label class="block text-sm font-medium mb-2">URL de video (opcional)</label>
          <input 
            v-model="form.video_url" 
            type="url" 
            class="input" 
            placeholder="https://youtube.com/watch?v=..."
          >
        </div>

        <!-- Thumbnail -->
        <div>
          <label class="block text-sm font-medium mb-2">Imagen de portada (opcional)</label>
          <input 
            type="file" 
            @change="handleFileChange" 
            accept="image/*"
            class="input"
          >
          <p v-if="form.thumbnail && typeof form.thumbnail === 'string'" class="text-xs text-gray-500 mt-1">
            Imagen actual: {{ form.thumbnail }}
          </p>
        </div>

        <!-- Editor de contenido -->
        <div>
          <label class="block text-sm font-medium mb-2">Contenido *</label>
          <RichTextEditor v-model="form.content" />
        </div>

        <!-- Botones -->
        <div class="flex gap-4 justify-end">
          <button type="button" @click="$router.back()" class="btn btn-secondary">
            Cancelar
          </button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Publicar') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import RichTextEditor from '@/components/editor/RichTextEditor.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const games = ref([])
const loading = ref(false)
const isEditing = computed(() => !!route.params.slug)

const form = ref({
  game: '',
  title: '',
  description: '',
  difficulty: 'beginner',
  video_url: '',
  thumbnail: null,
  content: '',
  slug: ''
})

onMounted(async () => {
  // Cargar juegos
  try {
    const response = await api.get('/games/')
    console.log('Games for guide form:', response.data)
    // Manejar tanto respuestas paginadas como arrays directos
    games.value = Array.isArray(response.data) ? response.data : (response.data.results || [])
    console.log('Loaded games:', games.value.length)
  } catch (error) {
    console.error('Error loading games:', error)
    alert('Error al cargar los juegos. Por favor, recarga la página.')
  }

  // Si estamos editando, cargar la guía
  if (isEditing.value) {
    try {
      const response = await api.get(`/content/guides/${route.params.slug}/`)
      const guide = response.data
      form.value = {
        game: guide.game?.id || guide.game,
        title: guide.title,
        description: guide.description,
        difficulty: guide.difficulty,
        video_url: guide.video_url || '',
        thumbnail: guide.thumbnail,
        content: guide.content,
        slug: guide.slug
      }
    } catch (error) {
      console.error('Error loading guide:', error)
      router.push('/guides')
    }
  }
})

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    form.value.thumbnail = file
  }
}

const handleSubmit = async () => {
  if (!authStore.isAuthenticated) {
    alert('Debes iniciar sesión para crear una guía')
    router.push('/login')
    return
  }

  // Validación
  if (!form.value.game) {
    alert('Por favor selecciona un juego')
    return
  }
  if (!form.value.title.trim()) {
    alert('Por favor ingresa un título')
    return
  }
  if (!form.value.description.trim()) {
    alert('Por favor ingresa una descripción')
    return
  }
  if (!form.value.content.trim()) {
    alert('Por favor ingresa el contenido de la guía')
    return
  }

  loading.value = true

  try {
    const formData = new FormData()
    formData.append('game', form.value.game)
    formData.append('title', form.value.title.trim())
    formData.append('description', form.value.description.trim())
    formData.append('difficulty', form.value.difficulty)
    formData.append('content', form.value.content)
    
    if (form.value.video_url) {
      formData.append('video_url', form.value.video_url)
    }
    
    if (form.value.thumbnail && typeof form.value.thumbnail !== 'string') {
      formData.append('thumbnail', form.value.thumbnail)
    }

    // Generar slug automático si es nueva guía
    if (!isEditing.value) {
      const slug = form.value.title
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '') // Eliminar acentos
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '')
      formData.append('slug', slug)
    }

    console.log('Submitting guide...', {
      game: form.value.game,
      title: form.value.title,
      isEditing: isEditing.value
    })

    let response
    if (isEditing.value) {
      response = await api.patch(`/content/guides/${form.value.slug}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      response = await api.post('/content/guides/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }

    console.log('Guide saved successfully:', response.data)
    router.push(`/guides/${response.data.slug}`)
  } catch (error) {
    console.error('Error saving guide:', error)
    console.error('Error response:', error.response?.data)
    
    // Mostrar error más descriptivo
    let errorMessage = 'Error al guardar la guía'
    if (error.response?.data) {
      const errors = error.response.data
      if (typeof errors === 'object') {
        errorMessage = Object.entries(errors)
          .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
          .join('\n')
      } else {
        errorMessage = errors.detail || errors.toString()
      }
    }
    alert(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>
