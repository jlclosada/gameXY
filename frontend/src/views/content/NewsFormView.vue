<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="card p-8">
      <h1 class="text-3xl font-display font-bold mb-8">
        {{ isEdit ? 'Editar Noticia' : 'Crear Nueva Noticia' }}
      </h1>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Título -->
        <div>
          <label class="block text-sm font-medium mb-2">Título de la Noticia *</label>
          <input v-model="form.title" type="text" required class="input" placeholder="Título llamativo">
        </div>

        <!-- Slug -->
        <div>
          <label class="block text-sm font-medium mb-2">Slug (URL) *</label>
          <input v-model="form.slug" type="text" required class="input" placeholder="titulo-de-la-noticia">
          <p class="text-xs text-dark-400 mt-1">Se genera automáticamente pero puedes editarlo</p>
        </div>

        <!-- Excerpt -->
        <div>
          <label class="block text-sm font-medium mb-2">Resumen (Excerpt) *</label>
          <textarea v-model="form.excerpt" required maxlength="500" class="input min-h-[100px]" placeholder="Breve resumen de la noticia (máx 500 caracteres)"></textarea>
          <p class="text-xs text-dark-400 mt-1">{{ form.excerpt.length }}/500 caracteres</p>
        </div>

        <!-- Imagen destacada -->
        <div>
          <label class="block text-sm font-medium mb-2">Imagen Destacada</label>
          <input @change="handleFileChange" type="file" accept="image/*" class="input">
          <p class="text-xs text-dark-400 mt-1">Imagen principal que aparecerá en las tarjetas</p>
        </div>

        <!-- Juego relacionado -->
        <div>
          <label class="block text-sm font-medium mb-2">Juego Relacionado (Opcional)</label>
          <select v-model="form.game" class="input">
            <option value="">Sin juego asociado</option>
            <option v-for="game in games" :key="game.id" :value="game.id">
              {{ game.title }}
            </option>
          </select>
        </div>

        <!-- Editor de Contenido -->
        <div>
          <label class="block text-sm font-medium mb-2">Contenido de la Noticia *</label>
          <div class="mb-2 flex gap-2 flex-wrap border border-dark-600 rounded-lg p-2 bg-dark-700">
            <button type="button" @click="insertFormatting('**', '**')" class="px-3 py-1 bg-dark-600 rounded hover:bg-dark-500" title="Negrita">
              <strong>B</strong>
            </button>
            <button type="button" @click="insertFormatting('*', '*')" class="px-3 py-1 bg-dark-600 rounded hover:bg-dark-500" title="Cursiva">
              <em>I</em>
            </button>
            <button type="button" @click="insertFormatting('\n### ', '')" class="px-3 py-1 bg-dark-600 rounded hover:bg-dark-500" title="Título">
              H3
            </button>
            <button type="button" @click="insertFormatting('\n- ', '')" class="px-3 py-1 bg-dark-600 rounded hover:bg-dark-500" title="Lista">
              • List
            </button>
            <button type="button" @click="insertLink" class="px-3 py-1 bg-dark-600 rounded hover:bg-dark-500" title="Enlace">
              🔗 Link
            </button>
            <button type="button" @click="insertImage" class="px-3 py-1 bg-dark-600 rounded hover:bg-dark-500" title="Imagen">
              🖼️ Img
            </button>
          </div>
          <textarea 
            ref="contentEditor"
            v-model="form.content" 
            required 
            class="input min-h-[400px] font-mono text-sm"
            placeholder="Escribe el contenido de la noticia aquí. Puedes usar Markdown para dar formato."
          ></textarea>
          <p class="text-xs text-dark-400 mt-2">
            Usa Markdown para dar formato: **negrita**, *cursiva*, ### Títulos, [enlaces](url), etc.
          </p>
        </div>

        <!-- Vista previa -->
        <div v-if="form.content" class="border border-dark-600 rounded-lg p-6">
          <h3 class="font-semibold mb-4 text-primary-400">Vista Previa:</h3>
          <div class="prose prose-invert max-w-none" v-html="renderedContent"></div>
        </div>

        <!-- Publicado -->
        <div>
          <label class="flex items-center space-x-2">
            <input v-model="form.is_published" type="checkbox" class="rounded">
            <span>Publicar inmediatamente</span>
          </label>
          <p class="text-xs text-dark-400 mt-1">Si no se marca, se guardará como borrador</p>
        </div>

        <!-- Error mensaje -->
        <div v-if="error" class="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg">
          {{ error }}
        </div>

        <!-- Botones -->
        <div class="flex gap-4">
          <button type="submit" :disabled="loading" class="btn btn-primary flex-1">
            {{ loading ? 'Guardando...' : isEdit ? 'Actualizar Noticia' : 'Crear Noticia' }}
          </button>
          <button @click="$router.back()" type="button" class="btn btn-secondary">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { marked } from 'marked'
