# SEO 优化说明

本文档说明已实施的 SEO 优化措施。

## 已实施的 SEO 优化

### 1. Meta 标签优化

#### 基础 Meta 标签
- ✅ 页面标题（Title）- 每个页面都有独特的标题
- ✅ 页面描述（Description）- 每个页面都有详细的描述
- ✅ 关键词（Keywords）- 针对每个分类页面优化
- ✅ 语言设置（lang="zh-CN"）
- ✅ 字符编码（UTF-8）
- ✅ 视口设置（viewport）

#### 搜索引擎指令
- ✅ robots meta 标签
- ✅ Googlebot 指令
- ✅ 语言和地区设置

### 2. Open Graph 标签（社交媒体分享）

所有页面都包含完整的 Open Graph 标签：
- `og:type` - 内容类型
- `og:title` - 标题
- `og:description` - 描述
- `og:image` - 分享图片
- `og:url` - 页面 URL
- `og:locale` - 语言设置

### 3. Twitter Card 标签

- `twitter:card` - 卡片类型（summary_large_image）
- `twitter:title` - 标题
- `twitter:description` - 描述
- `twitter:image` - 图片

### 4. 结构化数据（Schema.org JSON-LD）

已为以下内容添加结构化数据：

#### 网站级
- ✅ WebSite schema - 网站基本信息
- ✅ Organization schema - 组织信息
- ✅ SearchAction - 搜索功能

#### 页面级
- ✅ ItemList schema - 资源列表
- ✅ Course schema - 课程信息（编程课程、音乐课程）
- ✅ Book schema - 书籍信息
- ✅ Product schema - 产品信息（助农产品）

### 5. 技术 SEO

#### URL 优化
- ✅ 语义化 URL（/programming-course, /music-course 等）
- ✅ Canonical URL - 防止重复内容
- ✅ 多语言支持准备（hreflang）

#### 页面结构
- ✅ 语义化 HTML5 标签（header, nav, main, footer）
- ✅ ARIA 标签（role, aria-label）
- ✅ 标题层级（H1, H2, H3）
- ✅ 图片懒加载（loading="lazy"）
- ✅ 图片 alt 属性

#### 性能优化
- ✅ 服务端渲染（SSR）
- ✅ 图片优化准备

### 6. robots.txt

已优化 robots.txt：
- ✅ 允许所有搜索引擎爬取
- ✅ 禁止爬取 API 和管理页面
- ✅ 指向 sitemap.xml

### 7. Sitemap.xml

已创建动态 sitemap 生成：
- ✅ 自动生成所有页面
- ✅ 设置更新频率（changefreq）
- ✅ 设置优先级（priority）
- ✅ 最后更新时间（lastmod）

访问地址：`/sitemap.xml`

### 8. 移动端优化

- ✅ 响应式设计
- ✅ 移动端视口设置
- ✅ 主题颜色设置
- ✅ Apple 移动端优化标签

## 使用方法

### 1. 设置网站 URL

创建 `.env` 文件（参考 `.env.example`）：

```env
NUXT_PUBLIC_SITE_URL=https://your-domain.com
```

### 2. 使用 SEO Composable

在页面中使用 `useSEO` composable：

```vue
<script setup lang="ts">
useSEO({
  title: '页面标题',
  description: '页面描述',
  keywords: '关键词1,关键词2',
  url: 'https://your-domain.com/page',
  structuredData: {
    // JSON-LD 结构化数据
  }
})
</script>
```

### 3. 生成结构化数据

使用工具函数生成结构化数据：

```typescript
import { generateCourseSchema, generateBookSchema } from '~/utils/structuredData'

// 生成课程结构化数据
const courseSchema = generateCourseSchema({
  name: '课程名称',
  description: '课程描述',
  url: 'https://your-domain.com/course',
  provider: '提供者',
  price: '¥199'
})
```

## SEO 检查清单

### 页面级别
- [x] 每个页面都有唯一的 title
- [x] 每个页面都有唯一的 description
- [x] 每个页面都有相关的 keywords
- [x] 每个页面都有 canonical URL
- [x] 每个页面都有 Open Graph 标签
- [x] 每个页面都有 Twitter Card 标签
- [x] 重要页面都有结构化数据

### 技术层面
- [x] robots.txt 配置正确
- [x] sitemap.xml 可访问
- [x] 语义化 HTML
- [x] 图片有 alt 属性
- [x] 链接使用语义化 URL
- [x] 页面加载速度优化

### 内容层面
- [x] 标题使用 H1-H6 层级
- [x] 内容结构清晰
- [x] 内部链接优化
- [x] 关键词自然分布

## 下一步优化建议

1. **添加 Open Graph 图片**
   - 创建 `/public/og-image.jpg` (1200x630px)
   - 为每个分类创建专门的 OG 图片

2. **添加网站图标**
   - 创建 `/public/logo.png`
   - 添加 favicon 多种尺寸

3. **性能优化**
   - 图片压缩和 WebP 格式
   - 代码分割和懒加载
   - CDN 配置

4. **内容优化**
   - 定期更新内容
   - 添加更多内部链接
   - 创建内容分类和标签

5. **分析工具**
   - 集成 Google Analytics
   - 集成 Google Search Console
   - 添加百度统计（如需要）

6. **社交媒体**
   - 添加社交媒体链接
   - 创建社交媒体分享按钮

## 验证工具

使用以下工具验证 SEO：

1. **Google Search Console** - https://search.google.com/search-console
2. **Google Rich Results Test** - https://search.google.com/test/rich-results
3. **Schema.org Validator** - https://validator.schema.org/
4. **Facebook Sharing Debugger** - https://developers.facebook.com/tools/debug/
5. **Twitter Card Validator** - https://cards-dev.twitter.com/validator
6. **PageSpeed Insights** - https://pagespeed.web.dev/

## 注意事项

1. **网站 URL** - 确保在生产环境中设置正确的 `NUXT_PUBLIC_SITE_URL`
2. **OG 图片** - 建议创建并上传 OG 图片到 `/public/og-image.jpg`
3. **定期更新** - 定期更新 sitemap 和内容
4. **监控** - 使用 Google Search Console 监控 SEO 表现

## 相关文件

- `nuxt.config.ts` - 全局 SEO 配置
- `app/composables/useSEO.ts` - SEO composable
- `app/utils/structuredData.ts` - 结构化数据工具
- `server/routes/sitemap.xml.ts` - Sitemap 生成
- `public/robots.txt` - Robots 文件




