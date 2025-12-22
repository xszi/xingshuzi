// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  
  // 确保服务端渲染（SSR）模式
  ssr: true,
  
  // 应用配置
  app: {
    head: {
      title: '行书子',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: '行书子 - 资源分享平台，提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  }
})
