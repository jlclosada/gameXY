<template>
  <div class="min-h-[80vh] flex items-center justify-center px-4 py-12">
    <div class="card max-w-md w-full p-8">
      <h1 class="text-3xl font-display font-bold text-center mb-8">Crear Cuenta</h1>
      
      <form @submit.prevent="handleRegister" class="space-y-6">
        <div v-if="authStore.error" class="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg text-sm">
          {{ typeof authStore.error === 'string' ? authStore.error : 'Error al registrarse' }}
        </div>
        
        <div>
          <label for="username" class="block text-sm font-medium mb-2">Usuario</label>
          <input 
            id="username"
            v-model="form.username"
            type="text"
            required
            class="input"
            placeholder="Tu nombre de usuario"
          >
        </div>
        
        <div>
          <label for="email" class="block text-sm font-medium mb-2">Email</label>
          <input 
            id="email"
            v-model="form.email"
            type="email"
            required
            class="input"
            placeholder="tu@email.com"
          >
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium mb-2">Contraseña</label>
          <input 
            id="password"
            v-model="form.password"
            type="password"
            required
            class="input"
            placeholder="Mínimo 8 caracteres"
          >
        </div>
        
        <button 
          type="submit" 
          :disabled="authStore.loading"
          class="btn btn-primary w-full py-3"
        >
          {{ authStore.loading ? 'Creando cuenta...' : 'Crear Cuenta' }}
        </button>
      </form>
      
      <p class="text-center text-dark-400 text-sm mt-6">
        ¿Ya tienes cuenta? 
        <RouterLink to="/login" class="link">Inicia sesión aquí</RouterLink>
      </p>
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
  username: '',
  email: '',
  password: ''
})

async function handleRegister() {
  const success = await authStore.register(form.value)
  if (success) {
    router.push('/')
  }
}
</script>
