<template>
  <div class="calendar-page">
    <h2 class="page-title">发小红书日历</h2>

    <div class="calendar-wrapper">
      <ClientOnly>
        <el-calendar v-model="currentDate">
          <template #date-cell="{ data }">
            <div class="cell-content" @click="handleDateClick(data)">
              <span class="cell-day">{{ data.day.split('-').slice(2).join('') }}</span>
              <span v-if="markedDays.has(data.day)" class="cell-dot" />
            </div>
          </template>
        </el-calendar>
        <template #fallback>
          <div class="calendar-loading">日历加载中...</div>
        </template>
      </ClientOnly>
    </div>

    <!-- 日期详情弹窗（只读展示） -->
    <ClientOnly>
      <el-dialog
        v-model="dialogVisible"
        :title="`${selectedDate} 发布安排`"
        width="680px"
        :align-center="!isMobile"
        :fullscreen="isMobile"
        class="post-dialog"
      >
        <div v-if="loading" class="dialog-loading">加载中...</div>

        <div v-else-if="dayPosts.length === 0" class="dialog-empty">
          当天暂无发布安排
        </div>

        <el-tabs
          v-else
          v-model="activeStudent"
          type="card"
          class="student-tabs"
        >
          <el-tab-pane
            v-for="group in studentGroups"
            :key="group.student"
            :label="studentLabel(group.student)"
            :name="group.student"
          >
            <el-tabs v-model="activeTabByStudent[group.student]" class="period-tabs">
              <el-tab-pane
                v-for="post in group.posts"
                :key="post.period"
                :label="`${periodLabel(post.period)} ${periodTime(post.period)}`"
                :name="post.period"
              >
                <div class="post-view">
                  <div class="best-time-tip">
                    🕐 最佳发布时间：{{ periodLabel(post.period) }} {{ periodTime(post.period) }}
                  </div>

                  <div v-if="post.title" class="view-item">
                    <div class="view-label-row">
                      <span class="view-label">标题</span>
                      <el-button
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
                      class="view-text copyable"
                      title="点击复制标题"
                      @click="copyText(post.title, '标题')"
                    >
                      {{ post.title }}
                    </p>
                  </div>

                  <div v-if="post.images && post.images.length" class="view-item">
                    <span class="view-label">配图</span>
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
                  </div>

                  <div v-if="post.content" class="view-item">
                    <div class="view-label-row">
                      <span class="view-label">文案</span>
                      <el-button
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
                      class="view-text view-content copyable"
                      title="点击复制文案"
                      @click="copyText(post.content, '文案')"
                    >
                      {{ post.content }}
                    </p>
                  </div>

                  <div v-if="post.products && post.products.length" class="view-item">
                    <span class="view-label">所挂商品</span>
                    <div class="product-tags">
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
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </el-tab-pane>
        </el-tabs>
      </el-dialog>

      <!-- 自定义全屏预览：原生 img，支持长按保存 -->
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
            <span v-if="isMobile" class="viewer-tip">长按图片保存到相册</span>
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

type Period = 'morning' | 'noon' | 'evening' | 'night'

interface PostView {
  id: number
  student: Student
  period: Period
  title: string
  images: string[]
  content: string
  products: string[]
}

const periodLabels: Record<Period, string> = {
  morning: '早上',
  noon: '中午',
  evening: '傍晚',
  night: '晚上'
}
// 各时段最佳发布时间
const periodTimes: Record<Period, string> = {
  morning: '7:30-8:30',
  noon: '11:30-12:30',
  evening: '18:30-19:30',
  night: '21:00-22:00'
}
const periodOrder: Period[] = ['morning', 'noon', 'evening', 'night']
const periodLabel = (p: string) => periodLabels[p as Period] || p
const periodTime = (p: string) => periodTimes[p as Period] || ''

const studentOrder = STUDENT_ORDER

