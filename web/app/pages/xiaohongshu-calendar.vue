<template>
  <div class="calendar-page">
    <div class="page-header">
      <h2 class="page-title">发小红书安排</h2>
      <NuxtLink to="/xhs-schedule" class="header-link">添加发布安排</NuxtLink>
    </div>

    <div class="week-wrapper">
      <XhsWeekdayPicker
        :selected-weekday="weekday"
        :marked-weekdays="markedWeekdays"
        @select="handleWeekdaySelect"
      />
    </div>

    <div class="schedule-panel">
      <h3 class="schedule-title">{{ weekdayTitle }} 发布安排</h3>

      <div v-if="loading" class="panel-loading">加载中...</div>

      <el-tabs
        v-else
        v-model="student"
        type="card"
        class="student-tabs"
      >
        <el-tab-pane
          v-for="group in studentGroups"
          :key="group.student"
          :label="studentLabel(group.student)"
          :name="group.student"
        >
          <div class="period-tabs-wrap">
            <div class="period-nav-scroll">
              <button
                v-for="post in group.posts"
                :key="post.period"
                type="button"
                class="period-nav-item"
                :class="{ 'is-active': periodForStudent(group.student) === post.period }"
                @click="selectPeriod(group.student, post.period, $event)"
              >
                <span class="period-nav-name">{{ periodLabel(post.period) }}</span>
                <span class="period-nav-time">{{ periodTime(post.period) }}</span>
              </button>
            </div>

            <div
              v-for="post in group.posts"
              :key="'panel-' + post.period"
              v-show="periodForStudent(group.student) === post.period"
              class="period-panel"
            >
              <div class="post-view">
                <div class="post-view-top">
                  <div class="best-time-tip">
                    🕐 最佳发布时间：{{ periodLabel(post.period) }} {{ periodTime(post.period) }}
                  </div>
                  <span v-if="post.isHot" class="hot-badge">🔥 爆文</span>
                </div>

                <div class="view-item">
                  <div class="view-label-row">
                    <span class="view-label">大字报文字</span>
                    <el-button
                      v-if="post.posterText"
                      class="copy-btn"
                      type="primary"
                      size="small"
                      plain
                      @click="copyText(post.posterText, '大字报文字')"
                    >
                      点击复制
                    </el-button>
                  </div>
                  <p
                    v-if="post.posterText"
                    class="view-text poster-text copyable"
                    title="点击复制大字报文字"
                    @click="copyText(post.posterText, '大字报文字')"
                  >
                    {{ post.posterText }}
                  </p>
                  <p v-else class="view-text view-empty-block">暂无大字报文字</p>
                </div>

                <div class="view-item">
                  <div class="view-label-row">
                    <span class="view-label">标题</span>
                    <el-button
                      v-if="post.title"
                      class="copy-btn"
                      type="primary"
                      size="small"
                      plain
                      @click="copyText(post.title, '标题')"
                    >
                      点击复制
                    </el-button>
                  </div>
                  <p
                    v-if="post.title"
                    class="view-text title-text copyable"
                    title="点击复制标题"
                    @click="copyText(post.title, '标题')"
                  >
                    {{ post.title }}
                  </p>
                  <p v-else class="view-text view-empty-block">暂无标题</p>
                </div>

                <div class="view-item">
                  <span class="view-label">配图</span>
                  <template v-if="post.images && post.images.length">
                    <p class="image-hint">📌 点击配图全屏预览，长按可保存到相册</p>
                    <div class="image-preview">
                      <div
                        v-for="(img, i) in post.images"
                        :key="i"
                        class="thumb-wrap"
                      >
                        <span class="thumb-index">{{ i + 1 }}</span>
                        <img
                          :src="img"
                          class="preview-thumb"
                          alt="配图"
                          @click="openImagePreview(post.images, i)"
                        />
                      </div>
                    </div>
                  </template>
                  <p v-else class="view-text view-empty-block">暂无配图</p>
                </div>

                <div class="view-item">
                  <div class="view-label-row">
                    <span class="view-label">文案</span>
                    <el-button
                      v-if="post.content"
                      class="copy-btn"
                      type="primary"
                      size="small"
                      plain
                      @click="copyText(post.content, '文案')"
                    >
                      点击复制
                    </el-button>
                  </div>
                  <p
                    v-if="post.content"
                    class="view-text view-content copyable"
                    title="点击复制文案"
                    @click="copyText(post.content, '文案')"
                  >
                    {{ post.content }}
                  </p>
                  <p v-else class="view-text view-empty-block">暂无文案</p>
                </div>

                <div class="view-item">
                  <span class="view-label">所挂商品</span>
                  <div v-if="post.products && post.products.length" class="product-tags">
                    <el-tag
                      v-for="(prod, i) in post.products"
                      :key="i"
                      type="danger"
                      effect="light"
                      round
                    >
                      {{ prod }}
                    </el-tag>
                  </div>
                  <p v-else class="view-text view-empty-block">暂无所挂商品</p>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 全屏配图预览 -->
    <ClientOnly>
      <Teleport to="body">
        <div
          v-if="previewVisible"
          class="image-viewer"
          @click.self="closeImagePreview"
        >
          <div class="viewer-toolbar">
            <span v-if="previewImages.length > 1" class="viewer-counter">
              {{ previewIndex + 1 }} / {{ previewImages.length }}
            </span>
            <span v-if="isMobile" class="viewer-tip">左右滑动切换 · 长按保存</span>
            <div class="viewer-actions">
              <button
                v-if="isMobile"
                type="button"
                class="viewer-save-btn"
                @click.stop="savePreviewImage"
              >
                存相册
              </button>
              <button
                type="button"
                class="viewer-close-btn"
                aria-label="关闭"
                @click.stop="closeImagePreview"
              >
                ✕
              </button>
            </div>
          </div>

          <div
            class="viewer-stage"
            @touchstart.passive="onViewerTouchStart"
            @touchend="onViewerTouchEnd"
          >
            <button
              v-if="previewImages.length > 1"
              type="button"
              class="viewer-nav viewer-prev"
              aria-label="上一张"
              @click.stop="shiftPreview(-1)"
            >
              ‹
            </button>

            <img
              v-if="previewImages[previewIndex]"
              :key="previewIndex"
              :src="previewImages[previewIndex]"
              class="viewer-img"
              alt="配图预览"
              @click.stop
            />

            <button
              v-if="previewImages.length > 1"
              type="button"
              class="viewer-nav viewer-next"
              aria-label="下一张"
              @click.stop="shiftPreview(1)"
            >
              ›
            </button>
          </div>
        </div>
      </Teleport>
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import {
  type Student,
  STUDENT_ORDER,
  studentLabel
} from '~/data/xhsStudents'
import { extFromImageUrl, saveImageToDevice } from '~/utils/saveImage'
import { type Weekday, weekdayLabel } from '~/utils/xhsWeekday'
import { fetchXhsPostsByWeekday } from '~/utils/xhsPostsApi'

