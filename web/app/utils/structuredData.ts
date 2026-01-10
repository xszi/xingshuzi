// 结构化数据工具函数

export const generateOrganizationSchema = (siteUrl: string) => {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: '行书子',
    url: siteUrl,
    logo: `${siteUrl}/logo.png`,
    description: '资源分享平台，提供编程课程、音乐课程、音乐专辑、各类书籍、助农产品等优质资源',
    sameAs: [
      // 可以添加社交媒体链接
    ]
  }
}

export const generateBreadcrumbSchema = (items: Array<{ name: string; url: string }>) => {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url
    }))
  }
}

export const generateItemListSchema = (items: Array<{
  name: string
  description: string
  url: string
}>) => {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      item: {
        '@type': 'Product',
        name: item.name,
        description: item.description,
        url: item.url
      }
    }))
  }
}

export const generateCourseSchema = (course: {
  name: string
  description: string
  url: string
  provider?: string
  price?: string
}) => {
  return {
    '@context': 'https://schema.org',
    '@type': 'Course',
    name: course.name,
    description: course.description,
    url: course.url,
    provider: course.provider ? {
      '@type': 'Organization',
      name: course.provider
    } : undefined,
    offers: course.price ? {
      '@type': 'Offer',
      price: course.price,
      priceCurrency: 'CNY'
    } : undefined
  }
}

export const generateBookSchema = (book: {
  name: string
  description: string
  url: string
  author?: string
  price?: string
}) => {
  return {
    '@context': 'https://schema.org',
    '@type': 'Book',
    name: book.name,
    description: book.description,
    url: book.url,
    author: book.author ? {
      '@type': 'Person',
      name: book.author
    } : undefined,
    offers: book.price ? {
      '@type': 'Offer',
      price: book.price,
      priceCurrency: 'CNY'
    } : undefined
  }
}
