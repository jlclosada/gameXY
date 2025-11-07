<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-4xl font-display font-bold mb-3 bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">
        Comunidad GameXY
      </h1>
      <p class="text-dark-400 text-lg">Únete a grupos, participa en foros y conecta con otros gamers</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary-400 mb-2">{{ stats.groups }}</div>
        <div class="text-sm text-dark-400">Grupos Activos</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-accent-400 mb-2">{{ stats.forums }}</div>
        <div class="text-sm text-dark-400">Foros</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-green-400 mb-2">{{ stats.topics }}</div>
        <div class="text-sm text-dark-400">Discusiones</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-purple-400 mb-2">{{ stats.members }}</div>
        <div class="text-sm text-dark-400">Miembros</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="card mb-6">
      <div class="flex border-b border-dark-700 overflow-x-auto">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-6 py-4 font-medium transition-colors whitespace-nowrap"
          :class="activeTab === tab.id 
            ? 'text-primary-400 border-b-2 border-primary-400' 
            : 'text-dark-400 hover:text-dark-200'"
        >
          <span class="mr-2">{{ tab.icon }}</span>
          {{ tab.label }}
        </button>
      </div>

      <div class="p-6">
        <!-- Groups Tab -->
        <div v-if="activeTab === 'groups'" class="space-y-6">
          <div class="mb-6">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-2xl font-display font-bold">Grupos de Gaming</h2>
              <button
                v-if="authStore.user?.can_edit_content"
                @click="showCreateGroupModal = true"
                class="btn btn-primary"
              >
                <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                Crear Grupo
              </button>
              <div v-else-if="authStore.isAuthenticated" class="text-sm text-dark-400">
                Solo usuarios GOAT/Admin pueden crear grupos
              </div>
            </div>
            
            <!-- Search Bar -->
            <div class="relative">
              <input
                v-model="groupSearchQuery"
                type="text"
                placeholder="Buscar grupos..."
                class="input pl-10"
              />
              <svg class="w-5 h-5 text-dark-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
          </div>

          <div v-if="loadingGroups" class="text-center py-12">
            <div class="inline-block w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
          </div>

          <div v-else-if="groups.length === 0" class="text-center py-12">
            <p class="text-dark-400">No hay grupos disponibles. ¡Crea el primero!</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="group in filteredGroups"
              :key="group.id"
              class="card p-6 hover:border-primary-500/50 transition-all cursor-pointer"
              @click="viewGroup(group)"
            >
              <div class="flex items-start gap-4">
                <div v-if="group.icon" class="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0">
                  <img
                    :src="group.icon"
                    :alt="group.name"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div v-else class="w-16 h-16 rounded-lg bg-dark-700 flex items-center justify-center text-2xl flex-shrink-0">
                  👥
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="font-display font-bold text-lg mb-1 truncate">{{ group.name }}</h3>
                  <p class="text-sm text-dark-400 line-clamp-2 mb-3">{{ group.description }}</p>
                  <div class="flex items-center gap-4 text-xs text-dark-500">
                    <span class="flex items-center gap-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                      </svg>
                      {{ group.member_count }} miembros
                    </span>
                    <span v-if="group.game_name" class="truncate">🎮 {{ group.game_name }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Forums Tab -->
        <div v-if="activeTab === 'forums'" class="space-y-4">
          <h2 class="text-2xl font-display font-bold mb-6">Foros de Discusión</h2>

          <div v-if="loadingForums" class="text-center py-12">
            <div class="inline-block w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
          </div>

          <div v-else-if="forums.length === 0" class="text-center py-12">
            <p class="text-dark-400">No hay foros disponibles</p>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="forum in forums"
              :key="forum.id"
              class="card p-6 hover:border-primary-500/50 transition-all cursor-pointer"
              @click="viewForum(forum)"
            >
              <div class="flex items-center gap-4">
                <div class="text-4xl">{{ forum.icon }}</div>
                <div class="flex-1">
                  <h3 class="font-display font-bold text-lg mb-1">{{ forum.name }}</h3>
                  <p class="text-sm text-dark-400 mb-2">{{ forum.description }}</p>
                  <div class="flex items-center gap-4 text-xs text-dark-500">
                    <span>{{ forum.topic_count }} temas</span>
                    <span>{{ forum.post_count }} respuestas</span>
                    <span class="px-2 py-1 bg-dark-700 rounded">{{ getCategoryLabel(forum.category) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Active Members Tab -->
        <div v-if="activeTab === 'members'">
          <h2 class="text-2xl font-display font-bold mb-6">Miembros Más Activos</h2>
          
          <div v-if="loadingActiveMembers" class="text-center py-12">
            <div class="inline-block w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
          </div>
          
          <div v-else-if="activeMembers.length === 0" class="text-center py-12 text-dark-400">
            <svg class="w-16 h-16 mx-auto mb-4 text-dark-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <p>No hay miembros activos aún</p>
          </div>
          
          <div v-else class="space-y-3">
            <div
              v-for="(member, index) in activeMembers"
              :key="member.id"
              class="card p-6 hover:border-primary-500/50 transition-all"
            >
              <div class="flex items-center gap-4">
                <!-- Ranking Badge -->
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 rounded-full flex items-center justify-center text-2xl font-bold"
                    :class="[
                      index === 0 ? 'bg-yellow-500/20 text-yellow-400' :
                      index === 1 ? 'bg-gray-400/20 text-gray-300' :
                      index === 2 ? 'bg-orange-600/20 text-orange-400' :
                      'bg-dark-700 text-dark-400'
                    ]"
                  >
                    {{ index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `#${index + 1}` }}
                  </div>
                </div>
                
                <!-- Avatar -->
                <div class="flex-shrink-0">
                  <div class="w-16 h-16 rounded-full overflow-hidden border-2"
                    :class="[
                      index === 0 ? 'border-yellow-500' :
                      index === 1 ? 'border-gray-400' :
                      index === 2 ? 'border-orange-600' :
                      'border-dark-600'
                    ]"
                  >
                    <img
                      v-if="member.avatar"
                      :src="member.avatar"
                      :alt="member.username"
                      class="w-full h-full object-cover"
                    >
                    <div v-else class="w-full h-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold text-xl">
                      {{ member.username.charAt(0).toUpperCase() }}
                    </div>
                  </div>
                </div>
                
                <!-- Info -->
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1">
                    <h3 class="font-display font-bold text-lg">{{ member.username }}</h3>
                    <span v-if="member.role === 'admin'" class="badge badge-accent">Admin</span>
                    <span v-else-if="member.role === 'goat'" class="badge badge-primary">GOAT</span>
                  </div>
                  
                  <div class="flex items-center gap-4 text-sm text-dark-400">
                    <span>📝 {{ member.contributions.topics }} temas</span>
                    <span>💬 {{ member.contributions.posts }} respuestas</span>
                    <span>📢 {{ member.contributions.group_posts }} publicaciones</span>
                  </div>
                </div>
                
                <!-- Activity Score -->
                <div class="flex-shrink-0 text-right">
                  <div class="text-2xl font-bold text-primary-400">{{ member.activity_score }}</div>
                  <div class="text-xs text-dark-500">puntos</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Group Modal -->
    <CreateGroupModal
      v-if="showCreateGroupModal"
      @close="showCreateGroupModal = false"
      @created="onGroupCreated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import CreateGroupModal from '@/components/community/CreateGroupModal.vue'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('groups')
const tabs = [
  { id: 'groups', label: 'Grupos', icon: '👥' },
  { id: 'forums', label: 'Foros', icon: '💬' },
  { id: 'members', label: 'Miembros Activos', icon: '⭐' },
]

const stats = ref({
  groups: 0,
  forums: 0,
  topics: 0,
  members: 0
})

const groups = ref([])
const forums = ref([])
const activeMembers = ref([])
const loadingGroups = ref(false)
const loadingForums = ref(false)
const loadingActiveMembers = ref(false)
const showCreateGroupModal = ref(false)
const groupSearchQuery = ref('')

const categoryLabels = {
  'general': 'General',
  'games': 'Juegos',
  'news': 'Noticias',
  'guides': 'Guías',
  'support': 'Soporte',
  'off_topic': 'Off Topic'
}

function getCategoryLabel(category) {
  return categoryLabels[category] || category
}

const filteredGroups = computed(() => {
  if (!groupSearchQuery.value.trim()) return groups.value
  
  const query = groupSearchQuery.value.toLowerCase()
  return groups.value.filter(group => 
    group.name.toLowerCase().includes(query) ||
    group.description.toLowerCase().includes(query)
  )
})

async function loadGroups() {
  loadingGroups.value = true
  try {
    console.log('Loading groups...')
    const response = await api.get('/community/groups/')
    console.log('Groups response:', response.data)
    groups.value = response.data.results || response.data
    stats.value.groups = groups.value.length
    console.log('Groups loaded:', groups.value.length)
  } catch (error) {
    console.error('Error loading groups:', error.response?.data || error.message)
  } finally {
    loadingGroups.value = false
  }
}

async function loadForums() {
  loadingForums.value = true
  try {
    console.log('Loading forums...')
    const response = await api.get('/community/forums/')
    console.log('Forums response:', response.data)
    forums.value = response.data.results || response.data
    stats.value.forums = forums.value.length
    console.log('Forums loaded:', forums.value.length)
  } catch (error) {
    console.error('Error loading forums:', error.response?.data || error.message)
  } finally {
    loadingForums.value = false
  }
}

async function loadStats() {
  try {
    const response = await api.get('/community/stats/')
    stats.value.groups = response.data.total_groups
    stats.value.forums = response.data.total_forums
    stats.value.topics = response.data.total_topics
    stats.value.members = response.data.total_members
    
    // Load active members
    activeMembers.value = response.data.active_members
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

function viewGroup(group) {
  router.push(`/community/groups/${group.slug}`)
}

function viewForum(forum) {
  router.push(`/community/forums/${forum.slug}`)
}

function onGroupCreated(newGroup) {
  groups.value.unshift(newGroup)
  stats.value.groups++
  showCreateGroupModal.value = false
}

onMounted(async () => {
  await Promise.all([
    loadGroups(),
    loadForums(),
    loadStats()
  ])
})
</script>