import api from '@/api/axios'

// Configurar marked
marked.setOptions({
  breaks: true,   // Convertir \n en <br>
  gfm: true       // GitHub Flavored Markdown
})

const router = useRouter()
const route = useRoute()

const isEdit = ref(false)
const loading = ref(false)
const error = ref(null)
const games = ref([])
const contentEditor = ref(null)

const form = ref({
  title: '',
  slug: '',
  excerpt: '',
  content: '',
  featured_image: null,
  game: '',
  is_published: true
})

// Auto-generar slug desde el título
watch(() => form.value.title, (newTitle) => {
  if (!isEdit.value && newTitle) {
    form.value.slug = newTitle
      .toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim()
  }
})

// Renderizado de Markdown usando marked (igual que en la vista de detalle)
const renderedContent = computed(() => {
  if (!form.value.content) return ''
  
  // Reemplazar saltos de línea simples con dobles después de cada párrafo
  let content = form.value.content
    .replace(/\n\n+/g, '\n\n')  // Normalizar múltiples saltos a dobles
    .replace(/(^|\n)([^\n#].+)\n([^\n#])/g, '$1$2\n\n$3')  // Añadir espacio entre líneas
  
  return marked(content)
})

function handleFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    form.value.featured_image = file
  }
}

function insertFormatting(before, after) {
  const textarea = contentEditor.value
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = form.value.content.substring(start, end)
  const newText = before + selectedText + after
  
  form.value.content = form.value.content.substring(0, start) + newText + form.value.content.substring(end)
  
  // Mantener el foco y selección
  textarea.focus()
  textarea.setSelectionRange(start + before.length, start + before.length + selectedText.length)
}

function insertLink() {
  const url = prompt('URL del enlace:')
  if (url) {
    const text = prompt('Texto del enlace:', url)
    insertFormatting(`[${text}](${url})`, '')
  }
}

function insertImage() {
  const url = prompt('URL de la imagen:')
  if (url) {
    const alt = prompt('Texto alternativo (opcional):', '')
    insertFormatting(`![${alt}](${url})`, '')
  }
}

async function handleSubmit() {
  loading.value = true
  error.value = null

  try {
    const formData = new FormData()
    
    formData.append('title', form.value.title)
    formData.append('slug', form.value.slug)
    formData.append('excerpt', form.value.excerpt)
    formData.append('content', form.value.content)
    formData.append('is_published', form.value.is_published)
    
    if (form.value.game) {
      formData.append('game', form.value.game)
    }
    
    if (form.value.featured_image instanceof File) {
      formData.append('featured_image', form.value.featured_image)
    }

    if (isEdit.value) {
      await api.put(`/content/news/${route.params.slug}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      await api.post('/content/news/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }

    router.push('/news')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al guardar la noticia'
    console.error('Error:', err.response?.data)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  // Cargar juegos para el selector
  try {
    const response = await api.get('/games/')
    games.value = response.data.results || []
  } catch (err) {
    console.error('Error loading games:', err)
  }

  // Si estamos editando, cargar la noticia
  if (route.params.slug) {
    isEdit.value = true
    try {
      const response = await api.get(`/content/news/${route.params.slug}/`)
      Object.assign(form.value, {
        title: response.data.title,
        slug: response.data.slug,
        excerpt: response.data.excerpt,
        content: response.data.content,
        game: response.data.game?.id || '',
        is_published: response.data.is_published
      })
    } catch (err) {
      error.value = 'Error al cargar la noticia'
    }
  }
})
</script>
