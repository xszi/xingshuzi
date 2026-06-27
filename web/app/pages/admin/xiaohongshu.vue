<template>
  <div class="xhs-admin">
    <el-card shadow="never" class="tip-card">
      <el-alert
        title="发小红书内容管理"
        type="info"
        description="点击日历中的某一天，可分别为「号1 / 号2 / 号3 / 号4」编辑各自「早上 / 中午 / 傍晚 / 晚上」四个时段的发布内容。红点表示该天已安排内容。"
        :closable="false"
        show-icon
      />
    </el-card>

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

    <!-- 日期详情弹窗 -->
    <ClientOnly>
      <el-dialog
        v-model="dialogVisible"
        :title="`${selectedDate} 发布安排`"
        width="680px"
        align-center
      >
        <el-tabs v-model="activeStudent" type="card" class="student-tabs">
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

                  <div class="form-item">
                    <label>标题</label>
                    <el-input
                      v-model="forms[stu.name][tab.name].title"
                      placeholder="请输入标题"
                      maxlength="50"
                      show-word-limit
                    />
                  </div>

                  <div class="form-item">
                    <label>配图（可多选，按选择顺序上传）</label>
                    <div class="image-uploader">
                      <div
                        v-for="(img, i) in forms[stu.name][tab.name].images"
                        :key="img + i"
                        class="uploaded-thumb"
                      >
                        <span class="thumb-order">{{ i + 1 }}</span>
                        <img :src="img" class="thumb-img" @error="onImgError" />
                        <div class="thumb-mask" @click="removeImage(stu.name, tab.name, i)">
                          <span class="thumb-remove">删除</span>
                        </div>
                      </div>

                      <el-upload
                        multiple
                        :show-file-list="false"
                        :before-upload="beforeUpload"
                        :http-request="(opt: any) => doUpload(stu.name, tab.name, opt)"
                        accept="image/*"
                        class="upload-trigger"
                      >
                        <div class="upload-box">
                          <span
                            v-if="uploadingKey === `${stu.name}:${tab.name}`"
                            class="upload-loading"
                          >上传中...</span>
                          <span v-else class="upload-plus">＋</span>
                        </div>
                      </el-upload>
                    </div>
                    <p class="upload-hint">支持 jpg / png / gif / webp，可多选，单张不超过 10MB，按选择顺序依次上传</p>
                  </div>

                  <div class="form-item">
                    <label>文案</label>
                    <el-input
                      v-model="forms[stu.name][tab.name].content"
                      type="textarea"
                      :rows="5"
                      placeholder="请输入文案内容"
                      maxlength="1000"
                      show-word-limit
                    />
                  </div>

                  <div class="form-item">
                    <label>所挂商品（选填，可多选）</label>
                    <el-select
                      v-model="forms[stu.name][tab.name].products"
                      multiple
                      placeholder="请选择所挂商品"
                      style="width: 100%"
                    >
                      <el-option
                        v-for="opt in productOptions"
                        :key="opt"
                        :label="opt"
                        :value="opt"
                      />
                    </el-select>
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
      </el-dialog>
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  type Student,
  STUDENT_TABS,
  STUDENT_ORDER
} from '~/data/xhsStudents'

definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

type Period = 'morning' | 'noon' | 'evening' | 'night'

interface PostForm {
  id: number | null
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
  { name: 'evening', label: '傍晚', time: '18:30-19:30' },
  { name: 'night', label: '晚上', time: '21:00-22:00' }
]

const studentTabs = STUDENT_TABS

const currentDate = ref(new Date())
const dialogVisible = ref(false)
const selectedDate = ref('')
const activeStudent = ref<Student>('a')
const activeTab = ref<Period>('morning')
const saving = ref(false)
const deleting = ref(false)
// 正在上传图片的「账号:时段」键（用于显示 loading），形如 "a:morning"
const uploadingKey = ref<string | null>(null)
// 同一账号时段内按选择顺序串行上传
const uploadQueues = new Map<string, Promise<void>>()

// 有内容的日期集合，用于在日历格子上打点
const markedDays = ref<Set<string>>(new Set())

const emptyForm = (): PostForm => ({
  id: null,
  title: '',
  images: [],
  content: '',
  products: []
})

// 每位同学一份「四时段」表单数据
const emptyStudentForms = (): Record<Period, PostForm> => ({
  morning: emptyForm(),
  noon: emptyForm(),
  evening: emptyForm(),
  night: emptyForm()
})

const forms = reactive<Record<Student, Record<Period, PostForm>>>(
  Object.fromEntries(
    STUDENT_ORDER.map((s) => [s, emptyStudentForms()])
  ) as Record<Student, Record<Period, PostForm>>
)

// 某位同学是否已安排任意时段内容（用于外层标签红点）
const studentHasContent = (student: Student) =>
  periodTabs.some((p) => forms[student][p.name].id)

const onImgError = (e: Event) => {
  ;(e.target as HTMLImageElement).style.display = 'none'
}

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

