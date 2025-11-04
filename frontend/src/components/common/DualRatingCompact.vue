<template>
  <div class="flex flex-col gap-1">
    <!-- GOAT Rating Badge -->
    <div 
      v-if="professionalRating && Number(professionalRating) > 0" 
      class="flex items-center gap-1.5 bg-gradient-to-br from-amber-500/20 to-orange-500/20 backdrop-blur-sm border border-amber-500/40 px-2 py-1 rounded-lg"
      :title="`Valoración GOAT: ${professionalRating}/10`"
    >
      <svg class="w-3 h-3 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
      </svg>
      <span class="text-xs font-bold text-amber-400">{{ formatRating(professionalRating) }}</span>
    </div>
    
    <!-- Community Rating Badge -->
    <div 
      v-if="communityRating && Number(communityRating) > 0" 
      class="flex items-center gap-1.5 bg-dark-900/90 backdrop-blur-sm border border-dark-700 px-2 py-1 rounded-lg"
      :title="`Valoración comunidad: ${communityRating}/5`"
    >
      <svg class="w-3 h-3 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
        <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"/>
      </svg>
      <span class="text-xs font-bold text-blue-400">{{ formatRating(communityRating) }}</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  professionalRating: {
    type: [Number, String],
    default: null
  },
  communityRating: {
    type: [Number, String],
    default: 0
  }
})

const formatRating = (rating) => {
  if (!rating || rating === 0) return '0.0'
  return Number(rating).toFixed(1)
}
</script>
