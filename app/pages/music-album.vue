<template>
  <div class="category-page">
    <div class="category-header">
      <h1 class="category-title">
        <span class="category-icon">🎶</span>
        音乐专辑
      </h1>
      <p class="category-description">精选音乐专辑资源，高品质音频下载</p>
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
import { sampleResources } from '~/data/resources'
import { generateItemListSchema } from '~/utils/structuredData'

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl || 'https://xingshuzi.com'

const resources = computed(() => {
  return sampleResources['music-album'] || []
})

const structuredData = computed(() => {
  const albumList = resources.value.map((resource) => ({
    name: resource.title,
    description: resource.description,
    url: `${siteUrl}/music-album#${resource.id}`
  }))
  
  return generateItemListSchema(albumList)
})

useSEO({
  title: '音乐专辑',
  description: '精选音乐专辑资源，高品质音频下载。流行音乐、轻音乐、古典音乐等各类专辑。',
  keywords: '音乐专辑,高品质音乐,无损音质,流行音乐,轻音乐,古典音乐,音乐下载',
  url: `${siteUrl}/music-album`,
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
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
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

