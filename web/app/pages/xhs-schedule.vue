<template>
  <div class="schedule-page">
    <div class="page-header">
      <h2 class="page-title">添加发布安排</h2>
      <NuxtLink :to="scheduleLink('/xiaohongshu-calendar')" class="back-link">
        查看发布日历
      </NuxtLink>
    </div>

    <el-card shadow="never" class="tip-card">
      <el-alert
        title="无需登录即可提交"
        type="info"
        description="填写提交密码后即可保存发布安排。同一「星期 + 号次 + 时段」仅保留一条，重复提交会更新该条记录。"
        :closable="false"
        show-icon
      />
    </el-card>

    <el-card shadow="never" class="form-card">
      <el-form label-position="top" @submit.prevent="handleSubmit">
        <el-form-item label="提交密码" required>
          <el-input
            v-model="submitPassword"
            type="password"
            placeholder="请输入提交密码"
            show-password
            class="field-full"
            @blur="rememberPassword"
          />
        </el-form-item>

        <div class="selector-row">
          <el-form-item label="周几" required>
            <el-select v-model="weekday" placeholder="选择星期" class="field-full">
              <el-option
                v-for="opt in WEEKDAY_OPTIONS"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="号几" required>
            <el-select v-model="student" placeholder="选择账号" class="field-full">
              <el-option
                v-for="opt in STUDENT_TABS"
                :key="opt.name"
                :label="opt.label"
                :value="opt.name"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="发布时间段" required>
            <el-select v-model="period" placeholder="选择时段" class="field-full">
              <el-option
                v-for="opt in PERIOD_OPTIONS"
                :key="opt.value"
                :label="`${opt.label}（${opt.time}）`"
                :value="opt.value"
              />
            </el-select>
          </el-form-item>
        </div>

        <div v-if="slotLoading" class="slot-loading">正在加载该时段已有内容...</div>

        <div v-else class="best-time-tip">
          🕐 最佳发布时间：{{ periodLabel(period) }} {{ periodTime(period) }}
          <span v-if="form.id" class="exists-tag">已有安排，提交将更新</span>
        </div>

        <div class="form-row">
          <el-form-item label="大字报文字">
            <el-input
              v-model="form.posterText"
              type="textarea"
              :autosize="{ minRows: 2, maxRows: 4 }"
              placeholder="配图醒目短句，可换行"
              maxlength="50"
              show-word-limit
            />
          </el-form-item>

          <el-form-item label="标题">
            <el-input
              v-model="form.title"
              type="textarea"
              :autosize="{ minRows: 2, maxRows: 4 }"
              placeholder="请输入标题，可换行"
              maxlength="50"
              show-word-limit
            />
          </el-form-item>
        </div>

        <el-form-item label="配图（可多选，按选择顺序上传）">
          <XhsImageUploader
            v-model="form.images"
            :uploading="uploading"
            :before-upload="beforeUpload"
            :http-request="doUpload"
          />
        </el-form-item>

        <el-form-item label="所挂商品（选填，可多选）">
          <el-select
            v-model="form.products"
            multiple
            placeholder="请选择所挂商品"
            class="field-full"
          >
            <el-option
              v-for="opt in productOptions"
              :key="opt"
              :label="opt"
              :value="opt"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="文案">
          <el-input
            v-model="form.content"
            type="textarea"
            :autosize="{ minRows: 6, maxRows: 14 }"
            placeholder="请输入文案内容（支持换行）"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>

        <div class="form-actions">
          <el-button class="action-btn" @click="resetContent" :disabled="saving">
            清空内容
          </el-button>
          <el-button
            class="action-btn action-btn--primary"
            type="primary"
            :loading="saving"
            @click="handleSubmit"
          >
            提交发布安排
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import {
  type Student,
  STUDENT_TABS
} from '~/data/xhsStudents'
import {
  type Weekday,
  WEEKDAY_OPTIONS
} from '~/utils/xhsWeekday'
import {
  type Period,
  PERIOD_OPTIONS,
  periodLabel,
  periodTime
} from '~/utils/xhsPeriods'
import {
  fetchXhsPostsByWeekday
} from '~/utils/xhsPostsApi'
import { publicApi } from '~/utils/publicApi'

definePageMeta({
  layout: 'plain'
})

// 提交页禁止聚焦放大，避免 iOS 自动缩放后出现横向滚动
useHead({
  meta: [
    {
      key: 'viewport',
      name: 'viewport',
      content: 'width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover'
    }
  ]
})

const productOptions = ['考研', '雅思', '六级', '四级', '小学语法学习纸']

const { submitPassword, rememberPassword } = useXhsSubmitPassword()

const {
  weekday,
  student,
  period,
  scheduleLink
} = useXhsScheduleFilters()

const saving = ref(false)
const slotLoading = ref(false)
const uploading = ref(false)

interface FormState {
  id: number | null
  posterText: string
  title: string
  images: string[]
  content: string
  products: string[]
}

const emptyForm = (): FormState => ({
  id: null,
  posterText: '',
  title: '',
  images: [],
  content: '',
  products: []
})

const form = reactive<FormState>(emptyForm())

const requireSubmitPassword = () => {
  if (!submitPassword.value.trim()) {
    ElMessage.warning('请先填写提交密码')
    return false
  }
  return true
}

const resetContent = () => {
  Object.assign(form, emptyForm())
}

