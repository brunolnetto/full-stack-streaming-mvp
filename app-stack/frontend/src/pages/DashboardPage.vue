<template>
  <div class="flex flex-col items-center justify-center min-h-[60vh] bg-white rounded-lg shadow-md p-10">
    <h1 class="text-4xl font-bold text-blue-700 mb-4">Welcome to Your Dashboard</h1>
    <p class="text-lg text-gray-600 mb-8">This is a modern, styled landing page using Tailwind CSS.<br>All your main features will appear here.</p>
    <div class="flex gap-4">
      <button class="px-6 py-2 bg-blue-600 text-white rounded shadow hover:bg-blue-700 transition">Primary Action</button>
      <button class="px-6 py-2 bg-gray-200 text-gray-700 rounded shadow hover:bg-gray-300 transition">Secondary Action</button>
    </div>
    <div class="mt-10 w-full max-w-xl">
      <div class="bg-blue-50 border-l-4 border-blue-400 p-4 text-blue-800 rounded">
        <p class="font-medium">Tip:</p>
        <p>Use the sidebar to navigate between pages. This dashboard is styled with Tailwind and ready for your content!</p>
      </div>
    </div>
  </div>
</template>
<script setup>
import BaseTable from '../components/BaseTable.vue'
const props = defineProps([
  'hits', 'connected', 'loading', 'error', 'search', 'minCount', 'maxCount', 'sortKey', 'sortDir', 'timeRange', 'manualRefresh', 'tableColumns', 'sortedHits', 'pageSize'
])
const emit = defineEmits(['update:search', 'update:minCount', 'update:maxCount', 'update:sortKey', 'update:sortDir', 'update:timeRange'])
</script>
<style scoped>
.status-dot { /* ... */ }
.live { /* ... */ }
.disconnected { /* ... */ }
.loader { /* ... */ }
.error { /* ... */ }
.controls { /* ... */ }
</style> 