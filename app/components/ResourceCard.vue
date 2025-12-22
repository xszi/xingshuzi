<template>
  <div class="resource-card">
    <div class="resource-cover" v-if="resource.cover">
      <img :src="resource.cover" :alt="resource.title" />
    </div>
    <div class="resource-content">
      <h3 class="resource-title">{{ resource.title }}</h3>
      <p class="resource-description">{{ resource.description }}</p>
      
      <div class="resource-meta">
        <span v-if="resource.author" class="resource-author">
          <span class="meta-icon">👤</span>
          {{ resource.author }}
        </span>
        <span v-if="resource.price" class="resource-price">
          {{ resource.price }}
        </span>
      </div>
      
      <div v-if="resource.tags && resource.tags.length > 0" class="resource-tags">
        <span 
          v-for="tag in resource.tags" 
          :key="tag" 
          class="resource-tag"
        >
          {{ tag }}
        </span>
      </div>
      
      <a 
        :href="resource.link" 
        :target="resource.isExternal ? '_blank' : '_self'"
        :rel="resource.isExternal ? 'noopener noreferrer' : undefined"
        class="resource-link"
        @click="handleClick"
      >
        {{ resource.isExternal ? '前往淘宝购买' : '查看详情' }}
        <span class="link-arrow">→</span>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Resource } from '~/data/resources'

const props = defineProps<{
  resource: Resource
}>()

const handleClick = (e: Event) => {
  if (props.resource.isExternal) {
    // 外部链接，允许默认行为
    return
  }
  // 内部链接可以在这里添加导航逻辑
  e.preventDefault()
  // 可以添加路由跳转或其他逻辑
}
</script>

<style scoped>
.resource-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.resource-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
}

.resource-cover {
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.resource-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.resource-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.resource-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #333;
  margin: 0 0 0.75rem 0;
  line-height: 1.4;
}

.resource-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.6;
  margin: 0 0 1rem 0;
  flex: 1;
}

.resource-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.resource-author {
  font-size: 0.85rem;
  color: #888;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.meta-icon {
  font-size: 0.9rem;
}

.resource-price {
  font-size: 1.1rem;
  font-weight: bold;
  color: #667eea;
}

.resource-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.resource-tag {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  background: #f0f0f0;
  color: #666;
  border-radius: 12px;
}

.resource-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  margin-top: auto;
}

.resource-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.link-arrow {
  transition: transform 0.3s ease;
}

.resource-link:hover .link-arrow {
  transform: translateX(4px);
}
</style>

