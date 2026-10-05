<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import { useUser } from '../stores/user'

const router = useRouter()
const { setUser } = useUser()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  if (!username.value || !password.value) return
  loading.value = true
  error.value = ''
  try {
    const u = await api.login({ username: username.value, password: password.value })
    setUser({ userid: u.userid, username: u.username, avatar: u.avatar })
    router.push('/home')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container auth">
    <div class="auth-box">
      <p class="eyebrow">Sign in</p>
      <h1 class="title">登录</h1>

      <form @submit.prevent="submit">
        <label class="lbl">用户名</label>
        <input v-model="username" class="field" type="text" autocomplete="username" />
        <label class="lbl" style="margin-top: 16px">密码</label>
        <input v-model="password" class="field" type="password" autocomplete="current-password" />

        <p v-if="error" class="error-tip">{{ error }}</p>

        <button class="btn btn--primary" style="margin-top: 24px; width: 100%" :disabled="loading">
          {{ loading ? '登录中…' : '登录' }}
        </button>
      </form>

      <p class="small" style="margin-top: 20px">
        还没有账号？
        <router-link to="/register" class="link">注册 →</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.auth {
  display: flex;
  justify-content: center;
  padding: 80px 24px;
}
.auth-box {
  width: 100%;
  max-width: 400px;
}
.auth-box .title {
  margin: 8px 0 32px;
}
.link {
  color: var(--accent);
  font-weight: 700;
}
</style>
