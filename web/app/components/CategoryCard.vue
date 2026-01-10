<template>
  <NuxtLink :to="category.route" class="category-card">
    <div class="category-icon">{{ category.icon }}</div>
    <h3 class="category-name">{{ category.name }}</h3>
    <p class="category-description">{{ category.description }}</p>
    <div class="category-arrow">→</div>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { Category } from '~/data/categories'

defineProps<{
  category: Category
}>()
</script>

<style scoped>
.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2.5rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.category-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: v-bind('category.color');
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.category-card:hover::before {
  transform: scaleX(1);
}

.category-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  transition: transform 0.3s ease;
}

.category-card:hover .category-icon {
  transform: scale(1.1);
}

.category-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin: 0 0 0.75rem 0;
  text-align: center;
}

.category-description {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.6;
  text-align: center;
  margin: 0 0 1rem 0;
  flex: 1;
}

.category-arrow {
  font-size: 1.5rem;
  color: v-bind('category.color');
  font-weight: bold;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.category-card:hover .category-arrow {
  opacity: 1;
  transform: translateX(0);
}
</style>




