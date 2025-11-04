<template>
  <div class="min-h-screen bg-gradient-to-b from-dark-950 via-dark-900 to-dark-950">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-display font-bold mb-4 bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 bg-clip-text text-transparent">
          🏆 Logros y Recompensas
        </h1>
        <p class="text-gray-400 text-lg">Completa desafíos y desbloquea logros épicos</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="text-center">
          <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-500 mx-auto mb-4"></div>
          <p class="text-gray-400">Cargando logros...</p>
        </div>
      </div>

      <div v-else>
        <!-- Progress Overview -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <!-- Total Points -->
          <div class="card-elevated p-6 text-center">
            <div class="text-5xl font-bold text-yellow-400 mb-2">{{ progress.total_points }}</div>
            <p class="text-gray-400 text-sm uppercase tracking-wider">Puntos Totales</p>
          </div>

          <!-- Unlocked -->
          <div class="card-elevated p-6 text-center">
            <div class="text-5xl font-bold text-green-400 mb-2">
              {{ progress.unlocked_count }}/{{ progress.total_achievements }}
            </div>
            <p class="text-gray-400 text-sm uppercase tracking-wider">Desbloqueados</p>
          </div>

          <!-- Progress Bar -->
          <div class="card-elevated p-6">
            <div class="mb-2 flex justify-between text-sm">
              <span class="text-gray-400">Progreso</span>
              <span class="text-primary-400 font-bold">{{ progressPercentage }}%</span>
            </div>
            <div class="w-full bg-dark-800 rounded-full h-4 overflow-hidden">
              <div 
                class="h-full bg-gradient-to-r from-primary-500 to-accent-500 rounded-full transition-all duration-500"
                :style="{ width: `${progressPercentage}%` }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Check Achievements Button -->
        <div class="text-center mb-8">
          <button
            @click="checkAchievements"
            :disabled="checking"
            class="btn btn-primary inline-flex items-center gap-2"
          >
            <svg v-if="!checking" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <div v-else class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            {{ checking ? 'Verificando...' : '🔍 Verificar Logros Disponibles' }}
          </button>
        </div>

        <!-- Newly Unlocked Achievements -->
        <div v-if="newlyUnlocked.length > 0" class="mb-8">
          <div class="card bg-gradient-to-r from-yellow-500/10 to-orange-500/10 border-2 border-yellow-500/30 p-6">
            <h3 class="text-xl font-display font-bold mb-4 text-yellow-400">🎉 ¡Nuevos Logros Desbloqueados!</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                v-for="achievement in newlyUnlocked"
                :key="achievement.id"
                class="flex items-center gap-3 bg-dark-850 p-3 rounded-lg animate-pulse-slow"
              >
                <div class="text-4xl">{{ achievement.icon }}</div>
                <div class="flex-1">
                  <p class="font-bold text-white">{{ achievement.name }}</p>
                  <p class="text-sm text-gray-400">+{{ achievement.points }} puntos</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Categories Tabs -->
        <div class="flex flex-wrap gap-2 mb-8">
          <button
            @click="selectedCategory = 'all'"
            class="px-4 py-2 rounded-lg font-medium transition"
            :class="selectedCategory === 'all' ? 'bg-primary-500 text-white' : 'bg-dark-850 text-gray-400 hover:bg-dark-800'"
          >
            Todos
          </button>
          <button
            v-for="category in categories"
            :key="category.value"
            @click="selectedCategory = category.value"
            class="px-4 py-2 rounded-lg font-medium transition"
            :class="selectedCategory === category.value ? 'bg-primary-500 text-white' : 'bg-dark-850 text-gray-400 hover:bg-dark-800'"
          >
            {{ category.icon }} {{ category.label }}
          </button>
        </div>

        <!-- Achievements Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="achievement in filteredAchievements"
            :key="achievement.id"
            class="card-elevated group relative overflow-hidden"
            :class="achievement.unlocked ? 'border-2 border-primary-500/30' : 'opacity-75'"
          >
            <!-- Unlock Glow Effect -->
            <div
              v-if="achievement.unlocked"
              class="absolute inset-0 bg-gradient-to-br from-primary-500/10 to-transparent pointer-events-none"
            ></div>

            <div class="p-6 relative z-10">
              <!-- Icon and Status -->
              <div class="flex items-start justify-between mb-4">
                <div 
                  class="text-6xl transform transition-transform group-hover:scale-110"
                  :class="!achievement.unlocked && 'grayscale opacity-50'"
                >
                  {{ achievement.icon }}
                </div>
                <div v-if="achievement.unlocked" class="flex flex-col items-end">
                  <span class="badge badge-primary text-xs px-2 py-1">Desbloqueado</span>
                  <span class="text-xs text-gray-500 mt-1">
                    {{ formatDate(achievement.unlocked_at) }}
                  </span>
                </div>
                <div v-else class="flex flex-col items-end">
                  <span class="badge badge-secondary text-xs px-2 py-1">Bloqueado</span>
                  <div class="text-3xl mt-2">🔒</div>
                </div>
              </div>

              <!-- Info -->
              <h3 class="font-display font-bold text-xl mb-2" :class="achievement.unlocked ? 'text-white' : 'text-gray-400'">
                {{ achievement.name }}
              </h3>
              <p class="text-sm text-gray-500 mb-4">{{ achievement.description }}</p>

              <!-- Points -->
              <div class="flex items-center justify-between pt-4 border-t border-dark-800">
                <span class="text-xs uppercase tracking-wider text-gray-600">{{ getCategoryLabel(achievement.category) }}</span>
                <span class="font-bold text-yellow-400">+{{ achievement.points }} pts</span>
              </div>
            </div>

            <!-- Shine effect on unlock -->
            <div
              v-if="achievement.unlocked"
              class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api/axios'