const currentDate = ref(new Date())
// 是否移动端（≤768px）：移动端弹窗全屏滚动展示
const isMobile = ref(false)
const dialogVisible = ref(false)
const selectedDate = ref('')
const activeStudent = ref<Student>('a')
// 每位同学各自当前选中的时段标签
const activeTabByStudent = reactive<Record<Student, Period>>(
  Object.fromEntries(
    STUDENT_ORDER.map((s) => [s, 'morning' as Period])
  ) as Record<Student, Period>
)
const loading = ref(false)
const previewVisible = ref(false)
const previewImages = ref<string[]>([])
const previewIndex = ref(0)

// 当天的发布内容（只读）
const dayPosts = ref<PostView[]>([])

// 按同学分组（只保留有内容的同学），各组内时段按固定顺序
const studentGroups = computed(() =>
  studentOrder
    .map((student) => ({
      student,
      posts: dayPosts.value
        .filter((p) => p.student === student)
        .sort(
          (a, b) => periodOrder.indexOf(a.period) - periodOrder.indexOf(b.period)
        )
    }))
    .filter((g) => g.posts.length > 0)
)

// 有内容的日期集合，用于在日历格子上打点
const markedDays = ref<Set<string>>(new Set())

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
    ElMessage.success(`${label}已复制`)
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

const savePreviewImage = async () => {
  const url = previewImages.value[previewIndex.value]
  if (!url) return
  const filename = `${selectedDate.value}_${previewIndex.value + 1}.${extFromImageUrl(url)}`
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
})

