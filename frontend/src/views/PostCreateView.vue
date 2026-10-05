<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../api'
import { useUser } from '../stores/user'

const route = useRoute()
const router = useRouter()
const { currentUser } = useUser()

const isEdit = computed(() => route.name === 'post-edit')
const postId = computed(() => route.params.id)

const title = ref('')
const intro = ref('')
const mdFile = ref(null)
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  if (isEdit.value) {
    try {
      const p = await api.getPost(postId.value)
      title.value = p.title || ''
      intro.value = p.intro
    } catch (e) {
      error.value = e.message
    }
  } else if (!currentUser.value) {
    router.push('/login')
  }
})

function onFile(e) {
  mdFile.value = e.target.files[0] || null
}

async function submit() {
  if (!intro.value.trim()) {
    error.value = '正文不能为空'
    return
  }
  loading.value = true
  error.value = ''
  try {
    if (isEdit.value) {
      await api.updatePost(postId.value, {
        title: title.value.trim() || undefined,
        intro: intro.value.trim(),
      })
      if (mdFile.value) {
        await api.uploadMd(postId.value, mdFile.value)
      }
      router.push(`/post/${postId.value}`)
    } else {
      const p = await api.createPost({
        userid: currentUser.value.userid,
        title: title.value.trim() || undefined,
        intro: intro.value.trim(),
      })
      router.push(`/post/${p.postid}`)
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container editor">
    <p class="eyebrow">{{ isEdit ? 'Edit' : 'New' }}</p>
    <h1 class="title">{{ isEdit ? '编辑笔记' : '写下你的看法' }}</h1>

    <form class="form" @submit.prevent="submit">
      <label class="lbl">标题（可选）</label>
      <input v-model="title" class="field" type="text" placeholder="给这篇分享起个标题" />

      <label class="lbl" style="margin-top: 20px">正文</label>
      <textarea
        v-model="intro"
        class="field"
        rows="12"
        placeholder="你为什么选择 CS？讲讲你的经历、想法、选择…"
      ></textarea>

      <label v-if="isEdit" class="lbl" style="margin-top: 20px">Markdown 文件（可选，替换正文）</label>
      <input v-if="isEdit" class="field" type="file" accept=".md,.markdown" @change="onFile" />

      <p v-if="error" class="error-tip">{{ error }}</p>

      <div class="row gap-3" style="margin-top: 28px">
        <button class="btn btn--primary" :disabled="loading">
          {{ loading ? '提交中…' : isEdit ? '保存' : '发布' }}
        </button>
        <button type="button" class="btn btn--ghost" @click="router.back()">取消</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.editor {
  padding-top: 48px;
  padding-bottom: 80px;
  max-width: 720px;
}
.editor .title {
  margin: 8px 0 32px;
}
.form .field {
  margin-bottom: 4px;
}
</style>
