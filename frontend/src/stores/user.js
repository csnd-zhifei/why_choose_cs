import { ref } from 'vue'

// 当前登录用户。后端暂未实现 token，登录后只保存 userid + 基础信息到本地。
const KEY = 'cs_why_user'

function load() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || 'null')
  } catch {
    return null
  }
}

const currentUser = ref(load())

function setUser(user) {
  currentUser.value = user
  localStorage.setItem(KEY, JSON.stringify(user))
}

function logout() {
  currentUser.value = null
  localStorage.removeItem(KEY)
}

export function useUser() {
  return { currentUser, setUser, logout }
}