const monthKey = (d: Date) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`

// 加载当前月份有内容的日期，给日历打点
const loadMarkedDays = async (d: Date) => {
  try {
    const res = await api.get<any>(`/xhs-posts/month?month=${monthKey(d)}`)
    const dates: string[] = res.data?.dates || []
    markedDays.value = new Set(dates)
  } catch (error) {
    console.error('加载月份标记失败', error)
  }
}

watch(currentDate, (d) => {
  if (d) loadMarkedDays(d)
})

const updateIsMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  updateIsMobile()
  window.addEventListener('resize', updateIsMobile)
  loadMarkedDays(currentDate.value)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateIsMobile)
  if (typeof document !== 'undefined') {
    document.body.style.overflow = ''
  }
})

const handleDateClick = async (data: { day: string }) => {
  selectedDate.value = data.day
  dialogVisible.value = true
  await loadDate(data.day)
}

// 加载某日期已存在的内容（只读展示）
const loadDate = async (date: string) => {
  loading.value = true
  dayPosts.value = []
  try {
    const res = await api.get<any>(`/xhs-posts?date=${date}`)
    const list = Array.isArray(res.data) ? res.data : []
    dayPosts.value = list.map((item: any): PostView => ({
      id: item.id,
      student: (item.student || 'a') as Student,
      period: item.period,
      title: item.title || '',
      images: item.images || [],
      content: item.content || '',
      products: Array.isArray(item.products) ? item.products : []
    }))

    // 默认选中第一个有内容的同学，及其第一个有内容的时段
    const groups = studentGroups.value
    if (groups.length > 0) {
      activeStudent.value = groups[0].student
      for (const g of groups) {
        activeTabByStudent[g.student] = g.posts[0].period
      }
    }
  } catch (error) {
    console.error('加载内容失败', error)
    ElMessage.error('加载内容失败')
  } finally {
    loading.value = false
  }
}

useSEO({
  title: '发小红书日历',
  description: '查看小红书发布日历安排，按 号1 / 号2 / 号3 / 号4 分别展示各自早上、中午、傍晚、晚上四个时段的发布内容。'
})
</script>

<style scoped>
.calendar-page {
  animation: fadeIn 0.5s ease-in;
}

.page-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 3px solid #667eea;
}

.calendar-wrapper {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.calendar-loading {
  text-align: center;
  padding: 4rem;
  color: #999;
  font-size: 1.2rem;
}

.cell-content {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  cursor: pointer;
}

.cell-day {
  font-size: 1.1rem;
  font-weight: 500;
}

.cell-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff2442; /* 小红书红 */
}

/* 放大日历组件 */
:deep(.el-calendar) {
  --el-calendar-cell-width: 120px;
}

:deep(.el-calendar__header) {
  padding: 16px 0;
}

:deep(.el-calendar__title) {
  font-size: 1.6rem;
  font-weight: 600;
  color: #333;
}

:deep(.el-calendar-table thead th) {
  font-size: 1.05rem;
  padding: 14px 0;
  color: #667eea;
}

:deep(.el-calendar-table .el-calendar-day) {
  height: 100px;
  padding: 10px;
  transition: background 0.2s;
}

:deep(.el-calendar-table .el-calendar-day:hover) {
  background: #f0f2ff;
}

:deep(.el-calendar-table td.is-selected .el-calendar-day) {
  background: #e6e9ff;
}

/* 弹窗只读展示 */
.dialog-loading,
.dialog-empty {
  text-align: center;
  padding: 2.5rem 0;
  color: #999;
  font-size: 1.05rem;
}

.post-view {
  padding: 0.5rem 0.25rem;
}

/* 最佳发布时间提示条 */
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
  align-items: center;
  justify-content: center;
  padding: 56px 12px 24px;
  touch-action: manipulation;
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
}

.period-tabs :deep(.el-tabs__item) {
  font-size: 1.05rem;
  padding: 0 1.5rem;
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
  .page-title {
    font-size: 1.6rem;
    margin-bottom: 1rem;
  }

  .calendar-wrapper {
    padding: 0.75rem;
    border-radius: 8px;
  }

  :deep(.el-calendar__title) {
    font-size: 1.1rem;
  }

  /* 移动端隐藏“上个月/下个月”按钮，只保留“今天”，避免按钮组溢出换行 */
  :deep(.el-calendar__button-group .el-button-group > button:not(:nth-child(2))) {
    display: none;
  }

  :deep(.el-calendar-table thead th) {
    font-size: 0.8rem;
    padding: 8px 0;
  }

  /* 缩小单元格高度，避免一屏放不下 */
  :deep(.el-calendar-table .el-calendar-day) {
    height: 52px;
    padding: 4px;
  }

  .cell-day {
    font-size: 0.85rem;
  }

  .cell-content {
    justify-content: center;
  }

  .cell-dot {
    top: 2px;
    right: 2px;
    width: 6px;
    height: 6px;
  }

  /* 移动端：弹窗全屏 + 整屏滚动展示 */
  :deep(.post-dialog.el-dialog.is-fullscreen) {
    display: flex;
    flex-direction: column;
    border-radius: 0;
  }

  /* 头部固定在顶部，不随内容滚动 */
  :deep(.post-dialog.is-fullscreen .el-dialog__header) {
    flex: 0 0 auto;
    margin: 0;
    padding: 14px 16px;
    border-bottom: 1px solid #eef0f7;
    position: sticky;
    top: 0;
    background: #fff;
    z-index: 2;
  }

  :deep(.post-dialog.is-fullscreen .el-dialog__title) {
    font-size: 1.05rem;
    font-weight: 600;
  }

  /* body 占满剩余高度并纵向滚动 */
  :deep(.post-dialog.is-fullscreen .el-dialog__body) {
    flex: 1 1 auto;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    padding: 12px 16px calc(16px + env(safe-area-inset-bottom, 0px));
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

  .period-tabs :deep(.el-tabs__item) {
    font-size: 0.95rem;
    padding: 0 0.9rem;
  }

  /* 同学 / 时段 tab 在窄屏可横向滚动，避免溢出换行 */
  .student-tabs > :deep(.el-tabs__header .el-tabs__nav-wrap),
  .period-tabs :deep(.el-tabs__nav-wrap) {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .student-tabs > :deep(.el-tabs__header .el-tabs__nav),
  .period-tabs :deep(.el-tabs__nav) {
    white-space: nowrap;
  }
}

@media (max-width: 380px) {
  :deep(.el-calendar-table .el-calendar-day) {
    height: 44px;
  }

  .period-tabs :deep(.el-tabs__item) {
    padding: 0 0.6rem;
  }
}
</style>
