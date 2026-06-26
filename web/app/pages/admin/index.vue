<template>
  <div class="admin-home">
    <el-row :gutter="20">
      <el-col :span="8" :xs="24" :sm="12" :md="8" :lg="8">
        <el-card shadow="hover" class="stat-card programming">
          <div class="stat-content">
            <div class="stat-icon">💻</div>
            <div class="stat-info">
              <div class="stat-label">编程课程</div>
              <div class="stat-value">{{ stats.programmingCourses }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8" :xs="24" :sm="12" :md="8" :lg="8">
        <el-card shadow="hover" class="stat-card music">
          <div class="stat-content">
            <div class="stat-icon">🎵</div>
            <div class="stat-info">
              <div class="stat-label">音乐课程</div>
              <div class="stat-value">{{ stats.musicCourses }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8" :xs="24" :sm="12" :md="8" :lg="8">
        <el-card shadow="hover" class="stat-card album">
          <div class="stat-content">
            <div class="stat-icon">🎶</div>
            <div class="stat-info">
              <div class="stat-label">音乐专辑</div>
              <div class="stat-value">{{ stats.musicAlbums }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8" :xs="24" :sm="12" :md="8" :lg="8">
        <el-card shadow="hover" class="stat-card books">
          <div class="stat-content">
            <div class="stat-icon">📚</div>
            <div class="stat-info">
              <div class="stat-label">各类书籍</div>
              <div class="stat-value">{{ stats.books }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8" :xs="24" :sm="12" :md="8" :lg="8">
        <el-card shadow="hover" class="stat-card agriculture">
          <div class="stat-content">
            <div class="stat-icon">🌾</div>
            <div class="stat-info">
              <div class="stat-label">助农产品</div>
              <div class="stat-value">{{ stats.agriculturalProducts }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never" class="welcome-card">
      <template #header>
        <div class="card-header">
          <span>欢迎使用后台管理系统</span>
        </div>
      </template>
      <el-alert
        title="系统提示"
        type="info"
        description="您可以在左侧菜单中选择要管理的内容分类，进行增删改查操作。所有数据都使用 Element Plus 组件展示，提供更好的用户体验。"
        :closable="false"
        show-icon
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const stats = ref({
  programmingCourses: 0,
  musicCourses: 0,
  musicAlbums: 0,
  books: 0,
  agriculturalProducts: 0
})

// 加载统计数据
onMounted(async () => {
  try {
    // 这里可以调用后端统计接口
    // const response = await api.get('/admin/stats')
    // stats.value = response.data
  } catch (error) {
    console.error('加载统计数据失败', error)
  }
})
</script>

<style scoped>
.admin-home {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stat-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.stat-card.programming .stat-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card.music .stat-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-card.album .stat-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-card.books .stat-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-card.agriculture .stat-icon {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.welcome-card {
  margin-top: 1rem;
}

.card-header {
  font-size: 1.1rem;
  font-weight: 600;
}
</style>

