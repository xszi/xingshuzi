// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  // 确保服务端渲染（SSR）模式
  ssr: true,

  // Element Plus 模块
  modules: ['@element-plus/nuxt'],
  
  // SEO 优化配置
  site: {
    url: process.env.NUXT_PUBLIC_SITE_URL || 'https://xingshuzi.com',
    name: '行书子',
    description: '行书子 - 资源分享平台，提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源',
    defaultLocale: 'zh-CN'
  },
  
  // 运行时配置
  runtimeConfig: {
    public: {
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || 'https://xingshuzi.com',
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:5001/api'
    }
  },
  
  // 应用配置
  app: {
    head: {
      htmlAttrs: {
        lang: 'zh-CN'
      },
      title: '行书子 - 资源分享平台',
      titleTemplate: '%s - 行书子',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=5' },
        { 
          name: 'description', 
          content: '行书子 - 资源分享平台，提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源。优质内容，值得信赖。' 
        },
        { 
          name: 'keywords', 
          content: '资源分享,编程课程,音乐课程,音乐专辑,电子书,二手书,助农产品,在线学习,教育资源' 
        },
        { name: 'author', content: '行书子' },
        { name: 'robots', content: 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1' },
        { name: 'googlebot', content: 'index, follow' },
        { name: 'language', content: 'Chinese' },
        { name: 'revisit-after', content: '7 days' },
        
        // Open Graph / Facebook
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: '行书子' },
        { property: 'og:title', content: '行书子 - 资源分享平台' },
        { 
          property: 'og:description', 
          content: '提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源' 
        },
        { property: 'og:locale', content: 'zh_CN' },
        { property: 'og:image', content: '/og-image.jpg' },
        { property: 'og:image:width', content: '1200' },
        { property: 'og:image:height', content: '630' },
        { property: 'og:image:alt', content: '行书子资源分享平台' },
        
        // Twitter Card
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: '行书子 - 资源分享平台' },
        { 
          name: 'twitter:description', 
          content: '提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源' 
        },
        { name: 'twitter:image', content: '/og-image.jpg' },
        
        // 移动端优化
        { name: 'theme-color', content: '#667eea' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },
        { name: 'apple-mobile-web-app-title', content: '行书子' },
        { name: 'format-detection', content: 'telephone=no' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'canonical', href: process.env.NUXT_PUBLIC_SITE_URL || 'https://xingshuzi.com' },
        { rel: 'alternate', hreflang: 'zh-CN', href: process.env.NUXT_PUBLIC_SITE_URL || 'https://xingshuzi.com' }
      ]
    }
  }
})
