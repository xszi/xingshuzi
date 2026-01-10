// 用户认证相关的 composable
export const useAuth = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // 用户信息状态
  const user = useState<any>('user', () => null)
  const token = useState<string | null>('token', () => null)

  // 从 localStorage 加载用户信息
  const loadUser = () => {
    if (process.client) {
      const storedToken = localStorage.getItem('token')
      const storedUser = localStorage.getItem('user')
      
      if (storedToken && storedUser) {
        token.value = storedToken
        try {
          user.value = JSON.parse(storedUser)
        } catch (e) {
          console.error('解析用户信息失败', e)
        }
      }
    }
  }

  // 登录
  const login = async (username: string, password: string) => {
    try {
      const response = await $fetch<any>(`${apiBase}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })

      if (response.code === 200 && response.data) {
        // 保存 token 和用户信息
        token.value = response.data.token
        user.value = response.data.user
        
        if (process.client) {
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('user', JSON.stringify(response.data.user))
        }
        
        return { success: true, user: response.data.user }
      } else {
        return { success: false, message: response.msg || '登录失败' }
      }
    } catch (error: any) {
      console.error('登录错误:', error)
      return { success: false, message: error.data?.msg || '登录失败，请稍后重试' }
    }
  }

  // 注册
  const register = async (username: string, password: string) => {
    try {
      const response = await $fetch<any>(`${apiBase}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })

      if (response.code === 200) {
        return { success: true, message: '注册成功，请登录' }
      } else {
        return { success: false, message: response.msg || '注册失败' }
      }
    } catch (error: any) {
      console.error('注册错误:', error)
      return { success: false, message: error.data?.msg || '注册失败，请稍后重试' }
    }
  }

  // 登出
  const logout = () => {
    token.value = null
    user.value = null
    
    if (process.client) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // 跳转到首页
      navigateTo('/')
    }
  }

  // 检查是否登录
  const isLoggedIn = computed(() => !!token.value && !!user.value)

  // 检查是否是管理员
  const isAdmin = computed(() => {
    return user.value?.role === 'admin'
  })

  // 初始化时加载用户信息
  if (process.client && !user.value) {
    loadUser()
  }

  return {
    user,
    token,
    isLoggedIn,
    isAdmin,
    login,
    register,
    logout,
    loadUser
  }
}




