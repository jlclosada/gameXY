<template>
  <Teleport to="body">
    <!-- Overlay -->
    <Transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="true"
        @click="$emit('close')"
        class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50"
      ></div>
    </Transition>

    <!-- Modal -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 scale-95 translate-y-4"
      enter-to-class="opacity-100 scale-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 scale-100 translate-y-0"
      leave-to-class="opacity-0 scale-95 translate-y-4"
    >
      <div
        v-if="true"
        class="fixed inset-x-4 top-20 mx-auto max-w-2xl bg-dark-800 rounded-xl shadow-2xl z-50 border border-dark-700 overflow-hidden"
        @click.stop
      >
        <!-- Header -->
        <div class="p-6 border-b border-dark-700">
          <h3 class="text-xl font-display font-bold mb-4">
            {{ type === 'games' ? 'Buscar Juego' : 'Buscar Noticia' }}
          </h3>
          
          <!-- Buscador -->
          <div class="relative">
            <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input
              v-model="searchQuery"
              @input="search"
              type="text"
              class="input pl-10"
              :placeholder="`Buscar ${type === 'games' ? 'juego' : 'noticia'}...`"
              autofocus
            >
          </div>
        </div>

        <!-- Resultados -->
        <div class="max-h-96 overflow-y-auto">
          <div v-if="loading" class="p-8 text-center text-dark-400">
            <svg class="w-8 h-8 mx-auto animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <p class="mt-2">Buscando...</p>
          </div>

          <div v-else-if="results.length === 0 && searchQuery" class="p-8 text-center text-dark-400">
            <svg class="w-12 h-12 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <p>No se encontraron resultados</p>
          </div>

          <div v-else-if="results.length === 0" class="p-8 text-center text-dark-400">
            <svg class="w-12 h-12 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <p>Escribe para buscar</p>
          </div>

          <div v-else class="divide-y divide-dark-700">
            <button
              v-for="item in results"
              :key="item.id"
              @click="selectItem(item)"
              class="w-full p-4 hover:bg-dark-700 transition flex items-center gap-4 text-left group"
            >
              <div v-if="type === 'games'" class="w-16 h-20 rounded bg-dark-600 overflow-hidden flex-shrink-0">
                <img v-if="item.cover_image" :src="item.cover_image" :alt="item.title" class="w-full h-full object-cover">
                <div v-else class="w-full h-full flex items-center justify-center text-dark-500">
                  <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z"/>
                  </svg>
                </div>
              </div>

              <div class="flex-1 min-w-0">
                <h4 class="font-semibold group-hover:text-primary-400 transition truncate">
                  {{ item.title }}
                </h4>
                <p v-if="type === 'games' && item.developer" class="text-sm text-dark-400 truncate">
                  {{ item.developer }}
                </p>
                <p v-if="type === 'news' && item.excerpt" class="text-sm text-dark-400 line-clamp-2 mt-1">
                  {{ item.excerpt }}
                </p>
              </div>

              <svg class="w-5 h-5 text-dark-500 group-hover:text-primary-400 transition flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Footer -->
        <div class="p-4 border-t border-dark-700 bg-dark-900/50">
          <button
            @click="$emit('close')"
            class="w-full btn btn-secondary"
          >
            Cancelar
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '@/api/axios'

const props = defineProps({
  type: {
    type: String,
    required: true,
    validator: (value) => ['games', 'news'].includes(value)
  }
})

const emit = defineEmits(['close', 'select'])

const searchQuery = ref('')
const results = ref([])
const loading = ref(false)

let searchTimeout = null

watch(searchQuery, () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  if (!searchQuery.value.trim()) {
    results.value = []
    return
  }

  searchTimeout = setTimeout(() => {
    search()
  }, 300)
})

async function search() {
  if (!searchQuery.value.trim()) {
    results.value = []
    return
  }

  loading.value = true
  
  try {
    const endpoint = props.type === 'games' ? '/games/' : '/content/news/'
    const response = await api.get(endpoint, {
      params: {
        search: searchQuery.value,
        page_size: 20
      }
    })
    
    results.value = response.data.results || []
  } catch (error) {
    console.error('Error searching:', error)
    results.value = []
  } finally {
    loading.value = false
  }
}

function selectItem(item) {
  emit('select', item)
}
</script>
