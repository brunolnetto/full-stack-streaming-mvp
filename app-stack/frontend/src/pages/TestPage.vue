<template>
  <div>
    <h2>Test API</h2>
    <button @click="callTestApi" :disabled="testApiLoading">Call /api/sample</button>
    <div v-if="testApiLoading">Loading...</div>
    <div v-if="testApiError" class="error">{{ testApiError }}</div>
    <div v-if="testApiResponse">Response: {{ testApiResponse }}</div>
    <h3>Aggregated Table</h3>
    <BaseTable :columns="tableColumns" :rows="sortedHits" :pageSize="pageSize" />
  </div>
</template>
<script setup>
import { ref } from 'vue'
import BaseTable from '../components/BaseTable.vue'
const props = defineProps(['backendUrl', 'tableColumns', 'sortedHits', 'pageSize'])
const testApiResponse = ref('')
const testApiLoading = ref(false)
const testApiError = ref('')
function callTestApi() {
  testApiLoading.value = true
  testApiError.value = ''
  fetch(`${props.backendUrl}/api/sample`)
    .then(res => res.json())
    .then(data => { testApiResponse.value = data.message; testApiLoading.value = false })
    .catch(() => { testApiError.value = 'Failed to call API'; testApiLoading.value = false })
}
</script>
<style scoped>
.error { color: #f44336; margin: 1em 0; }
</style> 