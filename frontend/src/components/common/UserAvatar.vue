<template>
  <div
    :class="[
      'rounded-full flex items-center justify-center font-semibold flex-shrink-0 overflow-hidden',
      sizeClasses,
      user?.avatar ? 'bg-dark-700' : 'bg-gradient-to-br from-primary-500 to-accent-500'
    ]"
  >
    <img
      v-if="user?.avatar"
      :src="user.avatar"
      :alt="user.username"
      class="w-full h-full object-cover"
    />
    <span v-else :class="textSizeClasses" class="text-white">
      {{ initials }}
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  size: {
    type: String,
    default: 'md', // xs, sm, md, lg, xl, 2xl
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl', '2xl'].includes(value)
  }
})

const sizeClasses = computed(() => {
  const sizes = {
    'xs': 'w-6 h-6',
    'sm': 'w-8 h-8',
    'md': 'w-10 h-10',
    'lg': 'w-12 h-12',
    'xl': 'w-16 h-16',
    '2xl': 'w-24 h-24'
  }
  return sizes[props.size]
})

const textSizeClasses = computed(() => {
  const sizes = {
    'xs': 'text-xs',
    'sm': 'text-sm',
    'md': 'text-base',
    'lg': 'text-lg',
    'xl': 'text-2xl',
    '2xl': 'text-4xl'
  }
  return sizes[props.size]
})

const initials = computed(() => {
  if (!props.user?.username) return '?'
  return props.user.username.slice(0, 2).toUpperCase()
})
</script>
