// Sitemap 生成路由
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const siteUrl = config.public?.siteUrl || process.env.NUXT_PUBLIC_SITE_URL || 'https://xingshuzi.com'
  
  // 定义所有页面
  const pages = [
    { url: '', changefreq: 'daily', priority: '1.0' },
    { url: '/programming-course', changefreq: 'weekly', priority: '0.9' },
    { url: '/music-course', changefreq: 'weekly', priority: '0.9' },
    { url: '/music-album', changefreq: 'weekly', priority: '0.9' },
    { url: '/books', changefreq: 'weekly', priority: '0.9' },
    { url: '/agricultural-product', changefreq: 'daily', priority: '0.8' },
    { url: '/about', changefreq: 'monthly', priority: '0.5' }
  ]
  
  const currentDate = new Date().toISOString()
  
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(page => `  <url>
    <loc>${siteUrl}${page.url}</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('\n')}
</urlset>`
  
  event.node.res.setHeader('Content-Type', 'application/xml')
  return sitemap
})

