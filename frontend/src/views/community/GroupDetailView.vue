<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <div v-else-if="group" class="space-y-6">
      <!-- Group Header -->
      <div class="card overflow-hidden">
        <!-- Banner -->
        <div v-if="group.banner" class="h-48 bg-gradient-to-r from-primary-600 to-accent-600">
          <img :src="group.banner" alt="Banner" class="w-full h-full object-cover" />
        </div>
        <div v-else class="h-48 bg-gradient-to-r from-primary-600 to-accent-600"></div>

        <div class="p-6">
          <div class="flex items-start gap-6">
            <!-- Group Icon -->
            <div class="w-24 h-24 -mt-16 rounded-xl overflow-hidden border-4 border-dark-900 bg-dark-800 flex items-center justify-center text-4xl flex-shrink-0">
              <img v-if="group.icon" :src="group.icon" alt="Icon" class="w-full h-full object-cover" />
              <span v-else>👥</span>
            </div>

            <div class="flex-1">
              <div class="flex items-start justify-between">
                <div>
                  <h1 class="text-3xl font-display font-bold mb-2">{{ group.name }}</h1>
                  <p class="text-dark-400 mb-4">{{ group.description }}</p>
                  <div class="flex items-center gap-6 text-sm text-dark-500">
                    <span class="flex items-center gap-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                      </svg>
                      {{ group.member_count }} miembros
                    </span>
                    <span v-if="group.game_name">🎮 {{ group.game_name }}</span>
                    <span class="px-2 py-1 bg-dark-700 rounded">
                      {{ group.is_public ? '🌐 Público' : '🔒 Privado' }}
                    </span>
                  </div>
                </div>

                <!-- Join/Leave/Edit Buttons -->
                <div v-if="authStore.isAuthenticated" class="flex items-center gap-3">
                  <!-- Invite button for creator -->
                  <button
                    v-if="group.creator.id === authStore.user?.id"
                    @click="showInviteModal = true"
                    class="btn btn-primary"
                  >
                    <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
                    </svg>
                    Invitar Usuario
                  </button>

                  <!-- Edit button for creator -->
                  <button
                    v-if="group.creator.id === authStore.user?.id"
                    @click="showEditModal = true"
                    class="btn btn-secondary"
                  >
                    <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    Editar Grupo
                  </button>

                  <!-- Pending join request -->
                  <button
                    v-if="!group.is_member && group.has_pending_request"
                    disabled
                    class="btn btn-secondary opacity-75 cursor-not-allowed"
                  >
                    <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    Solicitud Pendiente
                  </button>
                  <!-- Not a member -->
                  <button
                    v-else-if="!group.is_member"
                    @click="joinGroup"
                    :disabled="joiningGroup"
                    class="btn btn-primary"
                  >
                    {{ joiningGroup ? 'Uniéndose...' : 'Unirse al Grupo' }}
                  </button>
                  <!-- Member but not creator -->
                  <button
                    v-else-if="group.creator.id !== authStore.user?.id"
                    @click="leaveGroup"
                    :disabled="leavingGroup"
                    class="btn btn-secondary"
                  >
                    {{ leavingGroup ? 'Saliendo...' : 'Abandonar Grupo' }}
                  </button>
                  <!-- Creator badge -->
                  <div v-else class="badge badge-primary">Creador</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Locked for Non-Members -->
      <div v-if="!group.is_member && !isContentVisible" class="card p-12 text-center">
        <div class="inline-block p-6 bg-dark-800 rounded-full mb-6">
          <svg class="w-16 h-16 text-dark-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
        </div>
        <h2 class="text-2xl font-display font-bold mb-3">Contenido Bloqueado</h2>
        <p class="text-dark-400 mb-6">Únete al grupo para ver las publicaciones y participar en las conversaciones</p>
        <button @click="joinGroup" class="btn btn-primary">
          <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
          Unirse Ahora
        </button>
      </div>

      <!-- Join Requests (for admins/moderators/creator) -->
      <div v-if="canManageRequests && pendingRequests.length > 0" class="card p-6">
        <h3 class="text-xl font-display font-bold mb-4">
          <svg class="w-6 h-6 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          Solicitudes Pendientes ({{ pendingRequests.length }})
        </h3>
        <div class="space-y-3">
          <div
            v-for="request in pendingRequests"
            :key="request.id"
            class="flex items-center justify-between p-4 bg-dark-800 rounded-lg"
          >
            <div class="flex items-center gap-3">
              <UserAvatar :user="request.user" size="md" />
              <div>
                <div class="font-medium">{{ request.user.username }}</div>
                <div v-if="request.message" class="text-sm text-dark-400 mt-1">{{ request.message }}</div>
                <div class="text-xs text-dark-500 mt-1">{{ formatDate(request.created_at) }}</div>
              </div>
            </div>
            <div class="flex gap-2">
              <button
                @click="approveRequest(request.id)"
                class="btn btn-primary btn-sm"
              >
                <svg class="w-4 h-4 inline-block mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Aprobar
              </button>
              <button
                @click="rejectRequest(request.id)"
                class="btn btn-secondary btn-sm"
              >
                <svg class="w-4 h-4 inline-block mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
                Rechazar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs for Members -->
      <div v-else class="space-y-6">
        <!-- Tabs -->
        <div class="card">
          <div class="flex border-b border-dark-700">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              class="px-6 py-4 font-medium transition-colors"
              :class="activeTab === tab.id
                ? 'text-primary-400 border-b-2 border-primary-400'
                : 'text-dark-400 hover:text-dark-200'"
            >
              <span class="mr-2">{{ tab.icon }}</span>
              {{ tab.label }}
            </button>
          </div>

          <div class="p-6">
            <!-- Posts Tab -->
            <div v-if="activeTab === 'posts'" class="space-y-6">
              <!-- Create Post -->
              <div class="card p-6 bg-dark-800">
                <div class="flex items-start gap-4">
                  <div class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold flex-shrink-0">
                    {{ authStore.user?.username?.[0]?.toUpperCase() }}
                  </div>
                  <div class="flex-1">
                    <textarea
                      v-model="newPost.content"
                      placeholder="Comparte algo con el grupo..."
                      class="input mb-3 min-h-[100px]"
                    ></textarea>

                    <!-- Post Type Selector -->
                    <div class="flex items-center gap-2 mb-3">
                      <button
                        v-for="type in postTypes"
                        :key="type.value"
                        @click="newPost.post_type = type.value"
                        class="px-3 py-2 rounded-lg text-sm transition"
                        :class="newPost.post_type === type.value
                          ? 'bg-primary-600 text-white'
                          : 'bg-dark-700 text-dark-300 hover:bg-dark-600'"
                      >
                        {{ type.icon }} {{ type.label }}
                      </button>
                    </div>

                    <!-- Image Upload -->
                    <div v-if="newPost.post_type === 'image'" class="mb-3">
                      <input
                        type="file"
                        @change="handleImageChange"
                        accept="image/*"
                        class="input"
                      />
                      <img v-if="imagePreview" :src="imagePreview" alt="Preview" class="mt-2 max-h-48 rounded-lg" />
                    </div>

                    <!-- Video URL -->
                    <div v-if="newPost.post_type === 'video'" class="mb-3">
                      <input
                        v-model="newPost.video_url"
                        type="url"
                        placeholder="URL del video (YouTube, Twitch, etc.)"
                        class="input"
                      />
                    </div>

                    <!-- Link -->
                    <div v-if="newPost.post_type === 'link'" class="space-y-2 mb-3">
                      <input
                        v-model="newPost.link_url"
                        type="url"
                        placeholder="URL del enlace"
                        class="input"
                      />
                      <input
                        v-model="newPost.link_title"
                        type="text"
                        placeholder="Título del enlace (opcional)"
                        class="input"
                      />
                    </div>

                    <button
                      @click="createPost"
                      :disabled="!newPost.content.trim() || creatingPost"
                      class="btn btn-primary"
                    >
                      {{ creatingPost ? 'Publicando...' : 'Publicar' }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Posts List -->
              <div v-if="loadingPosts" class="text-center py-8">
                <div class="inline-block w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
              </div>

              <div v-else-if="posts.length === 0" class="text-center py-12 text-dark-400">
                No hay publicaciones aún. ¡Sé el primero en compartir algo!
              </div>

              <div v-else class="space-y-4">
                <div
                  v-for="post in posts"
                  :key="post.id"
                  class="card p-6"
                  :class="post.is_pinned && 'border-l-4 border-primary-500'"
                >
                  <div class="flex items-start gap-4">
                    <div class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold flex-shrink-0">
                      {{ post.author.username[0].toUpperCase() }}
                    </div>
                    <div class="flex-1">
                      <div class="flex items-center justify-between mb-2">
                        <div>
                          <span class="font-semibold">{{ post.author.username }}</span>
                          <span v-if="post.is_pinned" class="ml-2 text-xs bg-primary-600 text-white px-2 py-1 rounded">📌 Fijado</span>
                          <p class="text-xs text-dark-500">{{ formatDate(post.created_at) }}</p>
                        </div>
                      </div>

                      <p class="text-dark-200 mb-3 whitespace-pre-wrap">{{ post.content }}</p>

                      <!-- Media -->
                      <div v-if="post.image" class="mb-3">
                        <img :src="post.image" alt="Post image" class="rounded-lg max-h-96 w-auto" />
                      </div>

                      <div v-if="post.video_url" class="mb-3">
                        <a :href="post.video_url" target="_blank" class="text-primary-400 hover:underline">
                          🎥 Ver video
                        </a>
                      </div>

                      <div v-if="post.link_url" class="mb-3 p-4 bg-dark-800 rounded-lg">
                        <a :href="post.link_url" target="_blank" class="text-primary-400 hover:underline">
                          🔗 {{ post.link_title || post.link_url }}
                        </a>
                      </div>

                      <!-- Comments Section -->
                      <div class="mt-4 pt-4 border-t border-dark-700">
                        <button
                          @click="toggleComments(post.id)"
                          class="text-sm text-dark-400 hover:text-white transition"
                        >
                          💬 {{ post.comment_count }} comentarios
                        </button>

                        <div v-if="showComments[post.id]" class="mt-4 space-y-3">
                          <!-- Comment Form -->
                          <div class="flex gap-2">
                            <input
                              v-model="commentTexts[post.id]"
                              type="text"
                              placeholder="Escribe un comentario..."
                              class="input flex-1"
                              @keyup.enter="addComment(post.id)"
                            />
                            <button
                              @click="addComment(post.id)"
                              :disabled="!commentTexts[post.id]?.trim()"
                              class="btn btn-primary"
                            >
                              Enviar
                            </button>
                          </div>

                          <!-- Comments List -->
                          <div v-for="comment in post.comments" :key="comment.id" class="flex gap-3 pl-4">
                            <div class="w-8 h-8 rounded-full bg-accent-600 flex items-center justify-center text-white text-sm font-semibold flex-shrink-0">
                              {{ comment.author.username[0].toUpperCase() }}
                            </div>
                            <div class="flex-1 bg-dark-800 p-3 rounded-lg">
                              <p class="text-sm font-semibold mb-1">{{ comment.author.username }}</p>
                              <p class="text-sm text-dark-200">{{ comment.content }}</p>
                              <p class="text-xs text-dark-500 mt-1">{{ formatDate(comment.created_at) }}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Members Tab -->
            <div v-if="activeTab === 'members'">
              <h3 class="text-xl font-display font-bold mb-4">Miembros ({{ members.length }})</h3>

              <div v-if="loadingMembers" class="text-center py-8">
                <div class="inline-block w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
              </div>

              <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div
                  v-for="member in members"
                  :key="member.id"
                  class="flex items-center gap-4 p-4 bg-dark-800 rounded-lg"
                >
                  <div class="w-12 h-12 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold">
                    {{ member.user.username[0].toUpperCase() }}
                  </div>
                  <div class="flex-1">
                    <p class="font-semibold">{{ member.user.username }}</p>
                    <p class="text-xs text-dark-400">
                      {{ getRoleLabel(member.role) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 text-dark-400">
      Grupo no encontrado
    </div>

    <!-- Edit Group Modal -->
    <EditGroupModal
      v-if="showEditModal && group"
      :group="group"
      @close="showEditModal = false"
      @updated="onGroupUpdated"
    />

    <!-- Invite User Modal -->
    <InviteUserModal
      v-if="showInviteModal && group"
      :group="group"
      @close="showInviteModal = false"
      @invited="onUserInvited"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import UserAvatar from '@/components/common/UserAvatar.vue'
import EditGroupModal from '@/components/community/EditGroupModal.vue'
import InviteUserModal from '@/components/community/InviteUserModal.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const group = ref(null)
const posts = ref([])
const members = ref([])
const loading = ref(true)
const loadingPosts = ref(false)
const loadingMembers = ref(false)
const joiningGroup = ref(false)
const leavingGroup = ref(false)
const creatingPost = ref(false)
const pendingRequests = ref([])
const activeTab = ref('posts')
const showEditModal = ref(false)
const showInviteModal = ref(false)
const tabs = [
  { id: 'posts', label: 'Publicaciones', icon: '📝' },
  { id: 'members', label: 'Miembros', icon: '👥' },
]

const newPost = ref({
  content: '',
  post_type: 'text',
  image: null,
  video_url: '',
  link_url: '',
  link_title: ''
})

const postTypes = [
  { value: 'text', label: 'Texto', icon: '' },
  { value: 'image', label: 'Imagen', icon: '' },
  { value: 'video', label: 'Video', icon: '' },
  { value: 'link', label: 'Enlace', icon: '' },
]

const imagePreview = ref(null)
const showComments = ref({})
const commentTexts = ref({})

const isContentVisible = computed(() => {
  return group.value?.is_member || group.value?.is_public
})

const canManageRequests = computed(() => {
  if (!group.value || !authStore.user) return false
  if (group.value.creator.id === authStore.user.id) return true

  const userMembership = members.value.find(m => m.user.id === authStore.user.id)
  return userMembership && (userMembership.role === 'admin' || userMembership.role === 'moderator')
})

function handleImageChange(event) {
  const file = event.target.files[0]
  if (file) {
    newPost.value.image = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

async function loadGroup() {
  try {
    const response = await api.get(`/community/groups/${route.params.slug}/`)
    group.value = response.data
  } catch (error) {
    console.error('Error loading group:', error)
  } finally {
    loading.value = false
  }
}

async function loadPosts() {
  if (!isContentVisible.value) return

  loadingPosts.value = true
  try {
    const response = await api.get('/community/group-posts/', {
      params: { group: route.params.slug }
    })
    posts.value = response.data.results || response.data
  } catch (error) {
    console.error('Error loading posts:', error)
  } finally {
    loadingPosts.value = false
  }
}

async function loadMembers() {
  loadingMembers.value = true
  try {
    const response = await api.get(`/community/groups/${route.params.slug}/members/`)
    members.value = response.data
  } catch (error) {
    console.error('Error loading members:', error)
  } finally {
    loadingMembers.value = false
  }
}

async function loadJoinRequests() {
  try {
    const response = await api.get(`/community/groups/${route.params.slug}/join_requests/`)
    pendingRequests.value = response.data
  } catch (error) {
    console.error('Error loading join requests:', error)
  }
}

async function joinGroup() {
  joiningGroup.value = true
  try {
    const response = await api.post(`/community/groups/${route.params.slug}/join/`)
    const message = response.data?.message || 'Te has unido al grupo'

    // Show different message for private groups
    if (message.includes('Solicitud')) {
      alert('Solicitud enviada. El creador del grupo la revisar\u00e1 pronto.')
    }

    await loadGroup()
    if (group.value.is_member) {
      await loadPosts()
    }
  } catch (error) {
    console.error('Error joining group:', error)
    alert(error.response?.data?.detail || 'Error al unirse al grupo')
  } finally {
    joiningGroup.value = false
  }
}

async function approveRequest(requestId) {
  try {
    await api.post(`/community/groups/${route.params.slug}/approve_request/`, {
      request_id: requestId
    })
    await loadJoinRequests()
    await loadMembers()
    alert('Solicitud aprobada')
  } catch (error) {
    console.error('Error approving request:', error)
    alert(error.response?.data?.detail || 'Error al aprobar solicitud')
  }
}

async function rejectRequest(requestId) {
  try {
    await api.post(`/community/groups/${route.params.slug}/reject_request/`, {
      request_id: requestId
    })
    await loadJoinRequests()
    alert('Solicitud rechazada')
  } catch (error) {
    console.error('Error rejecting request:', error)
    alert(error.response?.data?.detail || 'Error al rechazar solicitud')
  }
}

async function leaveGroup() {
  if (!confirm('¿Estás seguro de que quieres abandonar el grupo?')) return

  leavingGroup.value = true
  try {
    await api.post(`/community/groups/${route.params.slug}/leave/`)
    router.push('/community')
  } catch (error) {
    console.error('Error leaving group:', error)
    alert(error.response?.data?.detail || 'Error al abandonar el grupo')
  } finally {
    leavingGroup.value = false
  }
}

async function createPost() {
  creatingPost.value = true
  try {
    const formData = new FormData()
    formData.append('group', group.value.id)
    formData.append('content', newPost.value.content)
    formData.append('post_type', newPost.value.post_type)

    if (newPost.value.post_type === 'image' && newPost.value.image) {
      formData.append('image', newPost.value.image)
    } else if (newPost.value.post_type === 'video' && newPost.value.video_url) {
      formData.append('video_url', newPost.value.video_url)
    } else if (newPost.value.post_type === 'link') {
      formData.append('link_url', newPost.value.link_url)
      if (newPost.value.link_title) {
        formData.append('link_title', newPost.value.link_title)
      }
    }

    const response = await api.post('/community/group-posts/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    posts.value.unshift(response.data)

    // Reset form
    newPost.value = {
      content: '',
      post_type: 'text',
      image: null,
      video_url: '',
      link_url: '',
      link_title: ''
    }
    imagePreview.value = null
  } catch (error) {
    console.error('Error creating post:', error)
    alert(error.response?.data?.detail || 'Error al crear la publicación')
  } finally {
    creatingPost.value = false
  }
}

function toggleComments(postId) {
  showComments.value[postId] = !showComments.value[postId]
}

async function addComment(postId) {
  const content = commentTexts.value[postId]
  if (!content?.trim()) return

  try {
    const response = await api.post('/community/group-post-comments/', {
      post: postId,
      content: content
    })

    const post = posts.value.find(p => p.id === postId)
    if (post) {
      if (!post.comments) post.comments = []
      post.comments.push(response.data)
      post.comment_count = post.comments.length
    }

    commentTexts.value[postId] = ''
  } catch (error) {
    console.error('Error adding comment:', error)
    alert('Error al añadir comentario')
  }
}

function getRoleLabel(role) {
  const labels = {
    'admin': '👑 Administrador',
    'moderator': '🛡️ Moderador',
    'member': '👤 Miembro'
  }
  return labels[role] || role
}

function formatDate(date) {
  const d = new Date(date)
  const now = new Date()
  const diff = now - d
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return 'Ahora mismo'
  if (minutes < 60) return `Hace ${minutes}m`
  if (hours < 24) return `Hace ${hours}h`
  if (days < 7) return `Hace ${days}d`

  return d.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
}

function onGroupUpdated(updatedGroup) {
  group.value = updatedGroup
  showEditModal.value = false
}

function onUserInvited() {
  showInviteModal.value = false
}

onMounted(async () => {
  await loadGroup()
  if (isContentVisible.value) {
    await Promise.all([loadPosts(), loadMembers()])
  }

  // Load join requests if user can manage them
  if (group.value && authStore.isAuthenticated) {
    await loadJoinRequests()
  }
})
</script>
