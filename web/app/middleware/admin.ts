// 路由中间件：保护后台管理页面，只有管理员可以访问
// 普通用户或未登录用户访问 /admin/* 时会被重定向
export default defineNuxtRouteMiddleware((to) => {
  // 仅在客户端校验（登录态保存在 localStorage，SSR 阶段无法读取）
  if (process.server) return

  const { isLoggedIn, isAdmin } = useAuth()

  // 未登录：跳转到登录页，并携带回跳地址
  if (!isLoggedIn.value) {
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }

  // 已登录但非管理员：跳转回首页
  if (!isAdmin.value) {
    return navigateTo('/')
  }
})
