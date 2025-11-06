<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950 flex items-center justify-center px-4 py-12">
    <!-- Decoraciones de fondo -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 right-10 w-72 h-72 bg-accent-600/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 left-10 w-96 h-96 bg-primary-600/10 rounded-full blur-3xl"></div>
    </div>
    
    <div class="relative z-10 w-full max-w-6xl grid md:grid-cols-2 gap-8 items-center">
      <!-- Sección Derecha - Formulario (en mobile aparece primero) -->
      <div class="card p-8 shadow-2xl order-2 md:order-1">
        <div class="text-center mb-8">
          <div class="inline-block p-3 bg-accent-600/20 rounded-full mb-4">
            <svg class="w-10 h-10 text-accent-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
            </svg>
          </div>
          <h2 class="text-3xl font-display font-bold mb-2">Crear Cuenta</h2>
          <p class="text-dark-400">Comienza tu aventura gaming hoy</p>
        </div>
        
        <form @submit.prevent="handleRegister" class="space-y-6">
          <div v-if="authStore.error" class="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg text-sm flex items-start gap-2">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>{{ typeof authStore.error === 'string' ? authStore.error : 'Error al registrarse' }}</span>
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
            <p class="text-xs text-dark-500 mt-1">Usaremos tu email para iniciar sesión</p>
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
                minlength="8"
                class="input pr-12"
                placeholder="Mínimo 8 caracteres"
                autocomplete="new-password"
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
            <div class="mt-2 space-y-1">
              <div class="flex items-center gap-2 text-xs" :class="form.password.length >= 8 ? 'text-green-400' : 'text-dark-500'">
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                Al menos 8 caracteres
              </div>
            </div>
          </div>
          
          <div class="bg-dark-800/50 p-4 rounded-lg border border-dark-700">
            <p class="text-xs text-dark-400">
              Al registrarte, aceptas nuestros Términos de Servicio y Política de Privacidad. Después del registro, podrás completar tu perfil con más información.
            </p>
          </div>
          
          <button 
            type="button"
            :disabled="authStore.loading"
            class="btn btn-primary w-full py-3 text-base font-semibold"
            @click="handleRegister"
          >
            <svg v-if="!authStore.loading" class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
            </svg>
            <div v-else class="inline-block w-5 h-5 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            {{ authStore.loading ? 'Creando cuenta...' : 'Crear Cuenta Gratis' }}
          </button>
        </form>
        
        <div class="mt-6 pt-6 border-t border-dark-700">
          <p class="text-center text-dark-400 text-sm">
            ¿Ya tienes cuenta? 
            <RouterLink to="/login" class="link font-semibold">
              Inicia sesión
            </RouterLink>
          </p>
        </div>
      </div>
      
      <!-- Sección Izquierda - Información -->
      <div class="hidden md:block space-y-6 order-1 md:order-2">
        <div class="space-y-4">
          <div class="inline-block px-4 py-2 bg-accent-600/20 border border-accent-500/30 rounded-full">
            <span class="text-accent-400 text-sm font-semibold">✨ Únete a la comunidad</span>
          </div>
          
          <h1 class="text-5xl md:text-6xl font-display font-bold leading-tight">
            Crea tu cuenta en
            <span class="block bg-gradient-to-r from-accent-400 via-primary-400 to-accent-400 bg-clip-text text-transparent">
              GameXY
            </span>
          </h1>
          
          <p class="text-xl text-dark-300 leading-relaxed">
            Únete a miles de gamers, comparte tus experiencias y descubre el mejor contenido gaming.
          </p>
        </div>
        
        <!-- Benefits -->
        <div class="space-y-4 pt-6">
          <div class="flex items-start gap-3">
            <div class="p-2 bg-green-600/20 rounded-lg">
              <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-white mb-1">100% Gratis</h3>
              <p class="text-sm text-dark-400">Sin costos ocultos ni suscripciones</p>
            </div>
          </div>
          
          <div class="flex items-start gap-3">
            <div class="p-2 bg-accent-600/20 rounded-lg">
              <svg class="w-6 h-6 text-accent-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-white mb-1">Registro Rápido</h3>
              <p class="text-sm text-dark-400">Solo necesitas email y contraseña para empezar</p>
            </div>
          </div>
          
          <div class="flex items-start gap-3">
            <div class="p-2 bg-primary-600/20 rounded-lg">
              <svg class="w-6 h-6 text-primary-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-white mb-1">Perfil Personalizado</h3>
              <p class="text-sm text-dark-400">Personaliza tu perfil con tus juegos y géneros favoritos</p>
            </div>
          </div>
        </div>
        
        <!-- Testimonial -->
        <div class="mt-8 bg-dark-800/50 p-6 rounded-lg border border-dark-700">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold text-lg">
              GX
            </div>
            <div class="flex-1">
              <p class="text-dark-300 text-sm italic mb-2">
                "La mejor plataforma para conectar con otros gamers y aprender de las mejores guías. ¡Totalmente recomendada!"
              </p>
              <p class="text-dark-500 text-xs">
                - Usuario de GameXY
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const showPassword = ref(false)

const isFormValid = computed(() => {
  const valid = form.value.email.trim() !== '' && form.value.password.length >= 8
  console.log('isFormValid:', valid, 'email:', form.value.email, 'password length:', form.value.password.length)
  return valid
})

console.log('RegisterView component loaded')

async function handleRegister() {
  console.log('handleRegister called with:', form.value)
  try {
    const result = await authStore.register(form.value)
    console.log('Register result:', result)
    if (result.success) {
      console.log('Account created, redirecting to complete profile')
      router.push('/complete-profile')
    }
  } catch (error) {
    console.error('Register error:', error)
  }
}
</script>
