<script setup>
import { computed } from 'vue'
import Avatar from './Avatar.vue'
import { timeAgo } from '../utils/format'

const props = defineProps({
  post: { type: Object, required: true },
  index: { type: Number, default: null },
})

const author = computed(() => props.post.author || {})
const num = computed(() => String(props.index).padStart(2, '0'))
</script>

<template>
  <router-link :to="`/post/${post.postid}`" class="card">
    <div class="card-head between">
      <div class="row gap-3">
        <Avatar :src="author.avatar" :name="author.username" :size="40" />
        <div>
          <div class="card-author">{{ author.username || '匿名' }}</div>
          <div class="small">{{ timeAgo(post.create_time) }}</div>
        </div>
      </div>
      <span v-if="index !== null" class="eyebrow">{{ num }}</span>
    </div>

    <h3 class="card-title">{{ post.title || '无题' }}</h3>
    <p class="card-intro">{{ post.intro }}</p>

    <div class="card-foot between">
      <div class="row gap-3 meta">
        <span v-if="!post.ready" class="tag tag--pending">生成中</span>
        <span>👍 {{ post.like_tot || 0 }}</span>
        <span>💬 {{ post.comment_tot || 0 }}</span>
        <span>☆ {{ post.bookmark_tot || 0 }}</span>
      </div>
      <span class="small">→</span>
    </div>
  </router-link>
</template>

<style scoped>
.card {
  display: block;
  border: 1px solid var(--line);
  border-radius: 2px;
  background: var(--paper);
  padding: 22px 22px 18px;
  transition: border-color 0.15s, transform 0.15s;
}
.card:hover {
  border-color: var(--line-strong);
  transform: translateY(-2px);
}
.card-head {
  margin-bottom: 16px;
}
.card-author {
  font-weight: 700;
  font-size: 0.95rem;
  line-height: 1.3;
}
.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.01em;
  margin-bottom: 8px;
}
.card-intro {
  color: var(--ink-soft);
  font-size: 0.9rem;
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.card-foot {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid var(--line);
}
.meta {
  font-size: 0.82rem;
  color: var(--ink-soft);
}
.tag {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 2px;
}
.tag--pending {
  background: var(--accent-soft);
  color: var(--accent-deep);
}
</style>
