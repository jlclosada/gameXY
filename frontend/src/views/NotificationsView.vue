<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-3xl font-display font-bold">Notificaciones</h1>
        <button
          v-if="notifications.length > 0 && unreadCount > 0"
          @click="markAllAsRead"
          class="btn btn-secondary"
        >
          Marcar todas como leídas
        </button>
      </div>

      <!-- Filter Tabs -->
      <div class="card mb-6">
        <div class="flex border-b border-dark-700">
          <button
            @click="filterType = 'all'"
            class="px-6 py-4 font-medium transition-colors"
            :class="filterType === 'all' 
              ? 'text-primary-400 border-b-2 border-primary-400' 
              : 'text-dark-400 hover:text-dark-200'"
          >
            Todas ({{ notifications.length }})
          </button>
          <button
            @click="filterType = 'unread'"
            class="px-6 py-4 font-medium transition-colors"
            :class="filterType === 'unread' 
              ? 'text-primary-400 border-b-2 border-primary-400' 
              : 'text-dark-400 hover:text-dark-200'"
          >
            No leídas ({{ unreadCount }})
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
        <p class="text-dark-400 mt-4">Cargando notificaciones...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredNotifications.length === 0" class="card p-12 text-center">
        <svg class="w-20 h-20 mx-auto mb-4 text-dark-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
        </svg>
        <p class="text-dark-300 font-medium text-lg mb-2">
          {{ filterType === 'unread' ? 'No tienes notificaciones sin leer' : 'No tienes notificaciones' }}
        </p>
        <p class="text-dark-500">
          {{ filterType === 'unread' ? '¡Estás al día!' : 'Te avisaremos cuando haya algo nuevo' }}
        </p>
      </div>

      <!-- Notifications List -->
      <div v-else class="space-y-3">
        <div
          v-for="notification in filteredNotifications"
          :key="notification.id"
          @click="handleNotificationClick(notification)"
          class="card p-5 hover:border-primary-500/50 transition-all cursor-pointer"
          :class="!notification.is_read && 'bg-primary-900/5 border-primary-500/30'"
        >
          <div class="flex gap-4">
            <!-- Sender Avatar or Icon -->
            <div class="flex-shrink-0">
              <div v-if="notification.sender" class="w-12 h-12 rounded-full overflow-hidden border-2 border-dark-700">
                <img
                  v-if="notification.sender.avatar"
                  :src="notification.sender.avatar"
                  :alt="notification.sender.username"
                  class="w-full h-full object-cover"
                >
                <div v-else class="w-full h-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold">
                  {{ notification.sender.username.charAt(0).toUpperCase() }}
                </div>
              </div>
              <div v-else class="w-12 h-12 rounded-full bg-primary-500/20 flex items-center justify-center text-2xl">
                {{ getNotificationIcon(notification.type) }}
              </div>
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between mb-1">
                <h3 class="font-semibold text-gray-200">{{ notification.title }}</h3>
                <div class="flex items-center gap-2 flex-shrink-0 ml-4">
                  <span class="text-xs text-dark-500">{{ formatTime(notification.created_at) }}</span>
                  <div v-if="!notification.is_read" class="w-2 h-2 rounded-full bg-primary-500"></div>
                </div>
              </div>
              
              <p class="text-sm text-dark-400 mb-2">{{ notification.message }}</p>
              
              <!-- Type Badge -->
              <div class="flex items-center gap-2">
                <span class="text-xs px-2 py-1 rounded bg-dark-700 text-dark-300">
                  {{ getTypeLabel(notification.type) }}
                </span>
                
                <!-- Action button for join requests -->
                <div v-if="notification.type === 'join_request' && notification.metadata" class="flex gap-2">
                  <button
                    @click.stop="approveRequest(notification)"
                    class="text-xs px-3 py-1 rounded bg-green-600 hover:bg-green-700 text-white transition"
                  >
                    ✓ Aprobar
                  </button>
                  <button
                    @click.stop="rejectRequest(notification)"
                    class="text-xs px-3 py-1 rounded bg-red-600 hover:bg-red-700 text-white transition"
                  >
                    ✗ Rechazar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()
const notifications = ref([])
const loading = ref(true)
const filterType = ref('all')

const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)

const filteredNotifications = computed(() => {
  if (filterType.value === 'unread') {
    return notifications.value.filter(n => !n.is_read)
  }
  return notifications.value
})

const getNotificationIcon = (type) => {
  const icons = {
    'comment_reply': '💬',
    'guide_like': '❤️',
    'guide_rating': '⭐',
    'achievement': '🏆',
    'new_guide_favorite_game': '📖',
    'new_follower': '👤',
    'system': '🔔',
    'post_reply': '📝',
    'group_post_comment': '💬',
    'join_request': '🚪',
    'join_approved': '✅',
    'join_rejected': '❌',
    'group_post': '📢'
  }
  return icons[type] || '🔔'
}

const getTypeLabel = (type) => {
  const labels = {
    'comment_reply': 'Respuesta a comentario',
    'guide_like': 'Me gusta',
    'guide_rating': 'Valoración',
    'achievement': 'Logro',
    'new_guide_favorite_game': 'Nueva guía',
    'new_follower': 'Nuevo seguidor',
    'system': 'Sistema',
    'post_reply': 'Respuesta en foro',
    'group_post_comment': 'Comentario en grupo',
    'join_request': 'Solicitud de grupo',
    'join_approved': 'Solicitud aprobada',
    'join_rejected': 'Solicitud rechazada',
    'group_post': 'Nueva publicación'
  }
  return labels[type] || 'Notificación'
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)

  if (diff < 60) return 'Hace un momento'
  if (diff < 3600) return `Hace ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `Hace ${Math.floor(diff / 3600)} h`
  if (diff < 604800) return `Hace ${Math.floor(diff / 86400)} d`
  
  return date.toLocaleDateString('es-ES', { 
    day: 'numeric', 
    month: 'short',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
  })
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

const handleNotificationClick = async (notification) => {
  // Mark as read
  if (!notification.is_read) {
    try {
      await api.post(`/auth/users/${notification.id}/mark_notification_read/`)
      notification.is_read = true
    } catch (error) {
      console.error('Error marking as read:', error)
    }
  }

  // Navigate if has action URL
  if (notification.action_url) {
    router.push(notification.action_url)
  }
}

const approveRequest = async (notification) => {
  if (!notification.metadata || !notification.metadata.request_id) return
  
  try {
    await api.post(`/community/groups/${notification.metadata.group_slug}/approve_request/`, {
      request_id: notification.metadata.request_id
    })
    
    // Mark as read and reload
    notification.is_read = true
    await loadNotifications()
    alert('Solicitud aprobada')
  } catch (error) {
    console.error('Error approving request:', error)
    alert(error.response?.data?.detail || 'Error al aprobar solicitud')
  }
}

const rejectRequest = async (notification) => {
  if (!notification.metadata || !notification.metadata.request_id) return
  
  try {
    await api.post(`/community/groups/${notification.metadata.group_slug}/reject_request/`, {
      request_id: notification.metadata.request_id
    })
    
    // Mark as read and reload
    notification.is_read = true
    await loadNotifications()
    alert('Solicitud rechazada')
  } catch (error) {
    console.error('Error rejecting request:', error)
    alert(error.response?.data?.detail || 'Error al rechazar solicitud')
  }
}

const markAllAsRead = async () => {
  try {
    await api.post('/auth/users/mark_all_notifications_read/')
    notifications.value.forEach(n => n.is_read = true)
  } catch (error) {
    console.error('Error marking all as read:', error)
  }
}

onMounted(() => {
  loadNotifications()
})
</script>
