<template>
  <div class="relative min-h-screen">
    <!-- Hero Section -->
    <div class="relative h-[300px] overflow-hidden bg-gradient-to-br from-primary-900/20 via-dark-950 to-accent-900/20">
      <div class="absolute inset-0">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(139,92,246,0.15),transparent_70%)]"></div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-32 pb-12">
      <!-- Profile Card -->
      <div class="card-elevated p-8 mb-8">
        <div class="flex flex-col md:flex-row gap-8">
          <!-- Avatar Section -->
          <div class="flex-shrink-0">
            <div class="relative group">
              <div class="w-40 h-40 rounded-full overflow-hidden border-4 border-dark-800 shadow-2xl">
                <img 
                  v-if="user?.avatar" 
                  :src="user.avatar" 
                  :alt="user.username"
                  class="w-full h-full object-cover"
                >
                <div v-else class="w-full h-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white text-5xl font-bold">
                  {{ user?.username?.charAt(0).toUpperCase() }}
                </div>
              </div>
              <button 
                @click="avatarInput?.click()"
                class="absolute inset-0 bg-black/60 rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
              >
                <div class="text-center">
                  <svg class="w-8 h-8 text-white mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  <span class="text-white text-sm font-medium">Cambiar foto</span>
                </div>
              </button>
              <input 
                ref="avatarInput"
                type="file"
                @change="handleAvatarChange"
                accept="image/*"
                class="hidden"
              >
            </div>
          </div>

          <!-- Info Section -->
          <div class="flex-1">
            <div class="flex items-start justify-between mb-4">
              <div>
                <h1 class="text-3xl font-display font-bold mb-2">{{ user?.username }}</h1>
                <p class="text-gray-400 mb-3">{{ user?.email }}</p>
                <span 
                  v-if="user?.role"
                  class="badge text-xs px-3 py-1"
                  :class="user.role === 'goat' || user.role === 'admin' ? 'badge-primary' : 'badge-accent'"
                >
                  {{ getRoleLabel(user?.role) }}
                </span>
              </div>
            </div>

            <div v-if="user?.bio" class="mt-4 p-4 bg-dark-850 rounded-lg">
              <p class="text-gray-300 leading-relaxed">{{ user.bio }}</p>
            </div>
            <div v-else class="mt-4 p-4 bg-dark-850 rounded-lg border-2 border-dashed border-dark-700">
              <p class="text-gray-500 italic">No has agregado una biografía aún</p>
            </div>

            <!-- Recent Achievements -->
            <div v-if="recentAchievements.length > 0" class="mt-6 p-4 bg-dark-850/50 rounded-lg border border-primary-500/20">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider">🏆 Logros Recientes</h3>
                <RouterLink to="/achievements" class="text-xs text-primary-400 hover:text-primary-300">
                  Ver todos →
                </RouterLink>
              </div>
              <div class="flex gap-2 overflow-x-auto pb-2">
                <div 
                  v-for="achievement in recentAchievements"
                  :key="achievement.id"
                  class="flex-shrink-0 flex items-center gap-2 bg-dark-900 px-3 py-2 rounded-lg border border-dark-700"
                  :title="achievement.description"
                >
                  <span class="text-2xl">{{ achievement.icon }}</span>
                  <div class="min-w-0">
                    <p class="text-xs font-medium text-white truncate">{{ achievement.name }}</p>
                    <p class="text-xs text-yellow-400">+{{ achievement.points }} pts</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Stats -->
            <div class="grid grid-cols-3 gap-4 mt-6">
              <div class="text-center p-3 bg-dark-850 rounded-lg">
                <p class="text-2xl font-bold text-primary-400">{{ user?.guides_count || 0 }}</p>
                <p class="text-sm text-gray-400">Guías</p>
              </div>
              <div class="text-center p-3 bg-dark-850 rounded-lg">
                <p class="text-2xl font-bold text-accent-400">{{ user?.comments_count || 0 }}</p>
                <p class="text-sm text-gray-400">Comentarios</p>
              </div>
              <div class="text-center p-3 bg-dark-850 rounded-lg">
                <p class="text-2xl font-bold text-green-400">{{ user?.favorites_count || 0 }}</p>
                <p class="text-sm text-gray-400">Favoritos</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Sidebar with quick actions -->
        <div class="space-y-4">
          <div class="card p-4">
            <h3 class="font-display font-semibold mb-3">Configuración</h3>
            <div class="space-y-2">
              <button
                @click="activeSection = 'info'"
                class="w-full text-left px-4 py-2 rounded-lg transition"
                :class="activeSection === 'info' ? 'bg-primary-500/10 text-primary-400' : 'text-gray-400 hover:bg-dark-800'"
              >
                📋 Información Personal
              </button>
              <button
                @click="activeSection = 'security'"
                class="w-full text-left px-4 py-2 rounded-lg transition"
                :class="activeSection === 'security' ? 'bg-primary-500/10 text-primary-400' : 'text-gray-400 hover:bg-dark-800'"
              >
                🔒 Seguridad
              </button>
            </div>
          </div>

          <div class="card p-4">
            <h3 class="font-display font-semibold mb-2 text-sm text-gray-400">Miembro desde</h3>
            <p class="text-gray-300">{{ formatDate(user?.created_at) }}</p>
          </div>
        </div>

        <!-- Main Content Area -->
        <div class="lg:col-span-2">
          <!-- Información Personal -->
          <div v-if="activeSection === 'info'" class="card p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-2xl font-display font-bold">Información Personal</h2>
              <button
                v-if="!editMode"
                @click="enableEdit"
                class="btn btn-primary"
              >
                ✏️ Editar Perfil
              </button>
            </div>

            <form @submit.prevent="saveProfile" class="space-y-6">
              <!-- Username -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  Nombre de usuario
                </label>
                <input
                  v-model="form.username"
                  type="text"
                  disabled
                  class="input bg-dark-850 opacity-60 cursor-not-allowed"
                >
                <p class="text-xs text-gray-500 mt-1">El nombre de usuario no se puede modificar</p>
              </div>

              <!-- Email -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  Correo electrónico
                </label>
                <input
                  v-model="form.email"
                  type="email"
                  disabled
                  class="input bg-dark-850 opacity-60 cursor-not-allowed"
                >
                <p class="text-xs text-gray-500 mt-1">El correo no se puede modificar</p>
              </div>

              <!-- Bio -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  Biografía
                </label>
                <textarea
                  v-model="form.bio"
                  :disabled="!editMode"
                  rows="5"
                  maxlength="500"
                  class="input resize-none"
                  :class="!editMode && 'bg-dark-850 opacity-60 cursor-not-allowed'"
                  placeholder="Cuéntanos sobre ti, tus juegos favoritos, tu experiencia gaming..."
                ></textarea>
                <div class="flex justify-between mt-1">
                  <p class="text-xs text-gray-500">Máximo 500 caracteres</p>
                  <p class="text-xs" :class="form.bio?.length >= 500 ? 'text-red-400' : 'text-gray-500'">
                    {{ form.bio?.length || 0 }}/500
                  </p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div v-if="editMode" class="flex gap-3 pt-4 border-t border-dark-800">
                <button
                  type="button"
                  @click="cancelEdit"
                  class="btn btn-ghost flex-1"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="saving"
                  class="btn btn-primary flex-1"
                >
                  {{ saving ? 'Guardando...' : '💾 Guardar Cambios' }}
                </button>
              </div>
            </form>
          </div>

          <!-- Seguridad -->
          <div v-if="activeSection === 'security'" class="card p-6">
            <h2 class="text-2xl font-display font-bold mb-6">Cambiar Contraseña</h2>
            
            <form @submit.prevent="changePassword" class="space-y-6">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  Contraseña actual
                </label>
                <input
                  v-model="passwordForm.current_password"
                  type="password"
                  class="input"
                  required
                  placeholder="Ingresa tu contraseña actual"
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  Nueva contraseña
                </label>
                <input
                  v-model="passwordForm.new_password"
                  type="password"
                  class="input"
                  required
                  placeholder="Mínimo 8 caracteres"
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  Confirmar nueva contraseña
                </label>
                <input
                  v-model="passwordForm.confirm_password"
                  type="password"
                  class="input"
                  required
                  placeholder="Repite la nueva contraseña"
                >
              </div>

              <div class="pt-4 border-t border-dark-800">
                <button
                  type="submit"
                  :disabled="changingPassword"
                  class="btn btn-primary w-full"
                >
                  {{ changingPassword ? 'Cambiando...' : '🔒 Cambiar Contraseña' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const authStore = useAuthStore()
const user = ref(null)
const recentAchievements = ref([])
const activeSection = ref('info')
const editMode = ref(false)
const saving = ref(false)
const changingPassword = ref(false)
const avatarInput = ref(null)

const form = reactive({
  username: '',
  email: '',
  bio: ''
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const getRoleLabel = (role) => {
  const labels = {
    'user': 'Usuario',
    'goat': 'GOAT',
    'admin': 'Administrador'
  }
  return labels[role] || role
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const loadUserProfile = async () => {
  try {
    const response = await api.get('/auth/users/me/')
    user.value = response.data
    form.username = user.value.username
    form.email = user.value.email
    form.bio = user.value.bio || ''
    
    // Cargar logros recientes
    await loadRecentAchievements()
  } catch (error) {
    console.error('Error loading profile:', error)
  }
}

const loadRecentAchievements = async () => {
  try {
    const response = await api.get('/auth/users/achievements/')
    // Obtener los 3 últimos logros desbloqueados
    const unlocked = response.data.achievements
      .filter(a => a.unlocked)
      .sort((a, b) => new Date(b.unlocked_at) - new Date(a.unlocked_at))
      .slice(0, 3)
    recentAchievements.value = unlocked
  } catch (error) {
    console.error('Error loading achievements:', error)
  }
}

const enableEdit = () => {
  editMode.value = true
}

const cancelEdit = () => {
  editMode.value = false
  form.bio = user.value.bio || ''
}

const saveProfile = async () => {
  saving.value = true
  try {
    const response = await api.patch('/auth/users/update_profile/', {
      bio: form.bio
    })
    user.value = response.data
    authStore.user = response.data
    editMode.value = false
    alert('✅ Perfil actualizado correctamente')
  } catch (error) {
    console.error('Error updating profile:', error)
    alert(error.response?.data?.error || 'Error al actualizar el perfil')
  } finally {
    saving.value = false
  }
}

const changePassword = async () => {
  changingPassword.value = true
  try {
    await api.post('/auth/users/change_password/', passwordForm)
    alert('✅ Contraseña cambiada correctamente')
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (error) {
    console.error('Error changing password:', error)
    const errorMsg = error.response?.data?.error
    if (Array.isArray(errorMsg)) {
      alert('❌ ' + errorMsg.join('\n'))
    } else {
      alert('❌ ' + (errorMsg || 'Error al cambiar la contraseña'))
    }
  } finally {
    changingPassword.value = false
  }
}

const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('avatar', file)

  try {
    const response = await api.patch('/auth/users/update_profile/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    user.value = response.data
    authStore.user = response.data
    alert('✅ Foto de perfil actualizada')
  } catch (error) {
    console.error('Error uploading avatar:', error)
    alert('❌ Error al subir la foto')
  }
}

onMounted(() => {
  loadUserProfile()
})
</script>
