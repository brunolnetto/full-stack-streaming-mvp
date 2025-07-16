<template>
  <div>
    <h2>Settings</h2>
    <div class="settings-group">
      <label>Backend URL:
        <input v-model="backendUrlProxy" placeholder="http://backend:8000" />
      </label>
    </div>
    <div class="settings-group">
      <label>Theme:
        <select v-model="themeProxy">
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </select>
      </label>
    </div>
    <div class="settings-group">
      <label>Page Size:
        <input v-model.number="pageSizeProxy" type="number" min="1" max="100" />
      </label>
    </div>
  </div>
</template>
<script setup>
const props = defineProps(['backendUrl', 'theme', 'pageSize'])
const emit = defineEmits(['update:backendUrl', 'update:theme', 'update:pageSize'])
const backendUrlProxy = computed({
  get: () => props.backendUrl,
  set: v => emit('update:backendUrl', v)
})
const themeProxy = computed({
  get: () => props.theme,
  set: v => emit('update:theme', v)
})
const pageSizeProxy = computed({
  get: () => props.pageSize,
  set: v => emit('update:pageSize', v)
})
</script>
<style scoped>
.settings-group { margin-bottom: 1em; }
</style> 