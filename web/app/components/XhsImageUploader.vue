<template>
  <div class="xhs-image-uploader">
    <div class="image-list-wrap">
      <div ref="listRef" class="image-list">
        <div
          v-for="(img, i) in images"
          :key="`${img}-${i}`"
          class="uploaded-thumb"
        >
          <span class="thumb-order">{{ i + 1 }}</span>
          <el-image
            :src="img"
            :preview-src-list="images"
            :initial-index="i"
            fit="cover"
            class="thumb-img"
            preview-teleported
          />
          <div class="thumb-actions">
            <button type="button" class="thumb-action thumb-preview" @click.stop="openPreview(i)">
              预览
            </button>
            <button type="button" class="thumb-action thumb-delete" @click.stop="removeAt(i)">
              删除
            </button>
          </div>
        </div>
      </div>

      <el-upload
        v-if="httpRequest"
        multiple
        :show-file-list="false"
        :before-upload="beforeUploadHandler"
        :http-request="httpRequest"
        accept="image/*"
        class="upload-trigger"
      >
        <div class="upload-box">
          <span v-if="uploading" class="upload-loading">上传中...</span>
          <span v-else class="upload-plus">＋</span>
        </div>
      </el-upload>
    </div>
    <p v-if="hint" class="upload-hint">{{ hint }}</p>
  </div>
</template>

<script setup lang="ts">
import Sortable from 'sortablejs'
import type { UploadRequestHandler, UploadProps } from 'element-plus'

const images = defineModel<string[]>({ default: () => [] })

const props = withDefaults(
  defineProps<{
    uploading?: boolean
    beforeUpload?: UploadProps['beforeUpload']
    httpRequest?: UploadRequestHandler
    hint?: string
  }>(),
  {
    uploading: false,
    hint: '可拖动调整顺序 · 点击预览 · jpg / png / gif / webp，单张 ≤10MB'
  }
)

const listRef = ref<HTMLElement | null>(null)
let sortable: Sortable | null = null

const removeAt = (index: number) => {
  images.value = images.value.filter((_, i) => i !== index)
}

const openPreview = (index: number) => {
  const list = listRef.value
  if (!list) return
  const imgEl = list.querySelectorAll('.thumb-img img')[index] as HTMLElement | undefined
  imgEl?.click()
}

const beforeUploadHandler: UploadProps['beforeUpload'] = (file) => {
  if (props.beforeUpload) {
    return props.beforeUpload(file)
  }
  return true
}

const initSortable = () => {
  if (!listRef.value || sortable) return
  sortable = Sortable.create(listRef.value, {
    animation: 160,
    delay: 180,
    delayOnTouchOnly: true,
    touchStartThreshold: 6,
    draggable: '.uploaded-thumb',
    filter: '.thumb-action',
    preventOnFilter: false,
    ghostClass: 'uploaded-thumb--ghost',
    chosenClass: 'uploaded-thumb--chosen',
    onEnd: (evt) => {
      const { oldIndex, newIndex } = evt
      if (
        oldIndex === undefined ||
        newIndex === undefined ||
        oldIndex === newIndex
      ) {
        return
      }
      const next = [...images.value]
      const [moved] = next.splice(oldIndex, 1)
      next.splice(newIndex, 0, moved)
      images.value = next
    }
  })
}

onMounted(() => {
  nextTick(initSortable)
})

onBeforeUnmount(() => {
  sortable?.destroy()
  sortable = null
})
</script>

<style scoped>
.xhs-image-uploader {
  max-width: 100%;
  overflow: hidden;
}

.image-list-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.uploaded-thumb {
  position: relative;
  width: 90px;
  height: 90px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #eee;
  flex-shrink: 0;
  cursor: grab;
  touch-action: manipulation;
  user-select: none;
}

.uploaded-thumb:active {
  cursor: grabbing;
}

.uploaded-thumb--ghost {
  opacity: 0.45;
}

.uploaded-thumb--chosen {
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.35);
}

.thumb-order {
  position: absolute;
  top: 4px;
  left: 4px;
  z-index: 2;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  border-radius: 9px;
  background: rgba(102, 126, 234, 0.92);
  color: #fff;
  font-size: 0.7rem;
  line-height: 18px;
  text-align: center;
  pointer-events: none;
}

.thumb-img {
  width: 100%;
  height: 100%;
  display: block;
}

.thumb-img :deep(.el-image__inner) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-actions {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  background: rgba(0, 0, 0, 0.48);
  opacity: 0;
  transition: opacity 0.2s;
}

.uploaded-thumb:hover .thumb-actions,
.uploaded-thumb:focus-within .thumb-actions {
  opacity: 1;
}

.thumb-action {
  border: none;
  border-radius: 4px;
  padding: 0.2rem 0.55rem;
  font-size: 0.75rem;
  line-height: 1.2;
  cursor: pointer;
}

.thumb-preview {
  background: rgba(255, 255, 255, 0.92);
  color: #333;
}

.thumb-delete {
  background: rgba(245, 108, 108, 0.95);
  color: #fff;
}

.upload-trigger :deep(.el-upload) {
  display: block;
}

.upload-box {
  width: 90px;
  height: 90px;
  border: 1px dashed #c0c4cc;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: #fafafa;
  flex-shrink: 0;
}

.upload-box:hover {
  border-color: #667eea;
}

.upload-plus {
  font-size: 1.8rem;
  color: #c0c4cc;
}

.upload-loading {
  font-size: 0.8rem;
  color: #999;
}

.upload-hint {
  margin: 0.5rem 0 0;
  font-size: 0.8rem;
  color: #999;
  line-height: 1.4;
}

@media (hover: none) {
  .thumb-actions {
    opacity: 1;
    background: rgba(0, 0, 0, 0.35);
    gap: 0.25rem;
  }

  .uploaded-thumb,
  .upload-box {
    width: 76px;
    height: 76px;
  }
}

@media (max-width: 768px) {
  .uploaded-thumb,
  .upload-box {
    width: 76px;
    height: 76px;
  }
}
</style>
