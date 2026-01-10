<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="120px"
    >
      <el-form-item
        v-for="field in fields"
        :key="field.key"
        :label="field.label"
        :prop="field.key"
      >
        <el-input
          v-if="field.type === 'text' || !field.type"
          v-model="formData[field.key]"
          :placeholder="`请输入${field.label}`"
        />
        
        <el-input
          v-else-if="field.type === 'textarea'"
          v-model="formData[field.key]"
          type="textarea"
          :rows="4"
          :placeholder="`请输入${field.label}`"
        />
        
        <el-input-number
          v-else-if="field.type === 'number'"
          v-model="formData[field.key]"
          :placeholder="`请输入${field.label}`"
          style="width: 100%"
        />
        
        <el-input
          v-else-if="field.type === 'url'"
          v-model="formData[field.key]"
          :placeholder="`请输入${field.label}`"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ submitText || '确定' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'

const props = defineProps<{
  visible: boolean
  title: string
  fields: Array<{
    key: string
    label: string
    type?: 'text' | 'textarea' | 'number' | 'url'
    required?: boolean
  }>
  initialData?: any
  submitText?: string
}>()

const emit = defineEmits<{
  close: []
  submit: [data: Record<string, any>]
}>()

const formRef = ref<FormInstance>()
const formData = ref<Record<string, any>>({})
const submitting = ref(false)

// 控制对话框显示
const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => {
    if (!val) emit('close')
  }
})

// 构建表单验证规则
const formRules = computed<FormRules>(() => {
  const rules: FormRules = {}
  props.fields.forEach(field => {
    if (field.required !== false) {
      rules[field.key] = [
        { required: true, message: `请输入${field.label}`, trigger: 'blur' }
      ]
      if (field.type === 'url') {
        rules[field.key].push({
          type: 'url',
          message: '请输入正确的URL格式',
          trigger: 'blur'
        })
      }
    }
  })
  return rules
})

// 监听初始数据变化
watch(() => props.initialData, (newData) => {
  if (newData) {
    formData.value = { ...newData }
  } else {
    // 重置表单
    formData.value = {}
    props.fields.forEach(field => {
      formData.value[field.key] = ''
    })
  }
  // 清除验证
  nextTick(() => {
    formRef.value?.clearValidate()
  })
}, { immediate: true })

// 关闭对话框
const handleClose = () => {
  emit('close')
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      submitting.value = true
      emit('submit', formData.value)
      // 注意：提交后的 loading 状态需要在父组件中重置
      setTimeout(() => {
        submitting.value = false
      }, 1000)
    }
  })
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