definePageMeta({
  layout: 'plain'
})

type Period = 'morning' | 'noon' | 'evening' | 'night' | 'late_night'

interface PostView {
  id: number
  student: Student
  period: Period
  posterText: string
  title: string
  isHot: boolean
  images: string[]
  content: string
  products: string[]
}

const periodLabels: Record<Period, string> = {
  morning: '早上',
  noon: '中午',
  evening: '初晚',
  night: '中晚',
  late_night: '深晚'
}
// 各时段最佳发布时间
const periodTimes: Record<Period, string> = {
  morning: '7:30-8:30',
  noon: '11:30-12:30',
  evening: '19:30-21:00',
  night: '21:30-22:30',
  late_night: '22:30-23:30'
}
const periodOrder: Period[] = ['morning', 'noon', 'evening', 'night', 'late_night']
const periodLabel = (p: string) => periodLabels[p as Period] || p
const periodTime = (p: string) => periodTimes[p as Period] || ''

const selectPeriod = (stu: Student, p: Period, event?: Event) => {
  student.value = stu
  period.value = p
  const btn = event?.currentTarget as HTMLElement | undefined
  btn?.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
}

const studentOrder = STUDENT_ORDER

const isMobile = useIsMobile()
const {
  weekday,
  student,
  period,
  markedWeekdays,
  scheduleLink,
  loadMarkedWeekdays
} = useXhsScheduleFilters()

