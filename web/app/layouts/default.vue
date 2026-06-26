<template>
  <div class="layout-container">
    <header class="header" role="banner">
      <div class="header-content">
        <NuxtLink to="/" class="logo-link">
          <h1 class="logo">行书子</h1>
        </NuxtLink>
        <NuxtLink to="/xiaohongshu-calendar" class="calendar-link">发小红书日历</NuxtLink>
        <nav class="nav" role="navigation" aria-label="主导航">
          <NuxtLink to="/" class="nav-link">首页</NuxtLink>
          <NuxtLink to="/programming-course" class="nav-link">编程课程</NuxtLink>
          <NuxtLink to="/music-course" class="nav-link">音乐课程</NuxtLink>
          <NuxtLink to="/music-album" class="nav-link">音乐专辑</NuxtLink>
          <NuxtLink to="/books" class="nav-link">各类书籍</NuxtLink>
          <NuxtLink to="/agricultural-product" class="nav-link">助农产品</NuxtLink>
          
          <!-- 管理员入口 -->
          <ClientOnly>
            <NuxtLink v-if="isAdmin" to="/admin" class="nav-link admin-link">
              后台管理
            </NuxtLink>
            <template #fallback>
              <!-- SSR 占位 -->
            </template>
          </ClientOnly>
          
          <!-- 用户状态 -->
          <ClientOnly>
            <div class="user-section">
              <NuxtLink v-if="!isLoggedIn" to="/login" class="nav-link login-btn">
                登录
              </NuxtLink>
              <div v-else class="user-menu">
                <span class="user-name">{{ user?.username }}</span>
                <button @click="handleLogout" class="logout-btn">退出</button>
              </div>
            </div>
            <template #fallback>
              <div class="user-section">
                <NuxtLink to="/login" class="nav-link login-btn">
                  登录
                </NuxtLink>
              </div>
            </template>
          </ClientOnly>
        </nav>
      </div>
    </header>
    
    <main class="main-content" role="main">
      <slot />
    </main>
    
    <footer class="footer" role="contentinfo">
      <div class="footer-content">
        <p>&copy; 2025 行书子. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const { user, isLoggedIn, isAdmin, logout } = useAuth()

const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    logout()
  }
}
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-link {
  text-decoration: none;
  color: white;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
}

.calendar-link {
  color: white;
  text-decoration: none;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.4rem 1rem;
  border-radius: 6px;
  margin-right: auto;
  margin-left: 1.5rem;
  white-space: nowrap;
  transition: background 0.3s;
}

.calendar-link:hover {
  background: rgba(255, 255, 255, 0.3);
}

@media (max-width: 768px) {
  .header-content {
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0 1rem;
  }

  .calendar-link {
    margin-left: 0;
    margin-right: 0;
    padding: 0.35rem 0.8rem;
    font-size: 0.9rem;
  }

  .nav {
    gap: 0.8rem 1rem;
    width: 100%;
  }

  .user-section {
    margin-left: 0;
  }
}

.nav {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s;
}

.nav-link:hover {
  opacity: 0.8;
}

.nav-link.router-link-active {
  border-bottom: 2px solid white;
}

.admin-link {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  margin-left: 0.5rem;
}

.admin-link:hover {
  background: rgba(255, 255, 255, 0.3);
}

.user-section {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.login-btn {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1.5rem;
  border-radius: 6px;
}

.login-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  color: white;
  font-weight: 500;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.3s;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
}

.footer {
  background-color: #f5f5f5;
  padding: 2rem 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
  color: #666;
}
</style>


