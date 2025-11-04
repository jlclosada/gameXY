<template>
  <footer class="bg-dark-800 border-t border-dark-700 mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 class="text-lg font-display font-bold mb-4">
            <span class="text-white">Game</span><span class="text-primary-400">XY</span>
          </h3>
          <p class="text-dark-400 text-sm">
            Tu comunidad de videojuegos favorita
          </p>
        </div>
        
        <div>
          <h4 class="font-semibold mb-4">Contenido</h4>
          <ul class="space-y-2 text-sm text-dark-400">
            <li><RouterLink to="/games" class="hover:text-white transition">Juegos</RouterLink></li>
            <li><RouterLink to="/news" class="hover:text-white transition">Noticias</RouterLink></li>
            <li><RouterLink to="/guides" class="hover:text-white transition">Guías</RouterLink></li>
            <li><RouterLink to="/posts" class="hover:text-white transition">Posts</RouterLink></li>
          </ul>
        </div>
        
        <div>
          <h4 class="font-semibold mb-4">Comunidad</h4>
          <ul class="space-y-2 text-sm text-dark-400">
            <li><a href="#" class="hover:text-white transition">Foro</a></li>
            <li><a href="#" class="hover:text-white transition">Discord</a></li>
            <li><a href="#" class="hover:text-white transition">Twitter</a></li>
          </ul>
        </div>
        
        <div>
          <h4 class="font-semibold mb-4">Legal</h4>
          <ul class="space-y-2 text-sm text-dark-400">
            <li><a href="#" class="hover:text-white transition">Privacidad</a></li>
            <li><a href="#" class="hover:text-white transition">Términos</a></li>
          </ul>
        </div>
      </div>
      
      <div class="mt-8 pt-8 border-t border-dark-700 text-center text-sm text-dark-400">
        <p>&copy; {{ new Date().getFullYear() }} GameXY. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
