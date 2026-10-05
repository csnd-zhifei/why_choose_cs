<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../api'
import { useUser } from '../stores/user'
import Avatar from '../components/Avatar.vue'
import { timeAgo } from '../utils/format'

const route = useRoute()
const router = useRouter()
const { currentUser } = useUser()

const post = ref(null)
const loading = ref(true)
const error = ref('')
let pollTimer = null
const pollCount = ref(0)

const comments = ref([])
const commentText = ref('')
const repliesMap = ref({})
const replyText = ref({})
const openReplies = ref({})

async function loadPost() {
  try {
    post.value = await api.getPost(route.params.id)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function startPoll() {
  stopPoll()
  pollTimer = setInterval(async () => {
    pollCount.value += 1
    try {
      const p = await api.getPost(route.params.id)
      post.value = p
      if (p.ready || pollCount.value > 20) stopPoll()
    } catch {
      /* 忽略单次失败，继续轮询 */
    }
  }, 1500)
}
function stopPoll() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

async function loadComments() {
  try {
    comments.value = await api.listComments(route.params.id)
  } catch {
    comments.value = []
  }
}

function needLogin() {
  if (!currentUser.value) {
    router.push('/login')
    return true
  }
  return false
}

async function toggleLike() {
  if (needLogin()) return
  try {
    const r = await api.toggleLike(post.value.postid, currentUser.value.userid)
    post.value.like_tot = r.like_tot
    post.value.liked = r.is_like
  } catch (e) {
    alert(e.message)
  }
}

async function toggleBookmark() {
  if (needLogin()) return
  try {
    const r = await api.toggleBookmark(post.value.postid, currentUser.value.userid)
    post.value.bookmark_tot = r.bookmark_tot
    post.value.bookmarked = r.is_bookmark
  } catch (e) {
    alert(e.message)
  }
}

async function submitComment() {
  if (needLogin()) return
  const text = commentText.value.trim()
  if (!text) return
  try {
    await api.createComment({
      postid: Number(route.params.id),
      userid: currentUser.value.userid,
      content: text,
    })
    commentText.value = ''
    await loadComments()
    const p = await api.getPost(route.params.id)
    post.value.comment_tot = p.comment_tot
  } catch (e) {
    alert(e.message)
  }
}

async function toggleReplies(commentid) {
  openReplies.value[commentid] = !openReplies.value[commentid]
  if (openReplies.value[commentid] && !repliesMap.value[commentid]) {
    repliesMap.value[commentid] = await api.listReplies(commentid)
  }
}

async function submitReply(comment) {
  if (needLogin()) return
  const text = (replyText.value[comment.commentid] || '').trim()
  if (!text) return
  try {
    await api.createReply(comment.commentid, {
      userid: currentUser.value.userid,
      content: text,
      to_user: comment.userid,
    })
    replyText.value[comment.commentid] = ''
    repliesMap.value[comment.commentid] = await api.listReplies(comment.commentid)
  } catch (e) {
    alert(e.message)
  }
}

onMounted(async () => {
  await loadPost()
  if (post.value) {
    loadComments()
    if (!post.value.ready) startPoll()
  }
})
onBeforeUnmount(stopPoll)
</script>

<template>
  <div class="container detail">
    <p v-if="error" class="error-tip">{{ error }}</p>

    <div v-else-if="loading" class="skeleton" style="height: 300px"></div>

    <template v-else-if="post">
      <!-- 作者 + 标题 -->
      <header class="detail-head">
        <p class="eyebrow">Post / {{ post.postid }}</p>
        <h1 class="title">{{ post.title || '无题' }}</h1>
        <div class="row gap-3 byline">
          <Avatar :src="post.author?.avatar" :name="post.author?.username" :size="44" />
          <div>
            <div class="author-name">{{ post.author?.username || '匿名' }}</div>
            <div class="small">{{ timeAgo(post.create_time) }}</div>
          </div>
        </div>
      </header>

      <!-- 正文看法 -->
      <section class="intro-block">
        <p class="intro-text">{{ post.intro }}</p>
      </section>

      <!-- 操作 -->
      <div class="actions row wrap">
        <button class="btn" :class="post.liked ? 'btn--primary' : 'btn--ghost'" @click="toggleLike">
          👍 {{ post.like_tot || 0 }}
        </button>
        <button class="btn" :class="post.bookmarked ? 'btn--primary' : 'btn--ghost'" @click="toggleBookmark">
          ☆ {{ post.bookmark_tot || 0 }}
        </button>
        <span class="small">💬 {{ post.comment_tot || 0 }} 条评论</span>
      </div>

      <!-- 单页 SPA -->
      <section class="spa-block">
        <div class="between spa-head">
          <h2 class="spa-title">完整页面</h2>
          <span v-if="post.ready" class="eyebrow">SPA</span>
          <span v-else class="eyebrow">生成中…</span>
        </div>
        <div v-if="post.ready" class="frame">
          <iframe :src="post.htmlurl" title="SPA" loading="lazy"></iframe>
        </div>
        <div v-else class="empty">
          <span class="eyebrow">Generating</span>
          <p>正在生成单页内容，请稍候…</p>
        </div>
      </section>

      <!-- 评论 -->
      <section class="comments">
        <h2 class="spa-title">评论 · {{ comments.length }}</h2>

        <div v-if="currentUser" class="composer">
          <textarea v-model="commentText" class="field" rows="3" placeholder="写下你的看法…"></textarea>
          <button class="btn btn--primary btn--sm" @click="submitComment">发表</button>
        </div>
        <p v-else class="small" style="margin: 12px 0">
          <router-link to="/login" class="link">登录</router-link> 后参与评论
        </p>

        <ul class="comment-list">
          <li v-for="c in comments" :key="c.id" class="comment">
            <div class="row gap-3">
              <Avatar :src="c.avatar" :name="c.username" :size="32" />
              <div class="comment-body">
                <div class="row gap-2">
                  <span class="author-name">{{ c.username || '匿名' }}</span>
                  <span class="small">{{ timeAgo(c.create_time) }}</span>
                </div>
                <p class="comment-text">{{ c.content }}</p>

                <button class="link" @click="toggleReplies(c.commentid)">
                  {{ openReplies[c.commentid] ? '收起回复' : `回复 ${(repliesMap[c.commentid] || []).length ? '(' + repliesMap[c.commentid].length + ')' : ''}` }}
                </button>

                <div v-if="openReplies[c.commentid]" class="replies">
                  <div v-for="r in repliesMap[c.commentid] || []" :key="r.id" class="reply">
                    <span class="author-name">{{ r.username }}</span>
                    <span class="small"> · {{ timeAgo(r.create_time) }}</span>
                    <p class="comment-text">{{ r.content }}</p>
                  </div>
                  <div class="row gap-2 reply-composer">
                    <input v-model="replyText[c.commentid]" class="field" placeholder="回复…" />
                    <button class="btn btn--ghost btn--sm" @click="submitReply(c)">发送</button>
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </section>
    </template>
  </div>
</template>

<style scoped>
.detail {
  padding-top: 48px;
  padding-bottom: 80px;
  max-width: 820px;
}
.detail-head .title {
  margin: 10px 0 20px;
}
.byline {
  margin-bottom: 28px;
}
.author-name {
  font-weight: 700;
  font-size: 0.9rem;
}
.intro-block {
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  padding: 24px 0;
  margin-bottom: 24px;
}
.intro-text {
  font-size: 1.02rem;
  line-height: 1.9;
  white-space: pre-wrap;
}
.actions {
  margin-bottom: 40px;
}
.spa-block {
  margin-bottom: 48px;
}
.spa-head {
  margin-bottom: 14px;
}
.spa-title {
  font-size: 1.15rem;
  font-weight: 700;
}
.frame {
  border: 1px solid var(--line);
  border-radius: 2px;
  overflow: hidden;
}
.frame iframe {
  width: 100%;
  height: 640px;
  border: 0;
  display: block;
  background: #fff;
}
.comments {
  border-top: 1px solid var(--line);
  padding-top: 28px;
}
.composer {
  margin: 16px 0 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.composer .btn {
  align-self: flex-end;
}
.comment-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.comment-body {
  flex: 1;
}
.comment-text {
  margin: 4px 0 8px;
  font-size: 0.92rem;
  line-height: 1.7;
}
.link {
  border: 0;
  background: none;
  color: var(--accent);
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0;
}
.replies {
  margin-top: 10px;
  padding-left: 12px;
  border-left: 2px solid var(--line);
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.reply-composer {
  margin-top: 4px;
}
</style>
