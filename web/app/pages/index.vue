<template>
  <div class="home-page">
    <!-- Banner Section - 轮播图 -->
    <div v-if="banners.length > 0">
      <ClientOnly>
        <div class="banner-section">
          <el-carousel 
            :interval="5000" 
            :height="bannerHeight"
            indicator-position="outside"
            arrow="hover"
          >
            <el-carousel-item 
              v-for="banner in banners" 
              :key="banner.id"
            >
              <div class="banner-item">
                <img 
                  :src="banner.image_url" 
                  :alt="banner.title" 
                  class="banner-image"
                  @error="handleImageError"
                />
                <div class="banner-overlay">
                  <div class="banner-content">
                    <h2 class="banner-title">{{ banner.title }}</h2>
                    <p class="banner-description">{{ banner.description }}</p>
                    <el-button 
                      v-if="banner.link" 
                      type="primary" 
                      size="large"
                      @click="handleBannerClick(banner.link)"
                    >
                      了解更多
                    </el-button>
                  </div>
                </div>
              </div>
            </el-carousel-item>
          </el-carousel>
        </div>
        <template #fallback>
          <div class="banner-section banner-fallback">
            <div class="banner-item">
              <img 
                :src="banners[0].image_url" 
                :alt="banners[0].title" 
                class="banner-image"
              />
              <div class="banner-overlay">
                <div class="banner-content">
                  <h2 class="banner-title">{{ banners[0].title }}</h2>
                  <p class="banner-description">{{ banners[0].description }}</p>
                </div>
              </div>
            </div>
          </div>
        </template>
      </ClientOnly>
    </div>

    <!-- Hero Section -->
    <div v-else class="hero-section">
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

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// 获取首页轮播图数据
const { data: bannerResponse } = await useFetch<any>(`${apiBase}/home/banners`)
const banners = computed(() => {
  const data = bannerResponse.value?.data
  return Array.isArray(data) ? data : []
})

// 轮播图高度（响应式）
const bannerHeight = ref('500px')

onMounted(() => {
  // 客户端挂载后设置响应式高度
  const updateHeight = () => {
    bannerHeight.value = window.innerWidth < 768 ? '300px' : '500px'
  }
  updateHeight()
  window.addEventListener('resize', updateHeight)
  onUnmounted(() => {
    window.removeEventListener('resize', updateHeight)
  })
})

// 处理图片加载错误
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = '/placeholder-banner.jpg' // 可以设置一个默认图片
}

// 处理轮播图点击
const handleBannerClick = (link: string) => {
  if (link) {
    if (link.startsWith('http')) {
      window.open(link, '_blank')
    } else {
      navigateTo(link)
    }
  }
}

// 获取精选资源 (这里我们可以并行获取几个分类的数据)
const { data: progCourses } = await useFetch<any>(`${apiBase}/courses/programming`)
const { data: musicAlbums } = await useFetch<any>(`${apiBase}/music/albums`)

const featuredResources = computed(() => {
  const featured: any[] = []
  
  const progData = progCourses.value?.data
  if (Array.isArray(progData)) {
    featured.push(...progData.slice(0, 3))
  }
  
  const musicData = musicAlbums.value?.data
  if (Array.isArray(musicData)) {
    featured.push(...musicData.slice(0, 3))
  }
  
  return featured
})

// SEO 优化
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

.banner-section {
  margin-bottom: 3rem;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.banner-item {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.banner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.2) 0%,
    rgba(0, 0, 0, 0.4) 50%,
    rgba(0, 0, 0, 0.7) 100%
  );
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 3rem 2rem;
}

.banner-content {
  max-width: 1200px;
  width: 100%;
  text-align: center;
  color: white;
}

.banner-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0 0 1rem 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.6s ease-out;
}

.banner-description {
  font-size: 1.2rem;
  margin: 0 0 1.5rem 0;
  opacity: 0.95;
  line-height: 1.6;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.8s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Element Plus 轮播图样式定制 */
:deep(.el-carousel__container) {
  height: 100%;
}

:deep(.el-carousel__indicators) {
  bottom: 20px;
}

:deep(.el-carousel__button) {
  background-color: rgba(255, 255, 255, 0.5);
  border: 2px solid rgba(255, 255, 255, 0.8);
}

:deep(.el-carousel__button:hover) {
  background-color: rgba(255, 255, 255, 0.8);
}

:deep(.el-carousel__indicator.is-active .el-carousel__button) {
  background-color: #667eea;
  border-color: #667eea;
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
  .banner-overlay {
    padding: 2rem 1rem;
  }

  .banner-title {
    font-size: 1.8rem;
  }

  .banner-description {
    font-size: 1rem;
  }

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


