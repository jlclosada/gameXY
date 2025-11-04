<template>
  <div class="star-rating">
    <div v-if="readonly" class="flex items-center gap-2">
      <div class="flex gap-0.5">
        <svg
          v-for="n in 5"
          :key="n"
          class="w-5 h-5"
          :class="n <= Math.round(value) ? 'text-yellow-400' : 'text-gray-600'"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
        </svg>
      </div>
      <span class="text-sm text-gray-400">({{ Number(value).toFixed(1) }})</span>
      <span v-if="count" class="text-xs text-gray-500">{{ count }} valoraciones</span>
    </div>

    <div v-else class="flex flex-col items-center">
      <div class="flex gap-2 mb-3">
        <button
          v-for="n in 5"
          :key="n"
          @click="rate(n)"
          @mouseenter="hoverRating = n"
          @mouseleave="hoverRating = 0"
          type="button"
          class="star-button"
          :class="{ 'star-filled': n <= (hoverRating || userRating) }"
        >
          <svg
            class="w-12 h-12 transition-all duration-200"
            :class="[
              n <= (hoverRating || userRating) ? 'text-yellow-400 drop-shadow-glow' : 'text-gray-700',
              { 'animate-bounce-subtle': justRated && n <= userRating }
            ]"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          </svg>
        </button>
      </div>
      <div class="text-center">
        <p v-if="userRating" class="text-sm text-gray-300 font-medium mb-1">
          Tu valoración: <span class="text-yellow-400">{{ userRating }}</span>/5
        </p>
        <p class="text-xs text-gray-500">
          {{ hoverRating ? `Valorar con ${hoverRating} ${hoverRating === 1 ? 'estrella' : 'estrellas'}` : 'Haz clic en una estrella para valorar' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    default: 0
  },
  count: {
    type: Number,
    default: 0
  },
  userRating: {
    type: Number,
    default: 0
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['rate'])

const hoverRating = ref(0)
const justRated = ref(false)

const rate = (rating) => {
  emit('rate', rating)
  justRated.value = true
  setTimeout(() => {
    justRated.value = false
  }, 600)
}
</script>

<style scoped>
.star-button {
  @apply transition-all duration-200 ease-out;
  cursor: pointer;
  position: relative;
}

.star-button:hover {
  transform: scale(1.15) rotate(-5deg);
}

.star-button:active {
  transform: scale(0.95);
}

.star-filled {
  animation: star-pulse 0.3s ease-out;
}

@keyframes star-pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.drop-shadow-glow {
  filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.6));
}

.animate-bounce-subtle {
  animation: bounce-subtle 0.6s ease-in-out;
}

@keyframes bounce-subtle {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  25% {
    transform: translateY(-8px) scale(1.1);
  }
  50% {
    transform: translateY(-4px) scale(1.05);
  }
  75% {
    transform: translateY(-2px) scale(1.02);
  }
}
</style>
