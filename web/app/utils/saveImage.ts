/** 从 URL 推断图片扩展名 */
export const extFromImageUrl = (url: string) => {
  const match = url.split('?')[0].match(/\.(jpe?g|png|gif|webp|bmp)$/i)
  return match ? match[1].toLowerCase() : 'jpg'
}

export type SaveImageResult = 'shared' | 'downloaded' | 'preview'

/** 检测是否为移动端（含平板） */
export const isMobileDevice = () => {
  if (typeof navigator === 'undefined') return false
  return /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent)
}

/**
 * 保存图片到设备：移动端优先调起系统分享（可选「存储到相册」），桌面端直接下载。
 */
export async function saveImageToDevice(
  url: string,
  filename: string
): Promise<SaveImageResult> {
  const res = await fetch(url, { mode: 'cors' })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)

  const blob = await res.blob()
  const type = blob.type || 'image/jpeg'
  const file = new File([blob], filename, { type })

  // iOS / Android：系统分享面板里通常有「存储到相册」
  if (
    typeof navigator !== 'undefined' &&
    typeof navigator.share === 'function' &&
    typeof navigator.canShare === 'function' &&
    navigator.canShare({ files: [file] })
  ) {
    await navigator.share({ files: [file] })
    return 'shared'
  }

  // 移动端无分享能力：由页面展示大图，引导长按保存
  if (isMobileDevice()) {
    return 'preview'
  }

  const objectUrl = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = objectUrl
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(objectUrl)
  return 'downloaded'
}