const weekdayTitle = computed(() => weekdayLabel(weekday.value))

// 各账号在当前会话内记住上次查看的时段；URL 保存当前激活账号的时段
const periodByStudent = reactive<Record<Student, Period>>(
  Object.fromEntries(
    STUDENT_ORDER.map((s) => [s, 'morning' as Period])
  ) as Record<Student, Period>
)
periodByStudent[student.value] = period.value

const periodForStudent = (stu: Student) =>
  stu === student.value ? period.value : periodByStudent[stu]

watch(period, (p) => {
  periodByStudent[student.value] = p
})

watch(student, (stu) => {
  period.value = periodByStudent[stu] || 'morning'
})

const loading = ref(false)
const previewVisible = ref(false)
const previewImages = ref<string[]>([])
const previewIndex = ref(0)

// 当天的发布内容（只读）
const dayPosts = ref<PostView[]>([])

const emptyPostView = (student: Student, period: Period): PostView => ({
  id: 0,
  student,
  period,
  posterText: '',
  title: '',
  isHot: false,
  images: [],
  content: '',
  products: []
})

// 号1～4 × 早中晚四时段始终展示，无数据时用空占位
const studentGroups = computed(() =>
  studentOrder.map((student) => ({
    student,
    posts: periodOrder.map((period) => {
      const found = dayPosts.value.find(
        (p) => p.student === student && p.period === period
      )
      return found || emptyPostView(student, period)
    })
  }))
)

// 点击复制文本（标题 / 文案）
const copyText = async (text: string, label: string) => {
  if (!text) return
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text)
    } else {
      // 降级方案：在不支持 Clipboard API 的环境下使用 textarea
      const ta = document.createElement('textarea')
      ta.value = text
      ta.style.position = 'fixed'
      ta.style.opacity = '0'
      document.body.appendChild(ta)
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
    }
    ElMessage.success('复制成功')
  } catch (error) {
    console.error('复制失败', error)
    ElMessage.error('复制失败，请手动选择文本复制')
  }
}

const openImagePreview = (images: string[], index: number) => {
  previewImages.value = images
  previewIndex.value = index
  previewVisible.value = true
}

const closeImagePreview = () => {
  previewVisible.value = false
}

const shiftPreview = (delta: number) => {
  const total = previewImages.value.length
  if (total <= 1) return
  previewIndex.value = (previewIndex.value + delta + total) % total
}

const SWIPE_THRESHOLD = 48
const SWIPE_MAX_VERTICAL = 72

const swipeStart = { x: 0, y: 0, active: false }

const onViewerTouchStart = (e: TouchEvent) => {
  if (previewImages.value.length <= 1) return
  const touch = e.touches[0]
  if (!touch) return
  swipeStart.x = touch.clientX
  swipeStart.y = touch.clientY
  swipeStart.active = true
}

const onViewerTouchEnd = (e: TouchEvent) => {
  if (!swipeStart.active || previewImages.value.length <= 1) return
  swipeStart.active = false
  const touch = e.changedTouches[0]
  if (!touch) return
  const dx = touch.clientX - swipeStart.x
  const dy = touch.clientY - swipeStart.y
  // 纵向滑动为主时不切换（避免与页面滚动冲突）
  if (Math.abs(dy) > SWIPE_MAX_VERTICAL && Math.abs(dy) > Math.abs(dx)) return
  if (Math.abs(dx) < SWIPE_THRESHOLD) return
  // 左滑下一张，右滑上一张
  shiftPreview(dx < 0 ? 1 : -1)
}

