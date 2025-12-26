<template>
  <div class="category-page">
    <div class="category-header">
      <h1 class="category-title">
        <span class="category-icon">📚</span>
        各类书籍
      </h1>
      <p class="category-description">电子书、二手书等各类图书资源</p>
    </div>

    <div v-if="resources.length > 0" class="resources-section">
      <div class="resources-grid">
        <ResourceCard 
          v-for="resource in resources" 
          :key="resource.id" 
          :resource="resource" 
        />
      </div>
    </div>

    <div v-else class="empty-state">
      <p>暂无资源，敬请期待...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { generateItemListSchema, generateBookSchema } from '~/utils/structuredData'

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl || 'https://xingshuzi.com'
const apiBase = config.public.apiBase

// 从后端接口获取数据
const { data: apiResponse, pending } = await useFetch<any>(`${apiBase}/books/list`)

const resources = computed(() => {
  const data = apiResponse.value?.data
  return Array.isArray(data) ? data : []
})

const structuredData = computed(() => {
  const bookList = resources.value.map((resource: any) => ({
    name: resource.title,
    description: resource.description,
    url: `${siteUrl}/books#${resource.id || resource._id}`
  }))
  
  return [
    generateItemListSchema(bookList),
    ...resources.value.map((resource: any) => 
      generateBookSchema({
        name: resource.title,
        description: resource.description,
        url: `${siteUrl}/books#${resource.id || resource._id}`,
        author: resource.author,
        price: resource.price
      })
    )
  ]
})

useSEO({
  title: '各类书籍',
  description: '电子书、二手书等各类图书资源。编程书籍、技术书籍、经典文学作品等。',
  keywords: '电子书,二手书,编程书籍,技术书籍,JavaScript,计算机科学,设计模式,图书资源',
  url: `${siteUrl}/books`,
  structuredData: structuredData.value
})
</script>

<style scoped>
.category-page {
  animation: fadeIn 0.5s ease-in;
}

.category-header {
  text-align: center;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  border-radius: 16px;
  margin-bottom: 3rem;
  color: white;
}

.category-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: white;
}

.category-icon {
  font-size: 3rem;
}

.category-description {
  font-size: 1.2rem;
  margin: 0;
  opacity: 0.95;
}

.resources-section {
  margin-bottom: 2rem;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.empty-state p {
  font-size: 1.2rem;
  color: #999;
  margin: 0;
}

@media (max-width: 768px) {
  .category-title {
    font-size: 2rem;
    flex-direction: column;
  }
  
  .resources-grid {
    grid-template-columns: 1fr;
  }
}
</style>

