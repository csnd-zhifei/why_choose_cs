<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'
import PostCard from '../components/PostCard.vue'

const q = ref('')
const sort = ref('new')
const page = ref(1)
const size = 12
const total = ref(0)
const posts = ref([])
const loading = ref(false)
const error = ref('')

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / size)))

async function load() {
  loading.value = true
  error.value = ''
  try {
    const data = await api.listPosts({
      q: q.value.trim() || undefined,
      sort: sort.value,
      page: page.value,
      size,
    })
    posts.value = data.items
    total.value = data.total
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

let timer
function onSearch() {
  clearTimeout(timer)
  timer = setTimeout(() => {
    page.value = 1
    load()
  }, 300)
}

function setSort(s) {
  if (sort.value === s) return
  sort.value = s
  page.value = 1
  load()
}

function go(p) {
  if (p < 1 || p > totalPages.value || p === page.value) return
  page.value = p
  load()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(load)
</script>

<template>
  <div class="container home">
    <header class="home-head">
      <p class="eyebrow">All posts</p>
      <h1 class="title">大家的看法</h1>

      <div class="controls between wrap">
        <input
          v-model="q"
          class="field search"
          type="search"
          placeholder="搜索标题、正文或摘要…"
          @input="onSearch"
        />
        <div class="row sort">
          <button class="btn btn--sm" :class="sort === 'new' ? 'btn--primary' : 'btn--ghost'" @click="setSort('new')">
            最新
          </button>
          <button class="btn btn--sm" :class="sort === 'hot' ? 'btn--primary' : 'btn--ghost'" @click="setSort('hot')">
            热门
          </button>
        </div>
      </div>
    </header>

    <p v-if="error" class="error-tip">{{ error }}</p>

    <div v-if="loading" class="grid">
      <div v-for="i in 6" :key="i" class="skeleton" style="height: 200px"></div>
    </div>

    <div v-else-if="posts.length" class="grid">
      <PostCard
        v-for="(p, i) in posts"
        :key="p.postid"
        :post="p"
        :index="(page - 1) * size + i + 1"
      />
    </div>

    <div v-else class="empty">
      <span class="eyebrow">No result</span>
      <p>没有找到相关内容，换个关键词试试。</p>
    </div>

    <div v-if="totalPages > 1" class="pager between">
      <button class="btn btn--ghost btn--sm" :disabled="page <= 1" @click="go(page - 1)">← 上一页</button>
      <span class="small">{{ page }} / {{ totalPages }}</span>
      <button class="btn btn--ghost btn--sm" :disabled="page >= totalPages" @click="go(page + 1)">下一页 →</button>
    </div>
  </div>
</template>

<style scoped>
.home {
  padding-top: 48px;
  padding-bottom: 80px;
}
.home-head .title {
  margin: 8px 0 28px;
}
.controls {
  gap: 16px;
  margin-bottom: 32px;
}
.search {
  flex: 1;
  min-width: 260px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.pager {
  margin-top: 36px;
  border-top: 1px solid var(--line);
  padding-top: 20px;
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