const onPreviewKeydown = (e: KeyboardEvent) => {
  if (!previewVisible.value) return
  if (e.key === 'ArrowLeft') shiftPreview(-1)
  else if (e.key === 'ArrowRight') shiftPreview(1)
  else if (e.key === 'Escape') closeImagePreview()
}

const savePreviewImage = async () => {
  const url = previewImages.value[previewIndex.value]
  if (!url) return
  const filename = `${weekday.value}_${previewIndex.value + 1}.${extFromImageUrl(url)}`
  try {
    const result = await saveImageToDevice(url, filename)
    if (result === 'shared') {
      ElMessage.success('请在分享面板选择「存储到相册」')
    } else if (result === 'downloaded') {
      ElMessage.success('图片已开始下载')
    }
  } catch (error: unknown) {
    if (error instanceof Error && error.name === 'AbortError') return
    ElMessage.info('请长按图片保存到相册')
  }
}

watch(previewVisible, (visible) => {
  if (typeof document === 'undefined') return
  document.body.style.overflow = visible ? 'hidden' : ''
  if (visible) {
    window.addEventListener('keydown', onPreviewKeydown)
  } else {
    window.removeEventListener('keydown', onPreviewKeydown)
    swipeStart.active = false
  }
})

const handleWeekdaySelect = (w: Weekday) => {
  weekday.value = w
}

const loadWeekday = async (weekday: Weekday) => {
  loading.value = true
  dayPosts.value = []
  try {
    const list = await fetchXhsPostsByWeekday(weekday)
    dayPosts.value = list.map((item: any): PostView => ({
      id: item.id,
      student: (item.student || 'a') as Student,
      period: item.period,
      posterText: item.poster_text || '',
      title: item.title || '',
      isHot: Boolean(item.is_hot),
      images: item.images || [],
      content: item.content || '',
      products: Array.isArray(item.products) ? item.products : []
    }))
  } catch (error) {
    console.error('加载内容失败', error)
    ElMessage.error('加载内容失败')
  } finally {
    loading.value = false
  }
}

watch(weekday, (w) => {
  if (w) loadWeekday(w)
}, { immediate: true })

onMounted(() => {
  loadMarkedWeekdays()
})

onUnmounted(() => {
  window.removeEventListener('keydown', onPreviewKeydown)
  if (typeof document !== 'undefined') {
    document.body.style.overflow = ''
  }
})

useSEO({
  title: '发小红书安排',
  description: '查看小红书发布安排，按周一至周日选择，为 号1 / 号2 / 号3 / 号4 分别展示早上、中午、傍晚、晚上四个时段的发布内容。'
})
</script>

<style scoped>
.calendar-page {
  animation: fadeIn 0.5s ease-in;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 3px solid #667eea;
}

.page-title {
  font-size: 2.5rem;
  color: #333;
  margin: 0;
}

.header-link {
  color: #667eea;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
  padding-bottom: 0.35rem;
}

.header-link:hover {
  text-decoration: underline;
}

.calendar-wrapper,
.week-wrapper {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.25rem;
}

