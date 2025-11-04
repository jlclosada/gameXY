<template>
  <div class="relative" ref="bellRef">
    <!-- Bell Button -->
    <button
      @click="toggleNotifications"
      class="relative p-2 text-gray-400 hover:text-white hover:bg-dark-850 rounded-lg transition"
      :class="{ 'bg-dark-850 text-white': showNotifications }"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
      </svg>
      
      <!-- Unread Badge -->
      <span 
        v-if="unreadCount > 0"
        class="absolute top-1 right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-xs font-bold text-white"
      >
        {{ unreadCount > 9 ? '9+' : unreadCount }}
      </span>
    </button>

    <!-- Notifications Dropdown -->
    <div
      v-if="showNotifications"
      class="absolute right-0 mt-2 w-96 bg-dark-850 border border-dark-700 rounded-lg shadow-2xl max-h-[600px] overflow-hidden z-50"
    >
      <!-- Header -->
      <div class="flex items-center justify-between p-4 border-b border-dark-800">
        <h3 class="font-display font-semibold text-lg">🔔 Notificaciones</h3>
        <button
          v-if="notifications.length > 0"
          @click="markAllAsRead"
          class="text-xs text-primary-400 hover:text-primary-300 font-medium"
        >
          Marcar todas como leídas
        </button>
      </div>

      <!-- Notifications List -->
      <div class="overflow-y-auto max-h-[500px]">
        <!-- Loading -->
        <div v-if="loading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
          <p class="text-gray-500 mt-3 text-sm">Cargando notificaciones...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="notifications.length === 0" class="p-8 text-center">
          <svg class="w-16 h-16 mx-auto mb-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
          </svg>
          <p class="text-gray-400 font-medium">No tienes notificaciones</p>
          <p class="text-gray-500 text-sm mt-1">Te avisaremos cuando haya algo nuevo</p>
        </div>

        <!-- Notifications -->
        <div v-else>
          <button
            v-for="notification in notifications"
            :key="notification.id"
            @click="handleNotificationClick(notification)"
            class="w-full text-left px-4 py-3 border-b border-dark-800 hover:bg-dark-800 transition"
            :class="!notification.is_read && 'bg-dark-800/50'"
          >
            <div class="flex gap-3">
              <!-- Sender Avatar -->
              <div v-if="notification.sender" class="flex-shrink-0">
                <div class="w-10 h-10 rounded-full overflow-hidden border-2 border-dark-700">
                  <img
                    v-if="notification.sender.avatar"
                    :src="notification.sender.avatar"
                    :alt="notification.sender.username"
                    class="w-full h-full object-cover"
                  >
                  <div v-else class="w-full h-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold text-sm">
                    {{ notification.sender.username.charAt(0).toUpperCase() }}
                  </div>
                </div>
              </div>
              
              <!-- Icon for system notifications -->
              <div v-else class="flex-shrink-0">
                <div class="w-10 h-10 rounded-full bg-primary-500/20 flex items-center justify-center text-2xl">
                  {{ getNotificationIcon(notification.type) }}
                </div>
              </div>

              <!-- Content -->
              <div class="flex-1 min-w-0">
                <p class="font-medium text-sm text-gray-200 mb-1">{{ notification.title }}</p>
                <p class="text-xs text-gray-400 line-clamp-2">{{ notification.message }}</p>
                <p class="text-xs text-gray-600 mt-1">{{ formatTime(notification.created_at) }}</p>
              </div>

              <!-- Unread Indicator -->
              <div v-if="!notification.is_read" class="flex-shrink-0">
                <div class="w-2 h-2 rounded-full bg-primary-500"></div>
              </div>
            </div>
          </button>
        </div>
      </div>

      <!-- Footer -->
      <div v-if="notifications.length > 0" class="p-3 border-t border-dark-800 text-center">
        <RouterLink
          to="/notifications"
          @click="showNotifications = false"
          class="text-sm text-primary-400 hover:text-primary-300 font-medium"
        >
          Ver todas las notificaciones →
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()
const showNotifications = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const loading = ref(false)
const bellRef = ref(null)

const getNotificationIcon = (type) => {
  const icons = {
    'comment_reply': '💬',
    'guide_like': '❤️',
    'guide_rating': '⭐',
    'achievement': '🏆',
    'new_guide_favorite_game': '📖',
    'new_follower': '👤',
    'system': '🔔'
  }
  return icons[type] || '🔔'
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000) // segundos

  if (diff < 60) return 'Hace un momento'
  if (diff < 3600) return `Hace ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `Hace ${Math.floor(diff / 3600)} h`
  if (diff < 604800) return `Hace ${Math.floor(diff / 86400)} d`
  
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
}

const loadNotifications = async () => {
  loading.value = true
  try {
    const response = await api.get('/auth/users/notifications/')
    notifications.value = response.data
  } catch (error) {
    console.error('Error loading notifications:', error)
  } finally {
    loading.value = false
  }
}

const loadUnreadCount = async () => {
  try {
    const response = await api.get('/auth/users/unread_notifications_count/')
    unreadCount.value = response.data.unread_count
  } catch (error) {
    console.error('Error loading unread count:', error)
  }
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value && notifications.value.length === 0) {
    loadNotifications()
  }
}

const handleNotificationClick = async (notification) => {
  // Marcar como leída
  if (!notification.is_read) {
    try {
      await api.post(`/auth/users/${notification.id}/mark_notification_read/`)
      notification.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    } catch (error) {
      console.error('Error marking as read:', error)
    }
  }

  // Navegar
  if (notification.action_url) {
    showNotifications.value = false
    router.push(notification.action_url)
  }
}

const markAllAsRead = async () => {
  try {
    await api.post('/auth/users/mark_all_notifications_read/')
    notifications.value.forEach(n => n.is_read = true)
    unreadCount.value = 0
  } catch (error) {
    console.error('Error marking all as read:', error)
  }
}

const handleClickOutside = (event) => {
  if (bellRef.value && !bellRef.value.contains(event.target)) {
    showNotifications.value = false
  }
}

// Polling para actualizar contador cada 30 segundos
let pollingInterval = null

onMounted(() => {
  loadUnreadCount()
  document.addEventListener('click', handleClickOutside)
  
  // Polling cada 30 segundos
  pollingInterval = setInterval(() => {
    loadUnreadCount()
  }, 30000)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }
})
</script>
