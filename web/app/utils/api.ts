// API 请求工具函数（带 Token）
export const apiRequest = async <T = any>(
  url: string,
  options: RequestInit = {}
): Promise<T> => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase
  
  // 从 localStorage 获取 token
  let token: string | null = null
  if (process.client) {
    token = localStorage.getItem('token')
  }

  // 构建请求头
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {})
  }

  // 如果有 token，添加 Authorization 头
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  try {
    const response = await $fetch<T>(`${apiBase}${url}`, {
      ...options,
      headers
    })

    return response
  } catch (error: any) {
    // 如果是 401 错误，清除登录信息并跳转到登录页
    if (error.status === 401 && process.client) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      navigateTo('/login')
    }
    throw error
  }
}

// 便捷方法
export const api = {
  get: <T = any>(url: string) => apiRequest<T>(url, { method: 'GET' }),
  
  post: <T = any>(url: string, body: any) => 
    apiRequest<T>(url, {
      method: 'POST',
      body: JSON.stringify(body)
    }),
  
  put: <T = any>(url: string, body: any) => 
    apiRequest<T>(url, {
      method: 'PUT',
      body: JSON.stringify(body)
    }),
  
  delete: <T = any>(url: string) =>
    apiRequest<T>(url, { method: 'DELETE' }),

  // 上传文件（multipart/form-data，不能手动设置 Content-Type）
  upload: <T = any>(url: string, file: File): Promise<T> => {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    let token: string | null = null
    if (process.client) {
      token = localStorage.getItem('token')
    }

    const formData = new FormData()
    formData.append('file', file)

    const headers: Record<string, string> = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    return $fetch<T>(`${apiBase}${url}`, {
      method: 'POST',
      headers,
      body: formData
    })
  }
}




