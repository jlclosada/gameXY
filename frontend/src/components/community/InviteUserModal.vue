<template>
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="$emit('close')">
    <div class="card max-w-lg w-full">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-display font-bold">Invitar Usuario</h2>
          <button @click="$emit('close')" class="text-dark-400 hover:text-white transition">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div v-if="error" class="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg text-sm mb-4">
          {{ error }}
        </div>

        <div v-if="success" class="bg-green-900/20 border border-green-700 text-green-400 px-4 py-3 rounded-lg text-sm mb-4">
          {{ success }}
        </div>

        <!-- User Search -->
        <div class="mb-6">
          <label class="block text-sm font-medium mb-2">Buscar usuario</label>
          <div class="relative">
            <input
              v-model="searchQuery"
              @input="searchUsers"
              type="text"
              placeholder="Escribe el nombre de usuario..."
              class="input pl-10"
            >
            <svg class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="searching" class="text-center py-8">
          <div class="inline-block w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
        </div>

        <!-- Search Results -->
        <div v-else-if="searchResults.length > 0" class="space-y-2 mb-6 max-h-64 overflow-y-auto">
          <button
            v-for="user in searchResults"
            :key="user.id"
            @click="selectUser(user)"
            class="w-full flex items-center gap-3 p-3 rounded-lg transition"
            :class="selectedUser?.id === user.id ? 'bg-primary-900/30 border-2 border-primary-500' : 'bg-dark-800 hover:bg-dark-700'"
          >
            <div class="w-10 h-10 rounded-full overflow-hidden bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold flex-shrink-0">
              <img v-if="user.avatar" :src="user.avatar" :alt="user.username" class="w-full h-full object-cover">
              <span v-else>{{ user.username.charAt(0).toUpperCase() }}</span>
            </div>
            <div class="flex-1 text-left">
              <p class="font-medium">{{ user.username }}</p>
              <p class="text-xs text-dark-400">{{ user.email }}</p>
            </div>
            <svg v-if="selectedUser?.id === user.id" class="w-6 h-6 text-primary-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="searchQuery.length >= 2 && !searching" class="text-center py-8 text-dark-400">
          <svg class="w-16 h-16 mx-auto mb-3 text-dark-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          <p>No se encontraron usuarios</p>
        </div>

        <!-- Help Text -->
        <div v-else-if="searchQuery.length < 2" class="text-center py-8 text-dark-400">
          <p class="text-sm">Escribe al menos 2 caracteres para buscar</p>
        </div>

        <!-- Message -->
        <div v-if="selectedUser" class="mb-6">
          <label class="block text-sm font-medium mb-2">Mensaje (opcional)</label>
          <textarea
            v-model="message"
            class="input min-h-[80px]"
            placeholder="Escribe un mensaje de invitación..."
          ></textarea>
        </div>

        <!-- Actions -->
        <div class="flex gap-4">
          <button
            @click="sendInvitation"
            :disabled="!selectedUser || loading"
            class="btn btn-primary flex-1"
          >
            {{ loading ? 'Enviando...' : 'Enviar Invitación' }}
          </button>
          <button
            @click="$emit('close')"
            class="btn btn-secondary"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/axios'

const props = defineProps({
  group: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'invited'])

const searchQuery = ref('')
const searchResults = ref([])
const selectedUser = ref(null)
const message = ref('')
const searching = ref(false)
const loading = ref(false)
const error = ref(null)
const success = ref(null)

let searchTimeout = null

async function searchUsers() {
  error.value = null
  success.value = null
  
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    return
  }

  // Debounce search
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    searching.value = true
    try {
      const response = await api.get('/auth/users/search/', {
        params: { q: searchQuery.value }
      })
      searchResults.value = response.data.results || []
    } catch (err) {
      console.error('Error searching users:', err)
      error.value = 'Error al buscar usuarios'
    } finally {
      searching.value = false
    }
  }, 300)
}

function selectUser(user) {
  selectedUser.value = user
}

async function sendInvitation() {
  if (!selectedUser.value) return
  
  loading.value = true
  error.value = null
  success.value = null

  try {
    await api.post(`/community/groups/${props.group.slug}/invite_user/`, {
      user_id: selectedUser.value.id,
      message: message.value
    })

    success.value = `Invitación enviada a ${selectedUser.value.username}`
    
    // Reset form
    setTimeout(() => {
      emit('invited')
      emit('close')
    }, 1500)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al enviar la invitación'
  } finally {
    loading.value = false
  }
}
</script>
