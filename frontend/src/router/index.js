import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/auth/RegisterView.vue'),
    meta: { guest: true }
  },
  {
    path: '/complete-profile',
    name: 'complete-profile',
    component: () => import('@/views/auth/ProfileCompleteView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/games',
    name: 'games',
    component: () => import('@/views/games/GamesView.vue')
  },
  {
    path: '/games/new',
    name: 'game-create',
    component: () => import('@/views/games/GameFormView.vue'),
    meta: { requiresAuth: true, requiresGoat: true }
  },
  {
    path: '/games/:slug/edit',
    name: 'game-edit',
    component: () => import('@/views/games/GameFormView.vue'),
    meta: { requiresAuth: true, requiresGoat: true }
  },
  {
    path: '/games/:slug',
    name: 'game-detail',
    component: () => import('@/views/games/GameDetailView.vue')
  },
  {
    path: '/news',
    name: 'news',
    component: () => import('@/views/content/NewsView.vue')
  },
  {
    path: '/news/:slug',
    name: 'news-detail',
    component: () => import('@/views/content/NewsDetailView.vue')
  },
  {
    path: '/guides',
    name: 'guides',
    component: () => import('@/views/content/GuidesView.vue')
  },
  {
    path: '/guides/new',
    name: 'guide-create',
    component: () => import('@/views/content/GuideFormView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/guides/:slug/edit',
    name: 'guide-edit',
    component: () => import('@/views/content/GuideFormView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/guides/:slug',
    name: 'guide-detail',
    component: () => import('@/views/content/GuideDetailView.vue')
  },
  {
    path: '/posts',
    name: 'posts',
    component: () => import('@/views/content/PostsView.vue')
  },
  {
    path: '/community',
    name: 'community',
    component: () => import('@/views/community/CommunityView.vue')
  },
  {
    path: '/community/groups/:slug',
    name: 'group-detail',
    component: () => import('@/views/community/GroupDetailView.vue')
  },
  {
    path: '/community/forums/:slug',
    name: 'forum-detail',
    component: () => import('@/views/community/ForumDetailView.vue')
  },
  {
    path: '/community/forums/:forumSlug/topics/:topicSlug',
    name: 'topic-detail',
    component: () => import('@/views/community/TopicDetailView.vue')
  },
  {
    path: '/posts/:slug',
    name: 'post-detail',
    component: () => import('@/views/content/PostDetailView.vue')
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: () => import('@/views/NotificationsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/saved-guides',
    name: 'saved-guides',
    component: () => import('@/views/SavedGuidesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/favorite-games',
    name: 'favorite-games',
    component: () => import('@/views/FavoriteGamesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/achievements',
    name: 'achievements',
    component: () => import('@/views/AchievementsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/news/new',
    name: 'news-create',
    component: () => import('@/views/content/NewsFormView.vue'),
    meta: { requiresAuth: true, requiresGoat: true }
  },
  {
    path: '/news/:slug/edit',
    name: 'news-edit',
    component: () => import('@/views/content/NewsFormView.vue'),
    meta: { requiresAuth: true, requiresGoat: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: 'home' })
  } else if (to.meta.requiresGoat && !authStore.user?.can_edit_content) {
    // Redirigir si la ruta requiere permisos de edición (GOAT o Admin) y el usuario no los tiene
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
