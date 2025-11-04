<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-4xl font-display font-bold mb-8">Noticias</h1>
    
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="card h-80 animate-pulse bg-dark-700"></div>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <NewsCard v-for="news in newsList" :key="news.id" :news="news" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import NewsCard from '@/components/cards/NewsCard.vue'
const newsList = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await api.get('/content/news/')
    console.log('News response:', response.data)
    console.log('Is array?', Array.isArray(response.data))
    
    // Manejar tanto respuestas paginadas como arrays directos
    if (Array.isArray(response.data)) {
      newsList.value = response.data
    } else if (response.data && response.data.results) {
      newsList.value = response.data.results
    } else {
      newsList.value = []
    }
    
    console.log('Loaded news:', newsList.value)
    console.log('News count:', newsList.value.length)
  } catch (error) {
    console.error('Error loading news:', error)
  } finally {
    loading.value = false
  }
})
</script>