// 移除某张已上传的配图
const removeImage = (student: Student, period: Period, index: number) => {
  forms[student][period].images.splice(index, 1)
}

const resetForms = () => {
  for (const stu of studentTabs) {
    for (const p of periodTabs) {
      Object.assign(forms[stu.name][p.name], emptyForm())
    }
  }
}

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

// 切换月份时刷新标记点
watch(currentDate, (d) => {
  if (d) loadMarkedDays(d)
})

onMounted(() => {
  loadMarkedDays(currentDate.value)
})

const handleDateClick = async (data: { day: string }) => {
  selectedDate.value = data.day
  activeStudent.value = 'a'
  activeTab.value = 'morning'
  resetForms()
  dialogVisible.value = true
  await loadDate(data.day)
}

// 加载某日期已存在的内容（含全部同学的四时段），填入对应表单
const loadDate = async (date: string) => {
  try {
    const res = await api.get<any>(`/xhs-posts?date=${date}`)
    const list = Array.isArray(res.data) ? res.data : []
    for (const item of list) {
      const stu = (item.student || 'a') as Student
      const p = item.period as Period
      if (forms[stu] && forms[stu][p]) {
        forms[stu][p].id = item.id
        forms[stu][p].title = item.title || ''
        forms[stu][p].images = Array.isArray(item.images) ? item.images : []
        forms[stu][p].content = item.content || ''
        // 只保留预设选项内的商品；旧的自由文本值不在选项里则显示为未选
        const rawProducts = Array.isArray(item.products) ? item.products : []
        forms[stu][p].products = rawProducts.filter((x: string) =>
          productOptions.includes(x)
        )
      }
    }
  } catch (error) {
    console.error('加载内容失败', error)
    ElMessage.error('加载内容失败')
  }
}

const handleSave = async (student: Student, period: Period) => {
  const form = forms[student][period]
  saving.value = true
  try {
    const res = await api.post<any>('/xhs-posts', {
      date: selectedDate.value,
      student,
      period,
      title: form.title,
      images: form.images,
      content: form.content,
      products: form.products
    })
    if (res.code === 200) {
      form.id = res.data?.id ?? form.id
      markedDays.value.add(selectedDate.value)
      ElMessage.success('保存成功')
    } else {
      ElMessage.error(res.msg || '保存失败')
    }
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
      // 若该天已无任何内容，去掉日历标记点
      await refreshDayMark(selectedDate.value)
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

// 删除后重新判断该天是否还有内容，更新日历标记
const refreshDayMark = async (date: string) => {
  try {
    const res = await api.get<any>(`/xhs-posts?date=${date}`)
    const list = Array.isArray(res.data) ? res.data : []
    if (list.length === 0) {
      markedDays.value.delete(date)
    } else {
      markedDays.value.add(date)
    }
  } catch (error) {
    console.error('刷新日历标记失败', error)
  }
}
</script>

<style scoped>
.xhs-admin {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.calendar-wrapper {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
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
  font-size: 1.05rem;
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

:deep(.el-calendar__title) {
  font-size: 1.4rem;
  font-weight: 600;
  color: #333;
}

:deep(.el-calendar-table thead th) {
  font-size: 1rem;
  padding: 12px 0;
  color: #667eea;
}

:deep(.el-calendar-table .el-calendar-day) {
  height: 90px;
  padding: 8px;
  transition: background 0.2s;
}

:deep(.el-calendar-table .el-calendar-day:hover) {
  background: #f0f2ff;
}

:deep(.el-calendar-table td.is-selected .el-calendar-day) {
  background: #e6e9ff;
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

.form-item {
  margin-bottom: 1.25rem;
}

.form-item label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.image-uploader {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.uploaded-thumb {
  position: relative;
  width: 90px;
  height: 90px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #eee;
}

.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.thumb-order {
  position: absolute;
  top: 4px;
  left: 4px;
  z-index: 1;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  border-radius: 9px;
  background: rgba(102, 126, 234, 0.92);
  color: #fff;
  font-size: 0.7rem;
  line-height: 18px;
  text-align: center;
}

.thumb-mask {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
  cursor: pointer;
}

.uploaded-thumb:hover .thumb-mask {
  opacity: 1;
}

.thumb-remove {
  color: #fff;
  font-size: 0.85rem;
}

.upload-trigger :deep(.el-upload) {
  display: block;
}

.upload-box {
  width: 90px;
  height: 90px;
  border: 1px dashed #c0c4cc;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.2s;
  background: #fafafa;
}

.upload-box:hover {
  border-color: #667eea;
}

.upload-plus {
  font-size: 1.8rem;
  color: #c0c4cc;
}

.upload-loading {
  font-size: 0.8rem;
  color: #999;
}

.upload-hint {
  margin: 0.5rem 0 0;
  font-size: 0.8rem;
  color: #999;
}

.form-actions {
  text-align: right;
  margin-top: 0.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
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
</style>
