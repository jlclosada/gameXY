<template>
  <div class="rich-editor border border-dark-800 rounded-lg overflow-hidden bg-dark-900">
    <div v-if="editor" class="toolbar bg-dark-850 border-b border-dark-800 p-2 flex flex-wrap gap-1">
      <button
        @click="editor.chain().focus().toggleBold().run()"
        :class="{ 'bg-primary-600': editor.isActive('bold') }"
        class="toolbar-btn"
        type="button"
      >
        <strong>B</strong>
      </button>
      <button
        @click="editor.chain().focus().toggleItalic().run()"
        :class="{ 'bg-primary-600': editor.isActive('italic') }"
        class="toolbar-btn"
        type="button"
      >
        <em>I</em>
      </button>
      <button
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
        :class="{ 'bg-primary-600': editor.isActive('heading', { level: 2 }) }"
        class="toolbar-btn"
        type="button"
      >
        H2
      </button>
      <button
        @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
        :class="{ 'bg-primary-600': editor.isActive('heading', { level: 3 }) }"
        class="toolbar-btn"
        type="button"
      >
        H3
      </button>
      <button
        @click="editor.chain().focus().toggleBulletList().run()"
        :class="{ 'bg-primary-600': editor.isActive('bulletList') }"
        class="toolbar-btn"
        type="button"
      >
        • List
      </button>
      <button
        @click="editor.chain().focus().toggleOrderedList().run()"
        :class="{ 'bg-primary-600': editor.isActive('orderedList') }"
        class="toolbar-btn"
        type="button"
      >
        1. List
      </button>
      <button
        @click="addImage"
        class="toolbar-btn"
        type="button"
      >
        🖼️ Imagen
      </button>
      <button
        @click="addYouTubeVideo"
        class="toolbar-btn"
        type="button"
      >
        ▶️ YouTube
      </button>
      <button
        @click="addLink"
        :class="{ 'bg-primary-600': editor.isActive('link') }"
        class="toolbar-btn"
        type="button"
      >
        🔗 Link
      </button>
    </div>
    <EditorContent :editor="editor" class="prose prose-invert max-w-none p-4 min-h-[400px]" />
  </div>
</template>

<script setup>
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Youtube from '@tiptap/extension-youtube'
import Link from '@tiptap/extension-link'
import { watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

// Función para decodificar HTML escapado
const decodeHTML = (html) => {
  const txt = document.createElement('textarea')
  txt.innerHTML = html
  return txt.value
}

const editor = useEditor({
  content: decodeHTML(props.modelValue || ''),
  extensions: [
    StarterKit,
    Image.configure({
      inline: true,
      allowBase64: true,
    }),
    Youtube.configure({
      controls: true,
      nocookie: true,
      width: 640,
      height: 480,
      HTMLAttributes: {
        class: 'youtube-video',
        allow: 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture',
        allowfullscreen: 'allowfullscreen',
        frameborder: '0',
      },
      inline: false,
      modestBranding: true,
      ccLoadPolicy: true,
    }),
    Link.configure({
      openOnClick: false,
    }),
  ],
  onUpdate: ({ editor }) => {
    emit('update:modelValue', editor.getHTML())
  },
})

watch(() => props.modelValue, (value) => {
  if (editor.value && value !== editor.value.getHTML()) {
    editor.value.commands.setContent(decodeHTML(value || ''), false)
  }
})

const addImage = () => {
  const url = prompt('URL de la imagen:')
  if (url) {
    editor.value.chain().focus().setImage({ src: url }).run()
  }
}

const addYouTubeVideo = () => {
  const url = prompt('URL del video de YouTube:')
  if (url) {
    editor.value.chain().focus().setYoutubeVideo({ src: url }).run()
  }
}

const addLink = () => {
  const url = prompt('URL del enlace:')
  if (url) {
    editor.value.chain().focus().setLink({ href: url }).run()
  } else {
    editor.value.chain().focus().unsetLink().run()
  }
}
</script>

<style scoped>
.toolbar-btn {
  @apply px-3 py-1.5 rounded bg-dark-800 hover:bg-dark-700 text-sm text-gray-300 transition-colors;
}

:deep(.ProseMirror) {
  outline: none;
  color: #e5e5e5;
}

:deep(.ProseMirror h2) {
  @apply text-2xl font-display font-bold mt-6 mb-4;
}

:deep(.ProseMirror h3) {
  @apply text-xl font-display font-semibold mt-4 mb-3;
}

:deep(.ProseMirror ul),
:deep(.ProseMirror ol) {
  @apply pl-6 my-4;
}

:deep(.ProseMirror img) {
  @apply max-w-full rounded-lg my-4;
}

:deep(.ProseMirror iframe),
:deep(.ProseMirror .youtube-video) {
  @apply w-full rounded-lg my-4;
  aspect-ratio: 16 / 9;
  max-width: 100%;
  min-height: 400px;
  border: none;
}

:deep(.ProseMirror div[data-youtube-video]) {
  @apply w-full my-4;
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
  height: 0;
  overflow: hidden;
}

:deep(.ProseMirror div[data-youtube-video] iframe) {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

:deep(.ProseMirror a) {
  @apply text-primary-400 hover:text-primary-300 underline;
}

:deep(.ProseMirror p) {
  @apply my-3;
}
</style>
