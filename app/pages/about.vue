<template>
  <div class="about-page">
    <h2 class="page-title">关于我们</h2>
    
    <div class="content-section">
      <p>这是一个使用 Nuxt 4 构建的服务端渲染 PC 端应用示例项目。</p>
      
      <h3>技术栈</h3>
      <ul class="tech-list">
        <li>Nuxt 4 - 全栈 Vue 框架</li>
        <li>Vue 3 - 渐进式 JavaScript 框架</li>
        <li>TypeScript - 类型安全的 JavaScript</li>
        <li>服务端渲染 (SSR) - 提升 SEO 和性能</li>
      </ul>
      
      <h3>项目特点</h3>
      <ul class="features-list">
        <li>✅ 服务端渲染，提升首屏加载速度</li>
        <li>✅ 完整的 TypeScript 支持</li>
        <li>✅ 现代化的 UI 设计</li>
        <li>✅ 响应式布局，适配 PC 端</li>
        <li>✅ 开发工具集成 (Nuxt DevTools)</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.about-page {
  animation: fadeIn 0.5s ease-in;
}

.page-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 3px solid #667eea;
}

.content-section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  line-height: 1.8;
}

.content-section h3 {
  color: #667eea;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.content-section p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.tech-list,
.features-list {
  color: #333;
  padding-left: 2rem;
}

.tech-list li,
.features-list li {
  margin: 0.8rem 0;
  font-size: 1.1rem;
}
</style>


