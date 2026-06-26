<template>
  <div class="admin-page">
    <AdminDataTable
      :data="albums"
      :columns="columns"
      :loading="loading"
      resource-name="音乐专辑"
      @add="openAddModal"
      @edit="openEditModal"
      @delete="handleDelete"
    />

    <AdminFormModal
      :visible="modalVisible"
      :title="isEditing ? '编辑音乐专辑' : '添加音乐专辑'"
      :fields="formFields"
      :initial-data="currentItem"
      :submit-text="isEditing ? '保存' : '添加'"
      @close="closeModal"
      @submit="handleSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'

definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const albums = ref<any[]>([])
const loading = ref(false)
const modalVisible = ref(false)
const isEditing = ref(false)
const currentItem = ref<any>(null)

const columns = [
  { key: 'cover_url', label: '封面', type: 'image', width: 100 },
  { key: 'title', label: '专辑名称', minWidth: 150 },
  { key: 'description', label: '描述', minWidth: 200 },
  { key: 'author', label: '艺术家', width: 120 },
  { key: 'tags', label: '标签', type: 'tags', width: 150 }
]

const formFields = [
  { key: 'title', label: '专辑名称', type: 'text' as const },
  { key: 'description', label: '描述', type: 'textarea' as const },
  { key: 'author', label: '艺术家', type: 'text' as const },
  { key: 'link', label: '链接', type: 'url' as const },
  { key: 'cover_url', label: '封面图片URL', type: 'url' as const, required: false },
  { key: 'tags', label: '标签（逗号分隔）', type: 'text' as const, required: false }
]

const loadData = async () => {
  loading.value = true
  try {
    const response = await api.get<any>('/music/albums')
    // 兼容不同的响应格式
    if (Array.isArray(response.data)) {
      albums.value = response.data
    } else if (Array.isArray(response.data?.list)) {
      albums.value = response.data.list
    } else if (Array.isArray(response.data?.data)) {
      albums.value = response.data.data
    } else {
      albums.value = []
    }
  } catch (error) {
    console.error('加载数据失败', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const openAddModal = () => {
  isEditing.value = false
  currentItem.value = null
  modalVisible.value = true
}

const openEditModal = (item: any) => {
  isEditing.value = true
  currentItem.value = { ...item, tags: item.tags?.join(',') || '' }
  modalVisible.value = true
}

const closeModal = () => {
  modalVisible.value = false
  currentItem.value = null
}

const handleSubmit = async (data: Record<string, any>) => {
  try {
    const submitData = {
      ...data,
      tags: data.tags ? data.tags.split(',').map((t: string) => t.trim()).filter(Boolean) : [],
      category: 'album'
    }

    if (isEditing.value) {
      await api.put(`/music/albums/admin/${currentItem.value.id || currentItem.value._id}`, submitData)
      ElMessage.success('更新成功')
    } else {
      await api.post('/music/albums/admin', submitData)
      ElMessage.success('添加成功')
    }
    
    closeModal()
    loadData()
  } catch (error) {
    console.error('提交失败', error)
    ElMessage.error('操作失败，请重试')
  }
}

const handleDelete = async (item: any) => {
  ElMessageBox.confirm(
    `确定要删除「${item.title}」吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      await api.delete(`/music/albums/admin/${item.id || item._id}`)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败', error)
      ElMessage.error('删除失败，请重试')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.admin-page {
  max-width: 1400px;
}
</style>
