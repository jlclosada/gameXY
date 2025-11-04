<template>
  <div class="bg-gradient-to-r from-yellow-600 to-orange-600 rounded-lg p-4 mb-6 shadow-xl">
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <!-- Título GOAT -->
      <div class="flex items-center gap-3">
        <span class="text-3xl">👑</span>
        <div>
          <h3 class="font-bold text-lg">Modo GOAT</h3>
          <p class="text-sm text-white/80">Tienes permisos especiales de edición</p>
        </div>
      </div>
      
      <!-- Acciones -->
      <div class="flex gap-3 flex-wrap">
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
// Componente simple sin lógica
</script>
