<script setup>
import { ref } from 'vue'

const sidebarOpen = ref(false)
</script>

<template>
  <router-view />
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
}
main {
  width: 100%;
}
</style>
