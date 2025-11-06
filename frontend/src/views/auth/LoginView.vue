<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950 flex items-center justify-center px-4 py-12">
    <!-- Decoraciones de fondo -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-primary-600/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-accent-600/10 rounded-full blur-3xl"></div>
    </div>
    
    <div class="relative z-10 w-full max-w-6xl grid md:grid-cols-2 gap-8 items-center">
      <!-- Sección Izquierda - Información -->
      <div class="hidden md:block space-y-6">
        <div class="space-y-4">
          <div class="inline-block px-4 py-2 bg-primary-600/20 border border-primary-500/30 rounded-full">
            <span class="text-primary-400 text-sm font-semibold">🎮 Tu comunidad gaming</span>
          </div>
          
          <h1 class="text-5xl md:text-6xl font-display font-bold leading-tight">
            Bienvenido de nuevo a
            <span class="block bg-gradient-to-r from-primary-400 via-accent-400 to-primary-400 bg-clip-text text-transparent">
              GameXY
            </span>
          </h1>
          
          <p class="text-xl text-dark-300 leading-relaxed">
            Conecta con gamers, descubre nuevos juegos, comparte guías y vive la mejor experiencia gaming.
          </p>
        </div>
        
        <!-- Features -->
        <div class="space-y-4 pt-6">
          <div class="flex items-start gap-3">
            <div class="p-2 bg-primary-600/20 rounded-lg">
              <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-white mb-1">Guías y Tutoriales</h3>
              <p class="text-sm text-dark-400">Aprende de los mejores jugadores y comparte tus conocimientos</p>
            </div>
          </div>
          
          <div class="flex items-start gap-3">
            <div class="p-2 bg-accent-600/20 rounded-lg">
              <svg class="w-6 h-6 text-accent-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-white mb-1">Comunidad Activa</h3>
              <p class="text-sm text-dark-400">Conecta con miles de gamers apasionados</p>
            </div>
          </div>
          
          <div class="flex items-start gap-3">
            <div class="p-2 bg-green-600/20 rounded-lg">
              <svg class="w-6 h-6 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-white mb-1">Sistema de Logros</h3>
              <p class="text-sm text-dark-400">Desbloquea logros y destaca en la comunidad</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Sección Derecha - Formulario -->
      <div class="card p-8 shadow-2xl">
        <div class="text-center mb-8">
          <div class="inline-block p-3 bg-primary-600/20 rounded-full mb-4">
            <svg class="w-10 h-10 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
            </svg>
          </div>
          <h2 class="text-3xl font-display font-bold mb-2">Iniciar Sesión</h2>
          <p class="text-dark-400">Continúa tu aventura gaming</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div v-if="authStore.error" class="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg text-sm flex items-start gap-2">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>{{ authStore.error }}</span>
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium mb-2 flex items-center gap-2">
              <svg class="w-4 h-4 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              Email
            </label>
            <input 
              id="email"
              v-model="form.email"
              type="email"
              required
              class="input"
              placeholder="tu@email.com"
              autocomplete="email"
            >
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium mb-2 flex items-center gap-2">
              <svg class="w-4 h-4 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              Contraseña
            </label>
            <div class="relative">
              <input 
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="input pr-12"
                placeholder="Tu contraseña"
                autocomplete="current-password"
              >
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-dark-400 hover:text-white transition"
              >
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                </svg>
              </button>
            </div>
          </div>
          
          <button 
            type="submit" 
            :disabled="authStore.loading"
            class="btn btn-primary w-full py-3 text-base font-semibold"
          >
            <svg v-if="!authStore.loading" class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
            </svg>
            <div v-else class="inline-block w-5 h-5 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            {{ authStore.loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
          </button>
        </form>
        
        <div class="mt-6 pt-6 border-t border-dark-700">
          <p class="text-center text-dark-400 text-sm">
            ¿No tienes cuenta? 
            <RouterLink to="/register" class="link font-semibold">
              Regístrate gratis
            </RouterLink>
          </p>
        </div>
        
        <!-- Stats rápidas -->
        <div class="mt-6 grid grid-cols-3 gap-4 pt-6 border-t border-dark-700">
          <div class="text-center">
            <div class="text-2xl font-bold text-primary-400">10K+</div>
            <div class="text-xs text-dark-500">Usuarios</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-accent-400">500+</div>
            <div class="text-xs text-dark-500">Juegos</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-green-400">2K+</div>
            <div class="text-xs text-dark-500">Guías</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const showPassword = ref(false)

async function handleLogin() {
  const success = await authStore.login(form.value.email, form.value.password)
  if (success) {
    router.push('/')
  }
}
</script>
