<template>
  <li>
    <button
      class="w-full flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-colors duration-100 focus:outline-none focus:ring-2 focus:ring-blue-500 group text-gray-700 dark:text-gray-200"
      :class="[
        active ? 'bg-blue-50 dark:bg-blue-900 text-blue-700 dark:text-blue-200 border-l-4 border-blue-500' : 'hover:bg-gray-100 dark:hover:bg-gray-800',
        'justify-start'
      ]"
      :tabindex="tabindex"
      @click="$emit('activate', item.id)"
      @keydown.enter.prevent="$emit('activate', item.id)"
      :aria-current="active ? 'page' : undefined"
      :aria-label="item.label"
    >
      <span v-if="item.icon" class="w-5 h-5 flex-shrink-0">
        <component :is="item.icon" />
      </span>
      <span class="truncate">{{ item.label }}</span>
    </button>
  </li>
</template>
<script setup>
const props = defineProps({
  item: Object,
  active: Boolean,
  tabindex: { type: Number, default: 0 }
})
</script> 