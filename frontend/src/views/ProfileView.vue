<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import { useUser } from '../stores/user'
import Avatar from '../components/Avatar.vue'
import PostCard from '../components/PostCard.vue'

const router = useRouter()
const { currentUser, setUser } = useUser()

const tab = ref('posts')
const posts = ref([])
const bookmarks = ref([])
const loading = ref(false)
const gender = ref(null)
const location = ref('')

onMounted(async () => {
  if (!currentUser.value) {
    router.push('/login')
    return
  }
  try {
    const u = await api.getUser(currentUser.value.userid)
    setUser({ ...currentUser.value, avatar: u.avatar })
    gender.value = u.gender
    location.value = u.user_location || ''
  } catch {
    /* 忽略 */
  }
  load()
})

async function load() {
  loading.value = true
  try {
    const [p, b] = await Promise.all([
      api.listPosts({ userid: currentUser.value.userid, size: 100 }),
      api.listBookmarks({ userid: currentUser.value.userid, size: 100 }),
    ])
    posts.value = p.items
    bookmarks.value = b.items
  } catch {
    /* 忽略 */
  } finally {
    loading.value = false
  }
}

async function onAvatar(e) {
  const file = e.target.files[0]
  if (!file) return
  try {
    const u = await api.uploadAvatar(currentUser.value.userid, file)
    setUser({ ...currentUser.value, avatar: u.avatar })
  } catch (err) {
    alert(err.message)
  }
}

async function saveProfile() {
  try {
    const u = await api.updateUser(currentUser.value.userid, {
      gender: gender.value,
      user_location: location.value.trim() || undefined,
    })
    setUser({ ...currentUser.value, ...u })
    alert('已保存')
  } catch (err) {
    alert(err.message)
  }
}
</script>

<template>
  <div class="container profile">
    <section class="me">
      <div class="row gap-4">
        <label class="avatar-upload">
          <Avatar :src="currentUser?.avatar" :name="currentUser?.username" :size="72" />
          <input type="file" accept=".png,.jpg,.jpeg,.webp,.gif" hidden @change="onAvatar" />
        </label>
        <div>
          <h1 class="title">{{ currentUser?.username }}</h1>
          <p class="eyebrow">User / {{ currentUser?.userid }}</p>
        </div>
      </div>

      <div class="edit row wrap gap-4">
        <div>
          <label class="lbl">性别</label>
          <select v-model="gender" class="field">
            <option :value="null">保密</option>
            <option :value="0">女</option>
            <option :value="1">男</option>
            <option :value="2">其他</option>
          </select>
        </div>
        <div>
          <label class="lbl">地区</label>
          <input v-model="location" class="field" type="text" placeholder="如：北京" />
        </div>
        <button class="btn btn--primary btn--sm" style="align-self: flex-end" @click="saveProfile">保存</button>
      </div>
    </section>

    <div class="tabs">
      <button class="tab" :class="{ active: tab === 'posts' }" @click="tab = 'posts'">
        我的笔记 {{ posts.length }}
      </button>
      <button class="tab" :class="{ active: tab === 'bookmarks' }" @click="tab = 'bookmarks'">
        我的收藏 {{ bookmarks.length }}
      </button>
    </div>

    <div v-if="loading" class="grid">
      <div v-for="i in 3" :key="i" class="skeleton" style="height: 180px"></div>
    </div>
    <div v-else-if="(tab === 'posts' ? posts : bookmarks).length" class="grid">
      <PostCard v-for="(p, i) in tab === 'posts' ? posts : bookmarks" :key="p.postid" :post="p" :index="i + 1" />
    </div>
    <div v-else class="empty">
      <span class="eyebrow">Empty</span>
      <p>{{ tab === 'posts' ? '还没有发布过笔记。' : '还没有收藏任何笔记。' }}</p>
    </div>
  </div>
</template>

<style scoped>
.profile {
  padding-top: 48px;
  padding-bottom: 80px;
}
.me {
  display: flex;
  flex-wrap: wrap;
  gap: 32px;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid var(--line);
  padding-bottom: 32px;
  margin-bottom: 28px;
}
.avatar-upload {
  cursor: pointer;
}
.edit {
  gap: 16px;
}
.edit .field {
  min-width: 140px;
}
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid var(--line);
  margin-bottom: 24px;
}
.tab {
  border: 0;
  background: none;
  padding: 12px 20px;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--ink-soft);
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
}
.tab.active {
  color: var(--ink);
  border-bottom-color: var(--accent);
}
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
@media (max-width: 900px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 560px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
