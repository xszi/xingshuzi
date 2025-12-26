<template>
  <div class="data-table">
    <div class="table-header">
      <el-button type="primary" @click="$emit('add')" :icon="Plus">
        添加{{ resourceName }}
      </el-button>
    </div>

    <el-table 
      :data="data" 
      v-loading="loading"
      stripe
      border
      style="width: 100%"
      :empty-text="'暂无数据'"
      :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
    >
      <el-table-column
        v-for="column in columns"
        :key="column.key"
        :prop="column.key"
        :label="column.label"
        :width="column.width"
        :min-width="column.minWidth || 100"
      >
        <template #default="{ row }">
          <template v-if="column.type === 'image'">
            <el-image 
              v-if="row[column.key]"
              :src="row[column.key]"
              :alt="row.title"
              style="width: 60px; height: 60px"
              fit="cover"
              :preview-src-list="[row[column.key]]"
            />
          </template>
          <template v-else-if="column.type === 'tags'">
            <el-tag 
              v-for="tag in row[column.key]" 
              :key="tag"
              size="small"
              style="margin-right: 5px"
            >
              {{ tag }}
            </el-tag>
          </template>
          <template v-else>
            {{ row[column.key] }}
          </template>
        </template>
      </el-table-column>

      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button 
            type="primary" 
            size="small" 
            :icon="Edit"
            @click="$emit('edit', row)"
          >
            编辑
          </el-button>
          <el-button 
            type="danger" 
            size="small" 
            :icon="Delete"
            @click="$emit('delete', row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { Plus, Edit, Delete } from '@element-plus/icons-vue'

defineProps<{
  data: any[]
  columns: Array<{ 
    key: string
    label: string
    type?: string
    width?: string | number
    minWidth?: string | number
  }>
  loading?: boolean
  resourceName: string
}>()

defineEmits<{
  add: []
  edit: [item: any]
  delete: [item: any]
}>()
</script>

<style scoped>
.data-table {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.table-header {
  margin-bottom: 1.5rem;
}
</style>
