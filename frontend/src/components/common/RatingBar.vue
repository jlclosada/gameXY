<template>
  <div class="inline-flex items-center gap-0.5" :title="`${value.toFixed(1)}/${max}`">
    <div v-for="i in max" :key="i" class="relative" :style="{ width: size + 'px', height: size + 'px' }">
      <!-- Icono base (gris) -->
      <svg
        class="absolute inset-0"
        :style="{ color: inactiveColor }"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path v-if="icon === 'star'" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
        <path v-else fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
      </svg>
      
      <!-- Icono activo (color) con clip -->
      <div class="absolute inset-0 overflow-hidden" :style="{ width: getIconFill(i) }">
        <svg
          :style="{ color: activeColor, width: size + 'px', height: size + 'px' }"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path v-if="icon === 'star'" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          <path v-else fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: { type: Number, required: true },
  max: { type: Number, default: 5 },
  icon: { type: String, default: 'star' },
  size: { type: Number, default: 14 },
  activeColor: { type: String, default: '#fbbf24' },
  inactiveColor: { type: String, default: '#374151' }
})

const getIconFill = (position) => {
  const filled = props.value - (position - 1)
  if (filled >= 1) return '100%'
  if (filled <= 0) return '0%'
  return `${(filled * 100).toFixed(0)}%`
}
</script>
