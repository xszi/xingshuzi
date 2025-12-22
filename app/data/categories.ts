// 资源分类数据
export interface Category {
  id: string
  name: string
  description: string
  icon: string
  route: string
  color: string
}

export const categories: Category[] = [
  {
    id: 'programming-course',
    name: '编程课程',
    description: '优质的编程学习课程，涵盖前端、后端、移动开发等',
    icon: '💻',
    route: '/programming-course',
    color: '#667eea'
  },
  {
    id: 'music-course',
    name: '音乐课程',
    description: '专业的音乐教学课程，包括乐器、声乐、乐理等',
    icon: '🎵',
    route: '/music-course',
    color: '#f093fb'
  },
  {
    id: 'music-album',
    name: '音乐专辑',
    description: '精选音乐专辑资源，高品质音频下载',
    icon: '🎶',
    route: '/music-album',
    color: '#4facfe'
  },
  {
    id: 'books',
    name: '各类书籍',
    description: '电子书、二手书等各类图书资源',
    icon: '📚',
    route: '/books',
    color: '#43e97b'
  },
  {
    id: 'agricultural-product',
    name: '助农产品',
    description: '优质农产品，支持助农，跳转淘宝购买',
    icon: '🌾',
    route: '/agricultural-product',
    color: '#fa709a'
  }
]

