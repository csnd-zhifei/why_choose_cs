<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const questions = [
  { id: 'drink', label: 'Coffee or Tea？', options: ['咖啡', '茶'] },
  { id: 'pet', label: 'Cat or Dog？', options: ['猫', '狗'] },
  { id: 'machine', label: 'Mac or PC？', options: ['Mac', 'PC'] },
  { id: 'lang', label: '最喜欢的语言？', options: ['Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust'] },
]

const step = ref(0)
const answers = ref({})
const customLang = ref('')

const q = computed(() => questions[step.value])
const isLast = computed(() => step.value === questions.length - 1)
const progress = computed(() => `${String(step.value + 1).padStart(2, '0')} / 04`)

const canNext = computed(() => {
  if (q.value.id === 'lang') {
    return !!answers.value.lang || !!customLang.value.trim()
  }
  return !!answers.value[q.value.id]
})

function pick(opt) {
  answers.value[q.value.id] = opt
}

function next() {
  if (!canNext.value) return
  if (isLast.value) {
    finish()
    return
  }
  step.value += 1
}

function finish() {
  const lang = answers.value.lang || customLang.value.trim()
  try {
    localStorage.setItem('cs_why_quiz', JSON.stringify({ ...answers.value, lang }))
  } catch {
    /* ignore */
  }
  router.push('/home')
}

function skip() {
  router.push('/home')
}
</script>

<template>
  <div class="quiz">
    <div class="container">
      <header class="top between">
        <span class="eyebrow">快问快答</span>
        <button class="link" @click="skip">跳过 →</button>
      </header>

      <div class="body">
        <p class="eyebrow">{{ progress }}</p>
        <h1 class="title">{{ q.label }}</h1>

        <div class="options">
          <button
            v-for="opt in q.options"
            :key="opt"
            class="opt"
            :class="{ active: answers[q.id] === opt }"
            @click="pick(opt)"
          >
            {{ opt }}
          </button>

          <input
            v-if="q.id === 'lang'"
            v-model="customLang"
            class="field custom"
            placeholder="或输入其他语言…"
          />
        </div>

        <div class="actions between">
          <button v-if="step > 0" class="btn btn--ghost" @click="step--">← 上一题</button>
          <span v-else></span>
          <button class="btn btn--primary" :disabled="!canNext" @click="next">
            {{ isLast ? '完成，进入' : '下一题 →' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quiz {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  flex-direction: column;
}
.top {
  padding: 28px 0;
}
.link {
  border: 0;
  background: none;
  color: var(--ink-soft);
  font-size: 0.85rem;
}
.link:hover {
  color: var(--accent);
}
.body {
  padding: 60px 0;
  max-width: 640px;
}
.body .title {
  margin: 16px 0 40px;
}
.options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 480px;
}
.opt {
  text-align: left;
  padding: 16px 18px;
  border: 1px solid var(--line);
  background: var(--paper);
  font-size: 1rem;
  font-weight: 700;
  border-radius: 2px;
  transition: border-color 0.15s, background 0.15s;
}
.opt:hover {
  border-color: var(--ink);
}
.opt.active {
  border-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent-deep);
}
.custom {
  margin-top: 4px;
}
.actions {
  margin-top: 44px;
  border-top: 1px solid var(--line);
  padding-top: 24px;
}
</style>
