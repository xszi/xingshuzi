<template>
  <div class="xhs-admin">
    <el-card shadow="never" class="tip-card">
      <el-alert
        title="发小红书内容管理"
        type="info"
        description="选择周一至周日中的一天，为「号1 / 号2 / 号3 / 号4」编辑各自「早上 / 中午 / 傍晚 / 晚上」四个时段的发布内容。所有字段均为选填，填多少保存多少即可。红点表示该天已安排内容。"
        :closable="false"
        show-icon
      />
    </el-card>

    <div class="week-wrapper">
      <XhsWeekdayPicker
        :selected-weekday="selectedWeekday"
        :marked-weekdays="markedWeekdays"
        @select="handleWeekdaySelect"
      />
    </div>

    <div class="edit-panel">
      <h3 class="panel-title">{{ weekdayTitle }} 发布安排</h3>

      <div v-if="pageLoading" class="panel-loading">加载中...</div>

      <el-tabs v-else v-model="activeStudent" type="card" class="student-tabs">
        <el-tab-pane
          v-for="stu in studentTabs"
          :key="stu.name"
          :name="stu.name"
        >
          <template #label>
            <span>
              {{ stu.label }}
              <el-badge v-if="studentHasContent(stu.name)" is-dot type="danger" />
            </span>
          </template>

          <el-tabs v-model="activeTab" class="period-tabs">
            <el-tab-pane
              v-for="tab in periodTabs"
              :key="tab.name"
              :name="tab.name"
            >
              <template #label>
                <span class="period-tab-label">
                  <span class="period-name">{{ tab.label }}</span>
                  <span class="period-time">{{ tab.time }}</span>
                  <el-badge v-if="forms[stu.name][tab.name].id" is-dot type="danger" />
                </span>
              </template>

              <div class="post-form">
                <div class="best-time-tip">
                  🕐 最佳发布时间：{{ tab.label }} {{ tab.time }}
                </div>

                <div class="form-row">
                  <div class="form-item">
                    <label>大字报文字</label>
                    <el-input
                      v-model="forms[stu.name][tab.name].posterText"
                      type="textarea"
                      :autosize="{ minRows: 2, maxRows: 4 }"
                      placeholder="配图醒目短句，可换行"
                      maxlength="50"
                      show-word-limit
                      class="wrap-input"
                    />
                  </div>

                  <div class="form-item">
                    <label>标题</label>
                    <el-input
                      v-model="forms[stu.name][tab.name].title"
                      type="textarea"
                      :autosize="{ minRows: 2, maxRows: 4 }"
                      placeholder="请输入标题，可换行"
                      maxlength="50"
                      show-word-limit
                      class="wrap-input"
                    />
                  </div>
                </div>

                <div class="form-row form-row--media">
                  <div class="form-item">
                    <label>配图（可多选，按选择顺序上传）</label>
                    <XhsImageUploader
                      v-model="forms[stu.name][tab.name].images"
                      :uploading="uploadingKey === `${stu.name}:${tab.name}`"
                      :before-upload="beforeUpload"
                      :http-request="(opt: any) => doUpload(stu.name, tab.name, opt)"
                    />
                  </div>

                  <div class="form-item">
                    <label>所挂商品（选填，可多选）</label>
                    <el-select
                      v-model="forms[stu.name][tab.name].products"
                      multiple
                      placeholder="请选择所挂商品"
                      class="product-select"
                    >
                      <el-option
                        v-for="opt in productOptions"
                        :key="opt"
                        :label="opt"
                        :value="opt"
                      />
                    </el-select>
                  </div>
                </div>

                <div class="form-item">
                  <label>文案</label>
                  <el-input
                    v-model="forms[stu.name][tab.name].content"
                    type="textarea"
                    :autosize="{ minRows: 6, maxRows: 14 }"
                    placeholder="请输入文案内容（支持换行）"
                    maxlength="1000"
                    show-word-limit
                    class="wrap-input"
                  />
                </div>

                <div class="form-actions">
                  <el-button
                    v-if="forms[stu.name][tab.name].id"
                    type="danger"
                    plain
                    :loading="deleting"
                    @click="handleDelete(stu.name, tab.name)"
                  >
                    删除
                  </el-button>
                  <el-button
                    type="primary"
                    :loading="saving"
                    @click="handleSave(stu.name, tab.name)"
                  >
                    保存{{ stu.label }}·{{ tab.label }}内容
                  </el-button>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  type Student,
  STUDENT_TABS,
  STUDENT_ORDER
} from '~/data/xhsStudents'
import { type Weekday, weekdayLabel } from '~/utils/xhsWeekday'
import {
  fetchXhsPostsByWeekday,
  hasXhsPostsForWeekday,
  saveXhsPost
} from '~/utils/xhsPostsApi'

definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

useHead({
  title: '内容管理'
})

type Period = 'morning' | 'noon' | 'evening' | 'night' | 'late_night'

interface PostForm {
  id: number | null
  posterText: string
  title: string
  images: string[]
  content: string
  products: string[]
}

// 所挂商品可选项（与后端 PRODUCTS 一致）
const productOptions = ['考研', '雅思', '六级', '四级', '小学语法学习纸']

// 各时段最佳发布时间
const periodTabs: { name: Period; label: string; time: string }[] = [
  { name: 'morning', label: '早上', time: '7:30-8:30' },
  { name: 'noon', label: '中午', time: '11:30-12:30' },
  { name: 'evening', label: '初晚', time: '19:30-21:00' },
  { name: 'night', label: '中晚', time: '21:30-22:30' },
  { name: 'late_night', label: '深晚', time: '22:30-23:30' }
]

const studentTabs = STUDENT_TABS

const {
  selectedWeekday,
  markedWeekdays,
  loadMarkedWeekdays
} = useXhsWeekday()

const weekdayTitle = computed(() => weekdayLabel(selectedWeekday.value))

const activeStudent = ref<Student>('a')
const activeTab = ref<Period>('morning')
const saving = ref(false)
const deleting = ref(false)
const pageLoading = ref(false)
// 正在上传图片的「账号:时段」键（用于显示 loading），形如 "a:morning"
const uploadingKey = ref<string | null>(null)
// 同一账号时段内按选择顺序串行上传
const uploadQueues = new Map<string, Promise<void>>()

const emptyForm = (): PostForm => ({
  id: null,
  posterText: '',
  title: '',
  images: [],
  content: '',
  products: []
})

// 每位同学一份「各时段」表单数据
const emptyStudentForms = (): Record<Period, PostForm> => ({
  morning: emptyForm(),
  noon: emptyForm(),
  evening: emptyForm(),
  night: emptyForm(),
  late_night: emptyForm()
})

const forms = reactive<Record<Student, Record<Period, PostForm>>>(
  Object.fromEntries(
    STUDENT_ORDER.map((s) => [s, emptyStudentForms()])
  ) as Record<Student, Record<Period, PostForm>>
)

// 某位同学是否已安排任意时段内容（用于外层标签红点）
const studentHasContent = (student: Student) =>
  periodTabs.some((p) => forms[student][p.name].id)

// 上传前校验：类型 + 大小
const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  const within10M = file.size / 1024 / 1024 < 10
  if (!within10M) {
    ElMessage.error('图片大小不能超过 10MB')
    return false
  }
  return true
}

// 自定义上传：按选择顺序串行调用后端 /xhs-posts/upload
const doUpload = (student: Student, period: Period, option: any) => {
  const key = `${student}:${period}`
  uploadingKey.value = key

  const task = async () => {
    try {
      const res = await api.upload<any>('/xhs-posts/upload', option.file)
      if (res.code === 200 && res.data?.url) {
        forms[student][period].images.push(res.data.url)
        option.onSuccess?.(res)
      } else {
        ElMessage.error(res.msg || '上传失败')
        option.onError?.(new Error(res.msg || '上传失败'))
      }
    } catch (error: any) {
      console.error('上传失败', error)
      ElMessage.error(error.data?.msg || '上传失败，请确认已登录管理员账号')
      option.onError?.(error)
    }
  }

  const prev = uploadQueues.get(key) || Promise.resolve()
  const next = prev
    .then(task)
    .catch(() => {})
    .finally(() => {
      if (uploadQueues.get(key) === next) {
        uploadQueues.delete(key)
        if (uploadingKey.value === key) uploadingKey.value = null
      }
    })
  uploadQueues.set(key, next)
  return next
}

const resetForms = () => {
  for (const stu of studentTabs) {
    for (const p of periodTabs) {
      Object.assign(forms[stu.name][p.name], emptyForm())
    }
  }
}

onMounted(() => {
  loadMarkedWeekdays()
})

const applyPostToForm = (
  student: Student,
  period: Period,
  item: any
) => {
  const rawProducts = Array.isArray(item.products) ? item.products : []
  forms[student][period] = {
    id: item.id,
    posterText: item.poster_text || '',
    title: item.title || '',
    images: Array.isArray(item.images) ? [...item.images] : [],
    content: item.content || '',
    products: rawProducts.filter((x: string) => productOptions.includes(x))
  }
}

const handleWeekdaySelect = (weekday: Weekday) => {
  selectedWeekday.value = weekday
}

