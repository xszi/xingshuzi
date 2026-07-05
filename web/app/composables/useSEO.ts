// SEO 组合式函数
export const useSEO = (options: {
  title?: string
  description?: string
  keywords?: string
  image?: string
  url?: string
  type?: string
  structuredData?: object
}) => {
  const config = useRuntimeConfig()
  const route = useRoute()
  
  const siteUrl = config.public.siteUrl || process.env.NUXT_PUBLIC_SITE_URL || 'https://xingshuzi.com'
  const fullUrl = options.url || `${siteUrl}${route.path}`
  // 仅返回页面自身标题，站点名「行书子」由 nuxt.config 的 titleTemplate 统一追加，避免重复
  const title = options.title || '行书子 - 资源分享平台'
  const description = options.description || '行书子 - 资源分享平台，提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源'
  const image = options.image || `${siteUrl}/og-image.jpg`
  
  useHead({
    title,
    meta: [
      { name: 'description', content: description },
      { name: 'keywords', content: options.keywords || '资源分享,编程课程,音乐课程,音乐专辑,电子书,二手书,助农产品' },
      
      // Open Graph
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:image', content: image },
      { property: 'og:url', content: fullUrl },
      { property: 'og:type', content: options.type || 'website' },
      
      // Twitter Card
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: title },
      { name: 'twitter:description', content: description },
      { name: 'twitter:image', content: image }
    ],
    link: [
      { rel: 'canonical', href: fullUrl }
    ],
    script: options.structuredData ? (
      Array.isArray(options.structuredData)
        ? options.structuredData.map((data: any) => ({
            type: 'application/ld+json',
            children: JSON.stringify(data)
          }))
        : [{
            type: 'application/ld+json',
            children: JSON.stringify(options.structuredData)
          }]
    ) : []
  })
}

