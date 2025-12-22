<template>
  <div class="home-page">
    <div class="hero-section">
      <h2 class="hero-title">欢迎来到星数字</h2>
      <p class="hero-description">这是一个基于 Nuxt 的服务端渲染 PC 端应用</p>
    </div>
    
    <div class="features-section">
      <h3 class="section-title">特性</h3>
      <div class="features-grid">
        <div class="feature-card">
          <h4>服务端渲染 (SSR)</h4>
          <p>基于 Nuxt 的服务端渲染，提供更好的 SEO 和首屏加载性能</p>
        </div>
        <div class="feature-card">
          <h4>TypeScript 支持</h4>
          <p>完整的 TypeScript 支持，提供类型安全和更好的开发体验</p>
        </div>
        <div class="feature-card">
          <h4>现代化 UI</h4>
          <p>响应式设计，适配 PC 端，提供流畅的用户体验</p>
        </div>
      </div>
    </div>
    
    <div class="info-section">
      <h3 class="section-title">项目信息</h3>
      <div class="info-card">
        <p><strong>框架:</strong> Nuxt 4</p>
        <p><strong>渲染模式:</strong> 服务端渲染 (SSR)</p>
        <p><strong>目标平台:</strong> PC 端</p>
        <p><strong>当前时间:</strong> {{ currentTime }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 服务端和客户端都会执行
const currentTime = ref(new Date().toLocaleString('zh-CN'))

// 在客户端每秒钟更新一次时间
onMounted(() => {
  const timer = setInterval(() => {
    currentTime.value = new Date().toLocaleString('zh-CN')
  }, 1000)
  
  onUnmounted(() => {
    clearInterval(timer)
  })
})
</script>

<style scoped>
.home-page {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-section {
  text-align: center;
  padding: 4rem 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 12px;
  margin-bottom: 3rem;
}

.hero-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.hero-description {
  font-size: 1.2rem;
  color: #666;
}

.features-section,
.info-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #667eea;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.feature-card h4 {
  color: #667eea;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.info-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.info-card p {
  margin: 0.8rem 0;
  color: #333;
  font-size: 1.1rem;
}

.info-card strong {
  color: #667eea;
}
</style>

