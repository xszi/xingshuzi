<template>
  <div class="category-page">
    <div class="category-header">
      <h1 class="category-title">
        <span class="category-icon">🌾</span>
        助农产品
      </h1>
      <p class="category-description">优质农产品，支持助农，跳转淘宝购买</p>
      <p class="notice">💡 点击商品卡片将跳转到淘宝进行购买</p>
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
  return sampleResources['agricultural-product'] || []
})

const structuredData = computed(() => {
  const productList = resources.value.map((resource) => ({
    name: resource.title,
    description: resource.description,
    url: resource.link
  }))
  
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    itemListElement: productList.map((product, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      item: {
        '@type': 'Product',
        name: product.name,
        description: product.description,
        url: product.url,
        offers: {
          '@type': 'Offer',
          availability: 'https://schema.org/InStock',
          priceCurrency: 'CNY'
        }
      }
    }))
  }
})

useSEO({
  title: '助农产品',
  description: '优质农产品，支持助农，跳转淘宝购买。有机大米、新鲜水果、土鸡蛋等绿色健康农产品。',
  keywords: '助农产品,农产品,有机食品,绿色食品,淘宝购买,支持助农,有机大米,新鲜水果',
  url: `${siteUrl}/agricultural-product`,
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
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
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
  margin: 0 0 0.5rem 0;
  opacity: 0.95;
}

.notice {
  font-size: 1rem;
  margin: 1rem 0 0 0;
  opacity: 0.9;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  display: inline-block;
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

