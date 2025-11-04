<template>
  <div id="app" class="min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-1">
      <RouterView />
    </main>
    <Footer />
    
    <!-- Menú de opciones para usuarios autenticados -->
    <OptionsMenu v-if="authStore.isAuthenticated" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Navbar from '@/components/layout/Navbar.vue'
import Footer from '@/components/layout/Footer.vue'
import OptionsMenu from '@/components/common/OptionsMenu.vue'

const authStore = useAuthStore()

onMounted(() => {
  authStore.fetchUser()
})
</script>