.schedule-panel {
  background: white;
  padding: 1.5rem 2rem 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.schedule-title {
  margin: 0 0 1.25rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #eef0f7;
}

.panel-loading,
.panel-empty {
  text-align: center;
  padding: 2.5rem 0;
  color: #999;
  font-size: 1.05rem;
}

.post-view {
  padding: 0.5rem 0.25rem;
}

/* 最佳发布时间提示条 */
.post-view-top {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.post-view-top .best-time-tip {
  margin-bottom: 0;
  flex: 1;
}

.hot-badge {
  flex-shrink: 0;
  padding: 0.35rem 0.75rem;
  background: linear-gradient(135deg, #ff2442 0%, #ff6b35 100%);
  color: #fff;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 999px;
  white-space: nowrap;
  box-shadow: 0 2px 6px rgba(255, 36, 66, 0.3);
}

.best-time-tip {
  margin-bottom: 1.25rem;
  padding: 0.6rem 1rem;
  background: #fff0f3;
  border-left: 3px solid #ff2442;
  border-radius: 4px;
  color: #d81e06;
  font-size: 0.9rem;
}

.view-item {
  margin-bottom: 1.25rem;
}

.view-label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 600;
  color: #667eea;
  font-size: 0.95rem;
}

.view-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.4rem;
}

.view-label-row .view-label {
  margin-bottom: 0;
}

.copy-btn {
  --el-button-hover-text-color: #fff;
  --el-button-hover-bg-color: #667eea;
  --el-button-hover-border-color: #667eea;
  padding: 4px 14px;
  height: 28px;
  font-size: 0.78rem;
  font-weight: 500;
  border-radius: 999px;
  border-color: #d0d7ff;
  color: #667eea;
  background: #f7f8fc;
  flex-shrink: 0;
}

.copy-btn:active {
  transform: scale(0.97);
}

.view-text {
  margin: 0;
  color: #333;
  line-height: 1.6;
}

.view-empty-block {
  padding: 0.5rem 0.7rem;
  border-radius: 6px;
  background: #fafafa;
  border: 1px dashed #e4e7ed;
  color: #bbb;
  font-size: 0.92rem;
}

/* 可点击复制的文本块 */
.copyable {
  cursor: pointer;
  padding: 0.5rem 0.7rem;
  border-radius: 6px;
  background: #f7f8fc;
  border: 1px solid #eef0f7;
  transition: background 0.2s, border-color 0.2s;
}

.copyable:hover {
  background: #eef1ff;
  border-color: #c7cffb;
}

.poster-text {
  font-size: 1.35rem;
  font-weight: 700;
  line-height: 1.45;
  color: #ff2442;
  text-align: center;
  letter-spacing: 0.02em;
}

.title-text {
  font-size: 1.05rem;
  font-weight: 600;
  line-height: 1.55;
  color: #222;
}

.view-content {
  white-space: pre-wrap;
}

.image-hint {
  margin: 0 0 0.6rem;
  color: #ff2442;
  font-size: 0.85rem;
}

.image-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.product-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.thumb-wrap {
  position: relative;
  width: 96px;
}

.thumb-index {
  position: absolute;
  top: 4px;
  left: 4px;
  z-index: 1;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  border-radius: 9px;
  background: rgba(255, 36, 66, 0.9);
  color: #fff;
  font-size: 0.7rem;
  line-height: 18px;
  text-align: center;
}

.preview-thumb {
  display: block;
  width: 96px;
  height: 96px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #eee;
  cursor: zoom-in;
}

/* 全屏配图预览 */
.image-viewer {
  position: fixed;
  inset: 0;
  z-index: 10000;
  background: rgba(0, 0, 0, 0.92);
  display: flex;
  flex-direction: column;
  padding: 56px 0 24px;
  touch-action: none;
}

.viewer-stage {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 0;
  padding: 0 12px;
  touch-action: pan-y pinch-zoom;
}

.viewer-toolbar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 12px 16px;
  padding-top: calc(12px + env(safe-area-inset-top, 0px));
  color: #fff;
  z-index: 2;
}

.viewer-counter {
  font-size: 0.85rem;
  opacity: 0.9;
}

.viewer-tip {
  flex: 1;
  text-align: center;
  font-size: 0.82rem;
  opacity: 0.85;
}

.viewer-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.viewer-save-btn {
  border: 1px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  border-radius: 999px;
  padding: 6px 14px;
  font-size: 0.82rem;
  cursor: pointer;
}

.viewer-close-btn {
  border: none;
  background: transparent;
  color: #fff;
  font-size: 1.4rem;
  line-height: 1;
  padding: 4px 8px;
  cursor: pointer;
}

.viewer-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.6rem;
  line-height: 1;
  cursor: pointer;
  z-index: 2;
}

