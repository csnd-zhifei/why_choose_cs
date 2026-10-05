<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/AppHeader.vue'

const route = useRoute()
// 欢迎页与快问快答是全屏沉浸页，不显示顶部导航
const bare = computed(() => ['welcome', 'quiz'].includes(route.name))
</script>

<template>
  <div class="app">
    <AppHeader v-if="!bare" />
    <router-view />
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
}
</style>