const applyPost = (item: any) => {
  const rawProducts = Array.isArray(item.products) ? item.products : []
  Object.assign(form, {
    id: item.id,
    posterText: item.poster_text || '',
    title: item.title || '',
    images: Array.isArray(item.images) ? [...item.images] : [],
    content: item.content || '',
    products: rawProducts.filter((x: string) => productOptions.includes(x))
  })
}

const loadSlot = async () => {
  slotLoading.value = true
  resetContent()
  try {
    const list = await fetchXhsPostsByWeekday(weekday.value)
    const hit = list.find(
      (item) => item.student === student.value && item.period === period.value
    )
    if (hit) applyPost(hit)
  } catch (error: any) {
    console.error('加载失败', error)
    ElMessage.error(error?.data?.msg || '加载该时段内容失败')
  } finally {
    slotLoading.value = false
  }
}

watch([weekday, student, period], () => {
  loadSlot()
}, { immediate: true })

const beforeUpload = (file: File) => {
  if (!requireSubmitPassword()) return false
  if (!file.type.startsWith('image/')) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (file.size / 1024 / 1024 >= 10) {
    ElMessage.error('图片大小不能超过 10MB')
    return false
  }
  return true
}

const doUpload = async (option: any) => {
  if (!requireSubmitPassword()) {
    option.onError?.(new Error('缺少提交密码'))
    return
  }
  uploading.value = true
  rememberPassword()
  try {
    const res = await publicApi.upload<any>(
      '/xhs-posts/upload',
      option.file,
      { submit_password: submitPassword.value }
    )
    if (res.code === 200 && res.data?.url) {
      form.images.push(res.data.url)
      option.onSuccess?.(res)
    } else {
      ElMessage.error(res.msg || '上传失败')
      option.onError?.(new Error(res.msg || '上传失败'))
    }
  } catch (error: any) {
    console.error('上传失败', error)
    ElMessage.error(error.data?.msg || '上传失败，请检查提交密码')
    option.onError?.(error)
  } finally {
    uploading.value = false
  }
}

const handleSubmit = async () => {
  if (!requireSubmitPassword()) return
  saving.value = true
  rememberPassword()
  try {
    const body = {
      weekday: weekday.value,
      student: student.value,
      period: period.value,
      poster_text: form.posterText,
      title: form.title,
      images: form.images,
      content: form.content,
      products: form.products,
      submit_password: submitPassword.value
    }
    const res = await publicApi.post<any>('/xhs-posts', body)
    if (res.code === 200) {
      form.id = res.data?.id ?? form.id
      ElMessage.success('发布安排已保存')
    } else {
      ElMessage.error(res.msg || '提交失败')
    }
  } catch (error: any) {
    console.error('提交失败', error)
    ElMessage.error(error.data?.msg || '提交失败，请检查提交密码')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.schedule-page {
  max-width: 960px;
  width: 100%;
  margin: 0 auto;
  padding: 0.75rem 0 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-sizing: border-box;
  overflow-x: hidden;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.25rem 0;
}

.page-title {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 600;
  color: #333;
  line-height: 1.3;
}

.back-link {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
  white-space: nowrap;
  flex-shrink: 0;
}

.back-link:hover {
  text-decoration: underline;
}

.tip-card,
.form-card {
  border-radius: 12px;
  overflow: hidden;
}

.schedule-page :deep(.el-form-item__content) {
  min-width: 0;
}

.tip-card :deep(.el-card__body),
.form-card :deep(.el-card__body) {
  padding: 1rem;
}

.selector-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0 1rem;
  margin-bottom: 0.5rem;
}

.selector-row :deep(.el-form-item) {
  margin-bottom: 0.75rem;
}

.field-full {
  width: 100%;
}

.slot-loading {
  padding: 0.75rem 0 1rem;
  color: #909399;
  font-size: 0.9rem;
}

.best-time-tip {
  margin-bottom: 1rem;
  padding: 0.6rem 0.85rem;
  background: #fff0f3;
  border-left: 3px solid #ff2442;
  border-radius: 4px;
  color: #d81e06;
  font-size: 0.875rem;
  line-height: 1.5;
}

.exists-tag {
  display: inline-block;
  margin-left: 0.5rem;
  padding: 0.1rem 0.45rem;
  background: #fff;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #e6a23c;
  vertical-align: middle;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #eef0f7;
}

.action-btn {
  min-height: 40px;
}

@media (max-width: 768px) {
  .schedule-page {
    padding: 0.5rem 0 1.5rem;
    gap: 0.75rem;
  }

  .page-title {
    font-size: 1.2rem;
  }

  .tip-card :deep(.el-card__body),
  .form-card :deep(.el-card__body) {
    padding: 0.75rem;
  }

  .tip-card :deep(.el-alert__description) {
    font-size: 0.85rem;
    line-height: 1.5;
  }

  .selector-row {
    grid-template-columns: 1fr 1fr;
    gap: 0 0.5rem;
  }

  .selector-row :deep(.el-form-item:last-child) {
    grid-column: 1 / -1;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .form-row :deep(.el-form-item + .el-form-item) {
    margin-top: 0.5rem;
  }

  .exists-tag {
    display: block;
    margin-left: 0;
    margin-top: 0.35rem;
  }

  .form-actions {
    flex-direction: column-reverse;
    gap: 0.5rem;
    position: static;
    margin: 0;
    padding: 0.75rem 0 0;
    padding-bottom: calc(0.75rem + env(safe-area-inset-bottom, 0px));
    background: #fff;
    border-top: 1px solid #eef0f7;
    box-shadow: none;
    z-index: 1;
  }

  .action-btn {
    width: 100%;
    margin: 0;
  }
}
</style>
