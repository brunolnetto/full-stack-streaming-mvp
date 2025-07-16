<template>
  <nav class="h-screen w-56 bg-white border-r border-gray-200 flex flex-col">
    <div class="px-6 py-4 font-bold text-xl border-b border-gray-100">App</div>
    <ul class="flex-1 py-4">
      <li v-for="item in items" :key="item.id">
        <button
          class="w-full flex items-center gap-3 px-4 py-2 rounded font-medium text-gray-700"
          :class="activeId === item.id ? 'bg-blue-100 text-blue-700' : 'hover:bg-gray-100'"
          @click="$emit('activate', item.id)"
        >
          <span v-if="item.icon" class="w-5 h-5"><component :is="item.icon" /></span>
          <span>{{ item.label }}</span>
        </button>
      </li>
    </ul>
  </nav>
</template>
<script setup>
const props = defineProps({ items: Array, activeId: String })
const emit = defineEmits(['activate'])
</script> 