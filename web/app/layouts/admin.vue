<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <h2>后台管理</h2>
      </div>
      <nav class="sidebar-nav">
        <NuxtLink to="/admin" class="sidebar-link">
          <span class="icon">🏠</span>
          <span>首页</span>
        </NuxtLink>
        <NuxtLink to="/admin/programming-courses" class="sidebar-link">
          <span class="icon">💻</span>
          <span>编程课程</span>
        </NuxtLink>
        <NuxtLink to="/admin/music-courses" class="sidebar-link">
          <span class="icon">🎵</span>
          <span>音乐课程</span>
        </NuxtLink>
        <NuxtLink to="/admin/music-albums" class="sidebar-link">
          <span class="icon">🎶</span>
          <span>音乐专辑</span>
        </NuxtLink>
        <NuxtLink to="/admin/books" class="sidebar-link">
          <span class="icon">📚</span>
          <span>各类书籍</span>
        </NuxtLink>
        <NuxtLink to="/admin/agricultural-products" class="sidebar-link">
          <span class="icon">🌾</span>
          <span>助农产品</span>
        </NuxtLink>
        <NuxtLink to="/admin/xiaohongshu" class="sidebar-link">
          <span class="icon">📕</span>
          <span>发小红书</span>
        </NuxtLink>
        <div class="sidebar-divider"></div>
        <NuxtLink to="/admin/debug" class="sidebar-link">
          <span class="icon">🔧</span>
          <span>接口调试</span>
        </NuxtLink>
      </nav>
      <div class="sidebar-footer">
        <NuxtLink to="/" class="back-to-home">返回前台</NuxtLink>
      </div>
    </aside>
    
    <main class="admin-main">
      <header class="admin-header">
        <h1 class="page-title">{{ pageTitle }}</h1>
        <div class="admin-user">
          <span>{{ user?.username }}</span>
          <button @click="handleLogout" class="logout-btn">退出登录</button>
        </div>
      </header>
      
      <div class="admin-content">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const { user, logout } = useAuth()
const route = useRoute()

// 访问权限由路由中间件 middleware/admin.ts 统一校验

const pageTitle = computed(() => {
  const path = route.path
  if (path === '/admin') return '后台首页'
  if (path.includes('programming-courses')) return '编程课程管理'
  if (path.includes('music-courses')) return '音乐课程管理'
  if (path.includes('music-albums')) return '音乐专辑管理'
  if (path.includes('books')) return '书籍管理'
  if (path.includes('agricultural-products')) return '助农产品管理'
  if (path.includes('xiaohongshu')) return '发小红书内容管理'
  return '后台管理'
})

const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    logout()
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f5f5f5;
}

.admin-sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 2rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s;
}

.sidebar-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.sidebar-link.router-link-active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border-left: 3px solid #667eea;
}

.sidebar-link .icon {
  font-size: 1.2rem;
}

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.back-to-home {
  display: block;
  padding: 0.75rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: background 0.3s;
}

.back-to-home:hover {
  background: rgba(255, 255, 255, 0.2);
}

.sidebar-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0.5rem 0;
}

.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.admin-header {
  background: white;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.admin-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.admin-user span {
  color: #666;
  font-weight: 500;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.logout-btn:hover {
  background: #e0e0e0;
}

.admin-content {
  flex: 1;
  padding: 2rem;
}
</style>

