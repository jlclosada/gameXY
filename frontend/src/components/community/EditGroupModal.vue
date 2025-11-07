<template>
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="$emit('close')">
    <div class="card max-w-4xl w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-display font-bold">⚙️ Configuración del Grupo</h2>
          <button @click="$emit('close')" class="text-dark-400 hover:text-white transition">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Tabs -->
        <div class="flex gap-2 mb-6 border-b border-dark-700">
          <button
            @click="activeTab = 'general'"
            class="px-4 py-2 font-medium transition-colors"
            :class="activeTab === 'general' ? 'text-primary-400 border-b-2 border-primary-400' : 'text-dark-400 hover:text-dark-200'"
          >
            Personalización
          </button>
          <button
            @click="activeTab = 'members'"
            class="px-4 py-2 font-medium transition-colors"
            :class="activeTab === 'members' ? 'text-primary-400 border-b-2 border-primary-400' : 'text-dark-400 hover:text-dark-200'"
          >
            Miembros ({{ members.length }})
          </button>
        </div>

        <!-- General Tab -->
        <div v-if="activeTab === 'general'">
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
            >
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium mb-2">Descripción *</label>
            <textarea
              v-model="form.description"
              required
              class="input min-h-[120px]"
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

          <!-- Banner Upload -->
          <div>
            <label class="block text-sm font-medium mb-2">Banner del Grupo</label>
            <div class="space-y-3">
              <div class="w-full h-40 rounded-lg bg-dark-700 flex items-center justify-center overflow-hidden">
                <img v-if="previewBanner || group.banner" :src="previewBanner || group.banner" alt="Banner" class="w-full h-full object-cover" />
                <div v-else class="text-center text-dark-500">
                  <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  <p class="text-sm">Sin banner</p>
                </div>
              </div>
              <div class="flex gap-2">
                <input
                  type="file"
                  ref="bannerInput"
                  @change="handleBannerChange"
                  accept="image/*"
                  class="hidden"
                >
                <button
                  type="button"
                  @click="$refs.bannerInput.click()"
                  class="btn btn-secondary"
                >
                  Cambiar Banner
                </button>
                <button
                  v-if="previewBanner || group.banner"
                  type="button"
                  @click="removeBanner"
                  class="btn btn-secondary text-red-400"
                >
                  Eliminar
                </button>
              </div>
              <p class="text-xs text-dark-400">Recomendado: 1920x400px, JPG o PNG (máx. 5MB)</p>
            </div>
          </div>

          <!-- Icon Upload -->
          <div>
            <label class="block text-sm font-medium mb-2">Icono del Grupo</label>
            <div class="flex items-center gap-4">
              <div class="w-24 h-24 rounded-xl bg-dark-700 flex items-center justify-center overflow-hidden border-2 border-dark-600">
                <img v-if="previewIcon || group.icon" :src="previewIcon || group.icon" alt="Preview" class="w-full h-full object-cover" />
                <svg v-else class="w-12 h-12 text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                  Cambiar Icono
                </button>
                <p class="text-xs text-dark-400 mt-1">Cuadrado, JPG o PNG (máx. 2MB)</p>
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
                {{ loading ? 'Guardando...' : 'Guardar Cambios' }}
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

        <!-- Members Tab -->
        <div v-if="activeTab === 'members'">
          <div v-if="loadingMembers" class="text-center py-12">
            <div class="inline-block w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="member in members"
              :key="member.id"
              class="flex items-center justify-between p-4 bg-dark-800 rounded-lg hover:bg-dark-750 transition-all"
            >
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-full overflow-hidden bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold">
                  <img v-if="member.user.avatar" :src="member.user.avatar" :alt="member.user.username" class="w-full h-full object-cover">
                  <span v-else>{{ member.user.username.charAt(0).toUpperCase() }}</span>
                </div>
                <div>
                  <div class="font-semibold">{{ member.user.username }}</div>
                  <div class="text-sm text-dark-400">
                    <span :class="getRoleBadgeClass(member.role)" class="px-2 py-0.5 rounded text-xs">
                      {{ getRoleLabel(member.role) }}
                    </span>
                    <span class="ml-2 text-xs">Miembro desde {{ formatDate(member.joined_at) }}</span>
                  </div>
                </div>
              </div>

              <button
                v-if="member.user.id !== group.creator.id"
                @click="removeMember(member.user.id)"
                :disabled="removingMember === member.user.id"
                class="btn btn-sm bg-red-600/20 hover:bg-red-600/30 text-red-400 border-red-700"
              >
                {{ removingMember === member.user.id ? 'Eliminando...' : 'Eliminar' }}
              </button>
              <span v-else class="px-3 py-1 bg-primary-600 text-white text-sm rounded">👑 Creador</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'

const props = defineProps({
  group: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'updated'])

const form = ref({
  name: props.group.name,
  description: props.group.description,
  game: props.group.game,
  icon: null,
  banner: null,
  removeBannerFlag: false,
  is_public: props.group.is_public
})

const activeTab = ref('general')
const games = ref([])
const members = ref([])
const previewIcon = ref(null)
const previewBanner = ref(null)
const loading = ref(false)
const loadingMembers = ref(false)
const removingMember = ref(null)
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

function handleBannerChange(event) {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      error.value = 'El banner no puede superar los 5MB'
      return
    }
    form.value.banner = file
    form.value.removeBannerFlag = false
    previewBanner.value = URL.createObjectURL(file)
  }
}

function removeBanner() {
  form.value.banner = null
  form.value.removeBannerFlag = true
  previewBanner.value = null
}

function getRoleLabel(role) {
  const labels = {
    'admin': '👑 Administrador',
    'moderator': '🛡️ Moderador',
    'member': '👤 Miembro'
  }
  return labels[role] || role
}

function getRoleBadgeClass(role) {
  const classes = {
    'admin': 'bg-yellow-600/20 text-yellow-400',
    'moderator': 'bg-blue-600/20 text-blue-400',
    'member': 'bg-dark-600 text-dark-300'
  }
  return classes[role] || 'bg-dark-600 text-dark-300'
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

async function loadMembers() {
  loadingMembers.value = true
  try {
    const response = await api.get(`/community/groups/${props.group.slug}/members/`)
    members.value = response.data
  } catch (err) {
    console.error('Error loading members:', err)
  } finally {
    loadingMembers.value = false
  }
}

async function removeMember(userId) {
  if (!confirm('¿Estás seguro de que quieres eliminar este miembro del grupo?')) return

  removingMember.value = userId
  try {
    await api.post(`/community/groups/${props.group.slug}/remove_member/`, {
      user_id: userId
    })

    // Remove from local list
    members.value = members.value.filter(m => m.user.id !== userId)
    alert('Miembro eliminado correctamente')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al eliminar miembro')
  } finally {
    removingMember.value = null
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

    if (form.value.banner) {
      formData.append('banner', form.value.banner)
    } else if (form.value.removeBannerFlag) {
      formData.append('banner', '')
    }

    const response = await api.patch(`/community/groups/${props.group.slug}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    emit('updated', response.data)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al actualizar el grupo'
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

  // Load members
  await loadMembers()
})
</script>
