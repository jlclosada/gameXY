<template>
  <nav class="bg-dark-900/95 backdrop-blur-md border-b border-dark-800 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-14">
        <!-- Logo -->
        <RouterLink to="/" class="group">
          <span class="text-xl font-display font-bold">
            <span class="text-white">Game</span><span class="bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">XY</span>
          </span>
        </RouterLink>

        <!-- Search Bar -->
        <div class="hidden md:block flex-1 max-w-md mx-4">
          <GlobalSearch />
        </div>

        <!-- Navigation Links (Desktop) -->
        <div class="hidden md:flex items-center space-x-1">
          <RouterLink to="/games" class="px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition">
            Juegos
          </RouterLink>
          <RouterLink to="/news" class="px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition">
            Noticias
          </RouterLink>
          <RouterLink to="/guides" class="px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition">
            Guías
          </RouterLink>
          <RouterLink to="/community" class="px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition">
            Comunidad
          </RouterLink>
        </div>

        <!-- Mobile Menu Button -->
        <button
          @click="showMobileMenu = !showMobileMenu"
          class="md:hidden p-2 text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>

        <!-- User Menu -->
        <div class="hidden md:flex items-center space-x-2">
          <template v-if="authStore.isAuthenticated">
            <!-- Notification Bell -->
            <NotificationBell />
            <!-- User Dropdown -->
            <div class="relative" ref="dropdownRef">
              <button
                @click="showDropdown = !showDropdown"
                class="flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition group"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                <span class="hidden sm:inline">{{ authStore.user?.username }}</span>
                <span v-if="authStore.user?.is_admin" class="badge badge-accent">
                  Admin
                </span>
                <span v-else-if="authStore.user?.is_goat" class="badge badge-primary">
                  GOAT
                </span>
                <svg class="w-4 h-4 transition-transform" :class="showDropdown && 'rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>

              <!-- Dropdown Menu -->
              <transition
                enter-active-class="transition ease-out duration-200 transform"
                enter-from-class="opacity-0 scale-95 -translate-y-2"
                enter-to-class="opacity-100 scale-100 translate-y-0"
                leave-active-class="transition ease-in duration-150 transform"
                leave-from-class="opacity-100 scale-100 translate-y-0"
                leave-to-class="opacity-0 scale-95 -translate-y-2"
              >
                <div
                  v-if="showDropdown"
                  class="absolute right-0 mt-2 w-56 bg-dark-850 border border-dark-700 rounded-lg shadow-xl py-2 z-50 origin-top-right"
                >
                <RouterLink
                  to="/profile"
                  @click="showDropdown = false"
                  class="flex items-center gap-3 px-4 py-2 text-sm text-gray-300 hover:bg-dark-800 hover:text-white transition"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                  Mi Perfil
                </RouterLink>

                <RouterLink
                  to="/saved-guides"
                  @click="showDropdown = false"
                  class="flex items-center gap-3 px-4 py-2 text-sm text-gray-300 hover:bg-dark-800 hover:text-white transition"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
                  </svg>
                  Guías Guardadas
                </RouterLink>

                <RouterLink
                  to="/favorite-games"
                  @click="showDropdown = false"
                  class="flex items-center gap-3 px-4 py-2 text-sm text-gray-300 hover:bg-dark-800 hover:text-white transition"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                  </svg>
                  Mis Juegos Favoritos
                </RouterLink>

                <RouterLink
                  to="/achievements"
                  @click="showDropdown = false"
                  class="flex items-center gap-3 px-4 py-2 text-sm text-gray-300 hover:bg-dark-800 hover:text-white transition"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                  </svg>
                  Mis Logros
                </RouterLink>

                <div class="border-t border-dark-700 my-2"></div>

                  <button
                    @click="handleLogout"
                    class="flex items-center gap-3 px-4 py-2 text-sm text-red-400 hover:bg-dark-800 hover:text-red-300 transition w-full text-left"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                    </svg>
                    Cerrar Sesión
                  </button>
                </div>
              </transition>
            </div>
          </template>
          <template v-else>
            <RouterLink to="/login" class="px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition">
              Iniciar sesión
            </RouterLink>
            <RouterLink to="/register" class="btn btn-primary text-sm">
              Registrarse
            </RouterLink>
          </template>
        </div>
      </div>
      
      <!-- Mobile Menu -->
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div
          v-if="showMobileMenu"
          class="md:hidden border-t border-dark-800 py-4"
        >
        <!-- Search Bar Mobile -->
        <div class="mb-4 px-2">
          <GlobalSearch />
        </div>
        
        <!-- Navigation Links Mobile -->
        <div class="space-y-1 px-2 mb-4">
          <RouterLink
            to="/games"
            @click="showMobileMenu = false"
            class="block px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition"
          >
            Juegos
          </RouterLink>
          <RouterLink
            to="/news"
            @click="showMobileMenu = false"
            class="block px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition"
          >
            Noticias
          </RouterLink>
          <RouterLink
            to="/guides"
            @click="showMobileMenu = false"
            class="block px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition"
          >
            Guías
          </RouterLink>
          <RouterLink
            to="/community"
            @click="showMobileMenu = false"
            class="block px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition"
          >
            Comunidad
          </RouterLink>
        </div>
        
        <!-- User Menu Mobile -->
        <div v-if="authStore.isAuthenticated" class="border-t border-dark-800 pt-4 px-2">
          <div class="flex items-center gap-3 px-3 py-2 mb-2">
            <div class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold">
              {{ authStore.user?.username?.[0]?.toUpperCase() }}
            </div>
            <div>
              <p class="font-medium text-white">{{ authStore.user?.username }}</p>
              <p class="text-xs text-dark-400">{{ authStore.user?.email }}</p>
            </div>
          </div>
          
          <div class="space-y-1">
            <RouterLink
              to="/profile"
              @click="showMobileMenu = false"
              class="flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-dark-800 hover:text-white transition rounded-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Mi Perfil
            </RouterLink>
            
            <RouterLink
              to="/notifications"
              @click="showMobileMenu = false"
              class="flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-dark-800 hover:text-white transition rounded-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
              Notificaciones
            </RouterLink>
            
            <RouterLink
              to="/saved-guides"
              @click="showMobileMenu = false"
              class="flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-dark-800 hover:text-white transition rounded-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
              </svg>
              Guías Guardadas
            </RouterLink>
            
            <RouterLink
              to="/favorite-games"
              @click="showMobileMenu = false"
              class="flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-dark-800 hover:text-white transition rounded-lg"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              </svg>
              Mis Juegos Favoritos
            </RouterLink>
            
            <RouterLink
              to="/achievements"
              @click="showMobileMenu = false"
              class="flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-dark-800 hover:text-white transition rounded-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
              </svg>
              Mis Logros
            </RouterLink>
            
            <button
              @click="handleLogoutMobile"
              class="flex items-center gap-3 px-3 py-2 text-sm text-red-400 hover:bg-dark-800 hover:text-red-300 transition w-full text-left rounded-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
              Cerrar Sesión
            </button>
          </div>
        </div>
        
        <div v-else class="border-t border-dark-800 pt-4 px-2 space-y-2">
          <RouterLink
            to="/login"
            @click="showMobileMenu = false"
            class="block px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition text-center"
          >
            Iniciar sesión
          </RouterLink>
          <RouterLink
            to="/register"
            @click="showMobileMenu = false"
            class="block btn btn-primary text-sm text-center"
          >
            Registrarse
          </RouterLink>
        </div>
        </div>
      </transition>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import GlobalSearch from '@/components/common/GlobalSearch.vue'
import NotificationBell from '@/components/common/NotificationBell.vue'

const authStore = useAuthStore()
const showDropdown = ref(false)
const showMobileMenu = ref(false)
const dropdownRef = ref(null)

const handleLogout = () => {
  showDropdown.value = false
  authStore.logout()
}

const handleLogoutMobile = () => {
  showMobileMenu.value = false
  authStore.logout()
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
