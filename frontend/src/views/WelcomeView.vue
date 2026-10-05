<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="welcome">
    <div class="container">
      <header class="top between">
        <span class="brand">
          <span class="brand-mark">CS</span>
          <span>为啥选</span>
        </span>
        <span class="eyebrow">01 / 关于</span>
      </header>

      <div class="hero">
        <div class="hero-main">
          <p class="eyebrow">为 CS 学生 · 分享与浏览</p>
          <h1 class="display">
            你为什么<br />
            选择<span class="accent"> CS</span>？
          </h1>
          <p class="lead">
            这里收录不同背景的人对「为什么选择计算机」的真实回答。
            浏览他人的看法，也分享你自己的故事。
          </p>
          <div class="cta row wrap">
            <button class="btn btn--primary" @click="router.push('/quiz')">快问快答</button>
            <button class="btn btn--ghost" @click="router.push('/home')">直接进入</button>
          </div>
        </div>

        <aside class="hero-aside">
          <div class="square"></div>
          <div class="aside-meta">
            <span class="eyebrow">Est. 2026</span>
            <span class="eyebrow">CS / 观点 / 故事</span>
          </div>
        </aside>
      </div>

      <footer class="foot between">
        <span class="small">从一次选择开始，理解一条道路。</span>
        <span class="small">↓ 快问快答 · 四道小题</span>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.welcome {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
}
.welcome .container {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.top {
  padding: 28px 0;
}
.brand {
  display: inline-flex;
  align-items: baseline;
  gap: 6px;
  font-weight: 700;
  font-size: 1.05rem;
}
.brand-mark {
  font-family: var(--mono);
  font-size: 0.8rem;
  background: var(--ink);
  color: var(--bg);
  padding: 2px 6px;
  border-radius: 2px;
}

.hero {
  flex: 1;
  display: grid;
  grid-template-columns: 7fr 3fr;
  gap: 40px;
  align-items: center;
  padding: 40px 0;
}
.hero-main .display {
  margin: 18px 0 26px;
}
.hero-main .accent {
  color: var(--accent);
}
.hero-main .lead {
  margin-bottom: 36px;
}
.cta {
  gap: 14px;
}

.hero-aside {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: flex-end;
}
.square {
  width: 120px;
  height: 120px;
  background: var(--accent);
  border-radius: 2px;
}
.aside-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.foot {
  border-top: 1px solid var(--line);
  padding: 22px 0 30px;
}

@media (max-width: 760px) {
  .hero {
    grid-template-columns: 1fr;
  }
  .hero-aside {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
  .square {
    width: 72px;
    height: 72px;
  }
  .aside-meta {
    align-items: flex-start;
  }
}
</style>
