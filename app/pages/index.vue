<template>
  <div class="home-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <h1 class="hero-title">行书子 - 资源分享平台</h1>
      <p class="hero-description">提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源</p>
    </div>

    <!-- Categories Section -->
    <div class="categories-section">
      <h2 class="section-title">资源分类</h2>
      <div class="categories-grid">
        <CategoryCard 
          v-for="category in categories" 
          :key="category.id" 
          :category="category" 
        />
      </div>
    </div>

    <!-- Featured Resources -->
    <div class="featured-section">
      <h2 class="section-title">精选推荐</h2>
      <div class="resources-grid">
        <ResourceCard 
          v-for="resource in featuredResources" 
          :key="resource.id" 
          :resource="resource" 
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { categories } from '~/data/categories'
import { sampleResources } from '~/data/resources'

// 获取精选资源（从各个分类中取前2个）
const featuredResources = computed(() => {
  const featured: any[] = []
  Object.values(sampleResources).forEach(resources => {
    featured.push(...resources.slice(0, 2))
  })
  return featured.slice(0, 6) // 最多显示6个
})

// SEO 优化
const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl || 'https://xingshuzi.com'

useSEO({
  title: '行书子 - 资源分享平台',
  description: '提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源。优质内容，值得信赖。',
  keywords: '资源分享,编程课程,音乐课程,音乐专辑,电子书,二手书,助农产品,在线学习,教育资源',
  url: siteUrl,
  structuredData: {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: '行书子',
    description: '资源分享平台，提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源',
    url: siteUrl,
    potentialAction: {
      '@type': 'SearchAction',
      target: {
        '@type': 'EntryPoint',
        urlTemplate: `${siteUrl}/search?q={search_term_string}`
      },
      'query-input': 'required name=search_term_string'
    },
    publisher: {
      '@type': 'Organization',
      name: '行书子',
      url: siteUrl
    }
  }
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
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  margin-bottom: 3rem;
  color: white;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0 0 1rem 0;
  color: white;
}

.hero-description {
  font-size: 1.2rem;
  margin: 0;
  opacity: 0.95;
  line-height: 1.6;
}

.categories-section,
.featured-section {
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin: 0 0 2rem 0;
  padding-bottom: 1rem;
  border-bottom: 3px solid #667eea;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-description {
    font-size: 1rem;
  }
  
  .categories-grid,
  .resources-grid {
    grid-template-columns: 1fr;
  }
}
</style>


