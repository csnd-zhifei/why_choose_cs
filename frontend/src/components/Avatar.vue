<script setup>
import { computed } from 'vue'

const props = defineProps({
  src: { type: String, default: '' },
  name: { type: String, default: '' },
  size: { type: Number, default: 40 },
})

const initial = computed(() => (props.name || '?').trim().charAt(0).toUpperCase())
</script>

<template>
  <div
    class="avatar"
    :style="{ width: size + 'px', height: size + 'px', fontSize: size * 0.4 + 'px' }"
  >
    <img v-if="src" :src="src" :alt="name" />
    <span v-else>{{ initial }}</span>
  </div>
</template>

<style scoped>
.avatar {
  flex: none;
  border-radius: 2px;
  overflow: hidden;
  background: var(--accent-soft);
  color: var(--accent-deep);
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--line);
}
.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
