<script setup>
import { useRouter } from 'vue-router'
import { useUser } from '../stores/user'
import Avatar from './Avatar.vue'

const { currentUser, logout } = useUser()
const router = useRouter()

function onLogout() {
  logout()
  router.push('/home')
}
</script>

<template>
  <header class="header">
    <div class="container between">
      <router-link to="/home" class="brand">
        <span class="brand-mark">CS</span>
        <span>为啥选</span>
      </router-link>

      <nav class="row gap-3">
        <router-link to="/create" class="btn btn--primary btn--sm">＋ 发布</router-link>
        <template v-if="currentUser">
          <router-link to="/profile" class="row gap-2 user-chip">
            <Avatar :src="currentUser.avatar" :name="currentUser.username" :size="28" />
            <span class="user-name">{{ currentUser.username }}</span>
          </router-link>
          <button class="btn btn--ghost btn--sm" @click="onLogout">退出</button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn btn--ghost btn--sm">登录</router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  border-bottom: 1px solid var(--line);
  background: var(--bg);
  position: sticky;
  top: 0;
  z-index: 20;
}
.header .container {
  height: 64px;
}
.brand {
  display: inline-flex;
  align-items: baseline;
  gap: 6px;
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: 0.01em;
}
.brand-mark {
  font-family: var(--mono);
  font-size: 0.8rem;
  background: var(--ink);
  color: var(--bg);
  padding: 2px 6px;
  border-radius: 2px;
}
.user-chip {
  font-size: 0.9rem;
}
.user-name {
  font-weight: 700;
}
</style>
