<template>
  <div class="debug-page">
    <el-page-header title="返回" @back="$router.push('/admin')">
      <template #content>
        <span class="page-title">API 接口调试工具</span>
      </template>
    </el-page-header>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>当前用户信息</span>
            </div>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="用户名">{{ userInfo.username || '未登录' }}</el-descriptions-item>
            <el-descriptions-item label="角色">
              <el-tag v-if="userInfo.role === 'admin'" type="danger">管理员</el-tag>
              <el-tag v-else-if="userInfo.role" type="info">普通用户</el-tag>
              <span v-else>-</span>
            </el-descriptions-item>
            <el-descriptions-item label="登录状态">
              <el-tag v-if="userInfo.isLoggedIn" type="success">已登录</el-tag>
              <el-tag v-else type="info">未登录</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>Token 信息</span>
            </div>
          </template>
          <el-input
            v-model="token"
            type="textarea"
            :rows="5"
            readonly
            placeholder="暂无 Token"
          />
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>测试接口调用</span>
        </div>
      </template>
      <el-space wrap>
        <el-button type="primary" @click="testAPI('/courses/admin/list?category=programming')">
          测试编程课程接口
        </el-button>
        <el-button type="primary" @click="testAPI('/courses/admin/list?category=music')">
          测试音乐课程接口
        </el-button>
        <el-button type="primary" @click="testAPI('/music/albums')">
          测试音乐专辑接口
        </el-button>
        <el-button type="primary" @click="testAPI('/books/admin/list')">
          测试书籍接口
        </el-button>
        <el-button type="primary" @click="testAPI('/products/agriculture')">
          测试助农产品接口
        </el-button>
      </el-space>
    </el-card>

    <el-card shadow="never" style="margin-top: 20px" v-loading="testResult.loading">
      <template #header>
        <div class="card-header">
          <span>测试结果</span>
        </div>
      </template>
      <el-alert
        v-if="testResult.error"
        title="请求失败"
        type="error"
        :closable="false"
        show-icon
      >
        <pre>{{ testResult.error }}</pre>
      </el-alert>
      <el-alert
        v-else-if="testResult.data"
        title="请求成功"
        type="success"
        :closable="false"
        show-icon
      >
        <pre>{{ testResult.data }}</pre>
      </el-alert>
      <el-empty v-else description="暂无测试结果" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const { user, token } = useAuth()

const userInfo = computed(() => ({
  username: user.value?.username,
  role: user.value?.role,
  isLoggedIn: !!user.value
}))

const testResult = ref({
  loading: false,
  data: null,
  error: null
})

const testAPI = async (url: string) => {
  testResult.value = { loading: true, data: null, error: null }
  
  try {
    console.log('Testing API:', url)
    const response = await api.get(url)
    console.log('Response:', response)
    testResult.value = { 
      loading: false, 
      data: response,
      error: null 
    }
  } catch (error: any) {
    console.error('Error:', error)
    testResult.value = { 
      loading: false,
      data: null,
      error: {
        status: error.status,
        statusText: error.statusText,
        message: error.data?.msg || error.message,
        data: error.data
      }
    }
  }
}
</script>

<style scoped>
.debug-page {
  max-width: 1400px;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
}

.card-header {
  font-size: 1.1rem;
  font-weight: 600;
}

pre {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
  margin: 0;
  font-size: 0.9rem;
}
</style>