.viewer-prev {
  left: 12px;
}

.viewer-next {
  right: 12px;
}

.viewer-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 4px;
  -webkit-touch-callout: default;
  touch-callout: default;
  user-select: auto;
  -webkit-user-select: auto;
  pointer-events: auto;
  animation: viewerFadeIn 0.18s ease;
}

@keyframes viewerFadeIn {
  from {
    opacity: 0.55;
  }
  to {
    opacity: 1;
  }
}

.period-tabs-wrap {
  margin-bottom: 0.5rem;
}

/* 时段标签：横向滑动，手指左右划即可 */
.period-nav-scroll {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-x: contain;
  scroll-snap-type: x proximity;
  padding: 0.25rem 0 0.75rem;
  margin-bottom: 0.75rem;
  scrollbar-width: none;
  touch-action: pan-x;
}

.period-nav-scroll::-webkit-scrollbar {
  display: none;
}

.period-nav-item {
  flex: 0 0 auto;
  scroll-snap-align: start;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
  padding: 0.45rem 0.85rem;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  background: #fff;
  color: #606266;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, color 0.2s;
}

.period-nav-item.is-active {
  border-color: #667eea;
  background: #eef1ff;
  color: #667eea;
}

.period-nav-name {
  font-size: 0.95rem;
  font-weight: 500;
  white-space: nowrap;
}

.period-nav-time {
  font-size: 0.72rem;
  color: #909399;
  white-space: nowrap;
}

.period-nav-item.is-active .period-nav-time {
  color: #667eea;
}

.student-tabs > :deep(.el-tabs__header) {
  margin-bottom: 1rem;
}

.student-tabs > :deep(.el-tabs__header .el-tabs__item) {
  font-size: 1.05rem;
  font-weight: 500;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 移动端适配 */
@media (max-width: 768px) {
  .page-header {
    margin-bottom: 1rem;
  }

  .page-title {
    font-size: 1.6rem;
  }

  .header-link {
    font-size: 0.9rem;
    padding-bottom: 0.15rem;
  }

  .week-wrapper,
  .schedule-panel {
    padding: 0.75rem;
    border-radius: 8px;
  }

  .schedule-title {
    font-size: 1.05rem;
    margin-bottom: 1rem;
  }

  .post-view {
    padding: 0.25rem 0;
  }

  .view-item {
    margin-bottom: 1rem;
  }

  /* 配图：移动端三列自适应，缩略图随屏幕宽度放大 */
  .image-preview {
    gap: 0.6rem;
  }

  .thumb-wrap {
    width: calc((100% - 1.2rem) / 3);
    max-width: 110px;
  }

  .preview-thumb {
    width: 100%;
    height: auto;
    aspect-ratio: 1 / 1;
  }

  /* 号1-4 标签：隐藏箭头，支持手指滑动 */
  .student-tabs > :deep(.el-tabs__nav-prev),
  .student-tabs > :deep(.el-tabs__nav-next) {
    display: none;
  }

  .student-tabs > :deep(.el-tabs__nav-wrap) {
    overflow: visible;
    padding: 0;
  }

  .student-tabs > :deep(.el-tabs__nav-scroll) {
    overflow-x: auto !important;
    overflow-y: hidden;
    -webkit-overflow-scrolling: touch;
    overscroll-behavior-x: contain;
    touch-action: pan-x;
    scrollbar-width: none;
  }

  .student-tabs > :deep(.el-tabs__nav-scroll::-webkit-scrollbar) {
    display: none;
  }

  .student-tabs > :deep(.el-tabs__nav) {
    white-space: nowrap;
    transform: none !important;
  }

  .period-nav-item {
    padding: 0.4rem 0.75rem;
  }

  .period-nav-name {
    font-size: 0.88rem;
  }

  .period-nav-time {
    font-size: 0.68rem;
  }
}

@media (max-width: 380px) {
  .period-nav-item {
    padding: 0.35rem 0.6rem;
  }
}
</style>
