import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!user.value)

  async function login(email, password) {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/auth/login/', {
        email,
        password
      })
      
      const { access, refresh, user: userData } = response.data
      
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      user.value = userData
      
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al iniciar sesión'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/auth/users/', userData)
      // Guardar temporalmente las credenciales para login después de completar perfil
      sessionStorage.setItem('pendingEmail', userData.email)
      sessionStorage.setItem('pendingPassword', userData.password)
      return { success: true, userId: response.data.id }
    } catch (err) {
      error.value = err.response?.data || 'Error al registrarse'
      return { success: false }
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!localStorage.getItem('access_token')) return
    
    try {
      const response = await api.get('/auth/users/me/')
      user.value = response.data
    } catch (err) {
      logout()
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    // Redirect to login page
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    fetchUser,
    logout
  }
})
