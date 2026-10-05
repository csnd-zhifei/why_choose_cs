<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import { useUser } from '../stores/user'

const router = useRouter()
const { setUser } = useUser()

const form = ref({
  username: '',
  password: '',
  gender: null,
  user_location: '',
})
const error = ref('')
const loading = ref(false)

async function submit() {
  if (!form.value.username || form.value.password.length < 6) {
    error.value = '用户名不能为空，密码至少 6 位'
    return
  }
  loading.value = true
  error.value = ''
  try {
    const u = await api.register({
      username: form.value.username,
      password: form.value.password,
      gender: form.value.gender,
      user_location: form.value.user_location || undefined,
    })
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
      <p class="eyebrow">Sign up</p>
      <h1 class="title">注册</h1>

      <form @submit.prevent="submit">
        <label class="lbl">用户名</label>
        <input v-model="form.username" class="field" type="text" autocomplete="username" />

        <label class="lbl" style="margin-top: 16px">密码</label>
        <input v-model="form.password" class="field" type="password" autocomplete="new-password" />

        <label class="lbl" style="margin-top: 16px">性别（可选）</label>
        <select v-model="form.gender" class="field">
          <option :value="null">保密</option>
          <option :value="0">女</option>
          <option :value="1">男</option>
          <option :value="2">其他</option>
        </select>

        <label class="lbl" style="margin-top: 16px">地区（可选）</label>
        <input v-model="form.user_location" class="field" type="text" placeholder="如：北京" />

        <p v-if="error" class="error-tip">{{ error }}</p>

        <button class="btn btn--primary" style="margin-top: 24px; width: 100%" :disabled="loading">
          {{ loading ? '注册中…' : '注册并登录' }}
        </button>
      </form>

      <p class="small" style="margin-top: 20px">
        已有账号？
        <router-link to="/login" class="link">登录 →</router-link>
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
