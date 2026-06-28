<template>
  <div class="pwd-admin">
    <el-card shadow="never">
      <template #header>
        <span>修改提交密码</span>
      </template>

      <el-alert
        title="说明"
        type="info"
        description="此密码用于前台「添加发布安排」页面（/xhs-schedule）免登录提交。修改后立即生效，请妥善保管并告知需要提交的人员。"
        :closable="false"
        show-icon
        class="tip-alert"
      />

      <el-form label-position="top" class="pwd-form" @submit.prevent="handleSubmit">
        <el-form-item label="新提交密码" required>
          <el-input
            v-model="newPassword"
            type="password"
            placeholder="至少 4 位"
            show-password
            maxlength="64"
          />
        </el-form-item>

        <el-form-item label="确认新密码" required>
          <el-input
            v-model="confirmPassword"
            type="password"
            placeholder="再次输入新密码"
            show-password
            maxlength="64"
          />
        </el-form-item>

        <div class="form-actions">
          <el-button type="primary" :loading="saving" @click="handleSubmit">
            更新提交密码
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { changeXhsSubmitPassword } from '~/utils/xhsPostsApi'

definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const newPassword = ref('')
const confirmPassword = ref('')
const saving = ref(false)

const handleSubmit = async () => {
  if (newPassword.value.length < 4) {
    ElMessage.warning('新提交密码至少 4 位')
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  saving.value = true
  try {
    const res = await changeXhsSubmitPassword(newPassword.value)
    if (res.code === 200) {
      newPassword.value = ''
      confirmPassword.value = ''
      ElMessage.success('提交密码已更新')
    } else {
      ElMessage.error(res.msg || '更新失败')
    }
  } catch (error: any) {
    ElMessage.error(error.data?.msg || '更新失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.pwd-admin {
  max-width: 520px;
}

.tip-alert {
  margin-bottom: 1.25rem;
}

.pwd-form {
  margin-top: 0.5rem;
}

.form-actions {
  margin-top: 0.5rem;
}
</style>
