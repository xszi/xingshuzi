/** 公开页 API：不携带登录 Token，避免管理员会话绕过提交密码校验 */
export const publicApi = {
  post: <T = any>(url: string, body: Record<string, unknown>) => {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase
    return $fetch<T>(`${apiBase}${url}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
  },

  upload: <T = any>(
    url: string,
    file: File,
    extraFields?: Record<string, string>
  ): Promise<T> => {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase
    const formData = new FormData()
    formData.append('file', file)
    if (extraFields) {
      for (const [key, value] of Object.entries(extraFields)) {
        formData.append(key, value)
      }
    }
    return $fetch<T>(`${apiBase}${url}`, {
      method: 'POST',
      body: formData
    })
  }
}