const loading = ref(true)
const checking = ref(false)
const progress = ref({
  total_achievements: 0,
  unlocked_count: 0,
  total_points: 0,
  achievements: []
})
const newlyUnlocked = ref([])
const selectedCategory = ref('all')

const categories = [
  { value: 'content', label: 'Contenido', icon: '📖' },
  { value: 'engagement', label: 'Participación', icon: '💬' },
  { value: 'social', label: 'Social', icon: '👥' },
  { value: 'time', label: 'Antigüedad', icon: '⏰' },
  { value: 'special', label: 'Especial', icon: '🌟' }
]

const progressPercentage = computed(() => {
  if (progress.value.total_achievements === 0) return 0
  return Math.round((progress.value.unlocked_count / progress.value.total_achievements) * 100)
})

const filteredAchievements = computed(() => {
  if (selectedCategory.value === 'all') {
    return progress.value.achievements
  }
  return progress.value.achievements.filter(a => a.category === selectedCategory.value)
})

const getCategoryLabel = (category) => {
  const cat = categories.find(c => c.value === category)
  return cat ? cat.label : category
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const loadAchievements = async () => {
  loading.value = true
  try {
    const response = await api.get('/auth/users/achievements/')
    progress.value = response.data
  } catch (error) {
    console.error('Error loading achievements:', error)
    alert('Error al cargar los logros')
  } finally {
    loading.value = false
  }
}

const checkAchievements = async () => {
  checking.value = true
  newlyUnlocked.value = []
  
  try {
    const response = await api.post('/auth/users/check_achievements/')
    
    if (response.data.newly_unlocked && response.data.newly_unlocked.length > 0) {
      newlyUnlocked.value = response.data.newly_unlocked
      
      // Recargar logros para actualizar la vista
      await loadAchievements()
      
      // Mostrar mensaje de éxito
      setTimeout(() => {
        newlyUnlocked.value = []
      }, 10000) // Ocultar después de 10 segundos
    } else {
      alert('No hay nuevos logros desbloqueados en este momento. ¡Sigue jugando!')
    }
  } catch (error) {
    console.error('Error checking achievements:', error)
    alert('Error al verificar los logros')
  } finally {
    checking.value = false
  }
}

onMounted(() => {
  loadAchievements()
})
</script>

<style scoped>
@keyframes pulse-slow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
