<template>
  <div class="layout-container">
    <header class="header" role="banner">
      <div class="header-content">
        <NuxtLink to="/" class="logo-link">
          <h1 class="logo">行书子</h1>
        </NuxtLink>
        <nav class="nav" role="navigation" aria-label="主导航">
          <NuxtLink to="/" class="nav-link">首页</NuxtLink>
          <NuxtLink to="/programming-course" class="nav-link">编程课程</NuxtLink>
          <NuxtLink to="/music-course" class="nav-link">音乐课程</NuxtLink>
          <NuxtLink to="/music-album" class="nav-link">音乐专辑</NuxtLink>
          <NuxtLink to="/books" class="nav-link">各类书籍</NuxtLink>
          <NuxtLink to="/agricultural-product" class="nav-link">助农产品</NuxtLink>
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

.nav {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
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


