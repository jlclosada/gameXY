<template>
  <div>
    <!-- Botón flotante de opciones -->
    <button
      @click="toggleMenu"
      class="fixed bottom-6 right-6 z-40 bg-primary-600 hover:bg-primary-700 text-white p-4 rounded-full shadow-2xl transition-all duration-300 transform hover:scale-110 focus:outline-none focus:ring-4 focus:ring-primary-500/50"
      :class="{ 'rotate-45': isOpen }"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
      </svg>
    </button>

    <!-- Overlay -->
    <Transition
      enter-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        @click="closeMenu"
        class="fixed inset-0 bg-black/60 backdrop-blur-sm z-30"
      ></div>
    </Transition>

    <!-- Sidebar de opciones -->
    <Transition
      enter-active-class="transition-transform duration-300 ease-out"
      enter-from-class="translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition-transform duration-300 ease-in"
      leave-from-class="translate-x-0"
      leave-to-class="translate-x-full"
    >
      <div
        v-if="isOpen"
        class="fixed top-0 right-0 h-full w-80 bg-dark-800 shadow-2xl z-40 overflow-y-auto border-l border-dark-700"
      >
        <!-- Header -->
        <div class="p-6 border-b border-dark-700">
          <div class="flex items-center justify-between">
            <h2 class="text-xl font-display font-bold">Opciones</h2>
            <button
              @click="closeMenu"
              class="text-dark-400 hover:text-white transition p-2 rounded-lg hover:bg-dark-700"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          
          <!-- Badge de rol -->
          <div v-if="authStore.user?.can_edit_content" class="mt-4 flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-primary-600/20 to-purple-600/20 rounded-lg border border-primary-500/30">
            <svg class="w-5 h-5 text-primary-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            <span class="text-sm font-semibold text-primary-300">
              {{ authStore.user?.is_admin ? 'Administrador' : 'GOAT' }}
            </span>
          </div>
        </div>

        <!-- Opciones -->
        <div class="p-4 space-y-2">
          <!-- Opciones para GOAT/Admin -->
          <template v-if="authStore.user?.can_edit_content">
            <div class="text-xs font-semibold text-dark-400 uppercase tracking-wider px-3 py-2">
              Gestión de Contenido
            </div>
            
            <button
              @click="openGameSearch"
              class="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-dark-700 rounded-lg transition group"
            >
              <svg class="w-5 h-5 text-primary-400 group-hover:text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
              <div>
                <div class="font-medium">Editar Juegos</div>
                <div class="text-xs text-dark-400">Buscar y modificar juegos</div>
              </div>
            </button>

            <button
              @click="openNewsSearch"
              class="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-dark-700 rounded-lg transition group"
            >
              <svg class="w-5 h-5 text-primary-400 group-hover:text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
              </svg>
              <div>
                <div class="font-medium">Editar Noticias</div>
                <div class="text-xs text-dark-400">Buscar y modificar noticias</div>
              </div>
            </button>

            <button
              @click="createGame"
              class="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-dark-700 rounded-lg transition group"
            >
              <svg class="w-5 h-5 text-green-400 group-hover:text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              <div>
                <div class="font-medium">Añadir Juego</div>
                <div class="text-xs text-dark-400">Crear nuevo juego</div>
              </div>
            </button>

            <RouterLink
              to="/news/new"
              @click="closeMenu"
              class="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-dark-700 rounded-lg transition group"
            >
              <svg class="w-5 h-5 text-green-400 group-hover:text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              <div>
                <div class="font-medium">Crear Noticia</div>
                <div class="text-xs text-dark-400">Publicar nueva noticia</div>
              </div>
            </RouterLink>
          </template>

          <!-- Opciones solo para Admin -->
          <template v-if="authStore.user?.is_admin">
            <div class="text-xs font-semibold text-dark-400 uppercase tracking-wider px-3 py-2 mt-4">
              Administración
            </div>
            
            <button
              @click="openRatingManager"
              class="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-dark-700 rounded-lg transition group"
            >
              <svg class="w-5 h-5 text-yellow-400 group-hover:text-yellow-300" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
              <div>
                <div class="font-medium">Gestionar Ratings</div>
                <div class="text-xs text-dark-400">Modificar valoraciones</div>
              </div>
            </button>

            <button
              @click="openFeaturedManager"
              class="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-dark-700 rounded-lg transition group"
            >
              <svg class="w-5 h-5 text-purple-400 group-hover:text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
              </svg>
              <div>
                <div class="font-medium">Gestionar Destacados</div>
                <div class="text-xs text-dark-400">Juegos featured</div>
              </div>
            </button>
          </template>

          <!-- Opciones para todos los usuarios autenticados -->
          <template v-if="authStore.isAuthenticated">
            <div class="text-xs font-semibold text-dark-400 uppercase tracking-wider px-3 py-2 mt-4">
              Contenido
            </div>

            <RouterLink
              to="/guides/new"
              @click="closeMenu"
              class="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-dark-700 rounded-lg transition group"
            >
              <svg class="w-5 h-5 text-blue-400 group-hover:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
              </svg>
              <div>
                <div class="font-medium">Publicar Guía</div>
                <div class="text-xs text-dark-400">Crear nueva guía de juego</div>
              </div>
            </RouterLink>
          </template>

          <!-- Opciones comunes -->
          <div class="text-xs font-semibold text-dark-400 uppercase tracking-wider px-3 py-2 mt-4">
            Cuenta
          </div>

          <RouterLink
            to="/profile"
            @click="closeMenu"
            class="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-dark-700 rounded-lg transition group"
          >
            <svg class="w-5 h-5 text-dark-400 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            <div>
              <div class="font-medium">Mi Perfil</div>
              <div class="text-xs text-dark-400">Ver mi cuenta</div>
            </div>
          </RouterLink>
        </div>
      </div>
    </Transition>

    <!-- Modales de búsqueda -->
    <SearchModal
      v-if="showGameSearch"
      type="games"
      @close="showGameSearch = false"
      @select="editGame"
    />

    <SearchModal
      v-if="showNewsSearch"
      type="news"
      @close="showNewsSearch = false"
      @select="editNews"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import SearchModal from './SearchModal.vue'

const router = useRouter()
const authStore = useAuthStore()

const isOpen = ref(false)
const showGameSearch = ref(false)
const showNewsSearch = ref(false)

function toggleMenu() {
  isOpen.value = !isOpen.value
}

function closeMenu() {
  isOpen.value = false
}

function openGameSearch() {
  showGameSearch.value = true
}

function openNewsSearch() {
  showNewsSearch.value = true
}

function openRatingManager() {
  closeMenu()
  router.push('/admin/ratings')
}

function openFeaturedManager() {
  closeMenu()
  router.push('/admin/featured')
}

function editGame(game) {
  showGameSearch.value = false
  closeMenu()
  router.push(`/games/${game.slug}/edit`)
}

function editNews(news) {
  showNewsSearch.value = false
  closeMenu()
  router.push(`/news/${news.slug}/edit`)
}

function createGame() {
  console.log('Navigating to /games/new')
  closeMenu()
  router.push('/games/new')
}
</script>