// 加载某星期已存在的内容（含全部同学的四时段），填入对应表单
const loadWeekday = async (weekday: Weekday) => {
  try {
    const list = await fetchXhsPostsByWeekday(weekday)
    for (const item of list) {
      const stu = (item.student || 'a') as Student
      const p = item.period as Period
      if (forms[stu]?.[p]) {
        applyPostToForm(stu, p, item)
      } else if (STUDENT_ORDER.includes(stu)) {
        console.warn('未知时段标识:', p, item)
      }
    }
  } catch (error: any) {
    console.error('加载内容失败', error)
    const msg = error?.data?.msg || error?.message
    ElMessage.error(msg ? `加载失败：${msg}` : '加载内容失败，请确认后端已更新并重启')
  }
}

watch(selectedWeekday, async (weekday) => {
  activeStudent.value = 'a'
  activeTab.value = 'morning'
  resetForms()
  pageLoading.value = true
  try {
    await loadWeekday(weekday)
  } finally {
    pageLoading.value = false
  }
}, { immediate: true })

const handleSave = async (student: Student, period: Period) => {
  const form = forms[student][period]
  saving.value = true
  try {
    const res = await saveXhsPost({
      weekday: selectedWeekday.value,
      student,
      period,
      poster_text: form.posterText,
      title: form.title,
      images: form.images,
      content: form.content,
      products: form.products
    })
    form.id = res.data?.id ?? form.id
    markedWeekdays.value.add(selectedWeekday.value)
    ElMessage.success('编辑保存成功')
  } catch (error: any) {
    console.error('保存失败', error)
    ElMessage.error(error.data?.msg || '保存失败，请确认已登录管理员账号')
  } finally {
    saving.value = false
  }
}

const handleDelete = async (student: Student, period: Period) => {
  const form = forms[student][period]
  if (!form.id) return

  try {
    await ElMessageBox.confirm('确定删除该时段的发布内容吗？', '提示', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消'
    })
  } catch {
    return // 用户取消
  }

  deleting.value = true
  try {
    const res = await api.delete<any>(`/xhs-posts/${form.id}`)
    if (res.code === 200) {
      Object.assign(form, emptyForm())
      ElMessage.success('删除成功')
      // 若该日已无任何内容，去掉星期标记点
      await refreshWeekdayMark(selectedWeekday.value)
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error: any) {
    console.error('删除失败', error)
    ElMessage.error(error.data?.msg || '删除失败')
  } finally {
    deleting.value = false
  }
}

// 删除后重新判断该日是否还有内容，更新星期标记
const refreshWeekdayMark = async (weekday: Weekday) => {
  try {
    const hasContent = await hasXhsPostsForWeekday(weekday)
    if (hasContent) {
      markedWeekdays.value.add(weekday)
    } else {
      markedWeekdays.value.delete(weekday)
    }
  } catch (error) {
    console.error('刷新星期标记失败', error)
  }
}
</script>

<style scoped>
.xhs-admin {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.calendar-wrapper,
.week-wrapper,
.edit-panel {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.edit-panel {
  padding: 1.5rem 2rem 2rem;
}

.panel-title {
  margin: 0 0 1.25rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #eef0f7;
}

.panel-loading {
  text-align: center;
  padding: 3rem 0;
  color: #999;
  font-size: 1rem;
}

/* 时段标签：名称 + 最佳时间 */
.period-tab-label {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}

.period-name {
  font-weight: 500;
}

.period-time {
  font-size: 0.75rem;
  color: #909399;
}

/* 弹窗表单 */
.post-form {
  padding: 0.25rem 0;
}

/* 多行输入：允许换行、自动增高 */
.wrap-input :deep(.el-textarea__inner) {
  line-height: 1.55;
  word-break: break-word;
  white-space: pre-wrap;
  resize: vertical;
  min-height: 52px;
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

.form-item {
  margin-bottom: 1.1rem;
  min-width: 0;
}

/* 并排表单项：桌面两列，移动端自动折行 */
.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 1rem;
  margin-bottom: 1.1rem;
}

.form-row .form-item {
  margin-bottom: 0;
}

.form-row--3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

/* 配图 + 所挂商品：左宽右窄 */
.form-row--media {
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
  align-items: start;
}

.product-select {
  width: 100%;
}

.form-item--full {
  grid-column: 1 / -1;
}

.form-item label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-actions {
  text-align: right;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #eef0f7;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  position: sticky;
  bottom: 0;
  background: #fff;
  z-index: 1;
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

@media (max-width: 768px) {
  .form-row,
  .form-row--3,
  .form-row--media {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .form-row .form-item + .form-item {
    margin-top: 1.1rem;
  }

  .edit-panel {
    padding: 0.75rem;
  }
}
</style>
