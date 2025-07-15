<script setup>
import HitTable from './components/HitTable.vue'
import SampleBackendCall from './components/SampleBackendCall.vue'
</script>

<template>
  <nav style="margin-bottom: 1em;">
    <router-link to="/">Dashboard</router-link> |
    <router-link to="/sample">Sample API</router-link>
  </nav>
  <router-view />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
