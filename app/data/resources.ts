// 资源数据
export interface Resource {
  id: string
  title: string
  description: string
  category: string
  cover?: string
  link: string
  price?: string
  author?: string
  tags?: string[]
  isExternal?: boolean // 是否为外部链接（如淘宝）
}

// 示例资源数据
export const sampleResources: Record<string, Resource[]> = {
  'programming-course': [
    {
      id: 'pc-1',
      title: 'Vue.js 3 从入门到精通',
      description: '全面学习 Vue 3 框架，包括 Composition API、Pinia 状态管理等',
      category: 'programming-course',
      link: '#',
      price: '¥199',
      author: '张老师',
      tags: ['Vue', '前端', 'JavaScript']
    },
    {
      id: 'pc-2',
      title: 'Node.js 后端开发实战',
      description: '从零开始学习 Node.js，构建 RESTful API 和微服务',
      category: 'programming-course',
      link: '#',
      price: '¥299',
      author: '李老师',
      tags: ['Node.js', '后端', 'API']
    },
    {
      id: 'pc-3',
      title: 'TypeScript 高级编程',
      description: '深入学习 TypeScript 类型系统、泛型、装饰器等高级特性',
      category: 'programming-course',
      link: '#',
      price: '¥249',
      author: '王老师',
      tags: ['TypeScript', '类型系统']
    }
  ],
  'music-course': [
    {
      id: 'mc-1',
      title: '钢琴基础入门课程',
      description: '适合零基础学员，系统学习钢琴演奏技巧',
      category: 'music-course',
      link: '#',
      price: '¥399',
      author: '陈老师',
      tags: ['钢琴', '入门', '基础']
    },
    {
      id: 'mc-2',
      title: '吉他弹唱速成班',
      description: '快速掌握吉他弹唱技巧，30天学会弹唱',
      category: 'music-course',
      link: '#',
      price: '¥299',
      author: '刘老师',
      tags: ['吉他', '弹唱', '速成']
    },
    {
      id: 'mc-3',
      title: '声乐训练课程',
      description: '专业声乐训练，提升歌唱技巧和音准',
      category: 'music-course',
      link: '#',
      price: '¥499',
      author: '赵老师',
      tags: ['声乐', '训练', '专业']
    }
  ],
  'music-album': [
    {
      id: 'ma-1',
      title: '经典流行音乐合集',
      description: '收录近十年经典流行歌曲，高品质无损音质',
      category: 'music-album',
      link: '#',
      author: 'Various Artists',
      tags: ['流行', '经典', '合集']
    },
    {
      id: 'ma-2',
      title: '轻音乐精选',
      description: '舒缓的轻音乐，适合工作、学习时聆听',
      category: 'music-album',
      link: '#',
      author: 'Various Artists',
      tags: ['轻音乐', '放松', '工作']
    },
    {
      id: 'ma-3',
      title: '古典音乐大师作品集',
      description: '贝多芬、莫扎特等大师经典作品',
      category: 'music-album',
      link: '#',
      author: 'Various Artists',
      tags: ['古典', '大师', '经典']
    }
  ],
  'books': [
    {
      id: 'book-1',
      title: 'JavaScript 高级程序设计（第4版）',
      description: '前端开发必读经典，深入理解 JavaScript 语言特性',
      category: 'books',
      link: '#',
      price: '¥89',
      author: 'Matt Frisbie',
      tags: ['JavaScript', '编程', '前端']
    },
    {
      id: 'book-2',
      title: '深入理解计算机系统',
      description: '计算机科学经典教材，理解系统底层原理',
      category: 'books',
      link: '#',
      price: '¥139',
      author: 'Randal E. Bryant',
      tags: ['计算机', '系统', '底层']
    },
    {
      id: 'book-3',
      title: '设计模式：可复用面向对象软件的基础',
      description: '软件设计模式经典著作',
      category: 'books',
      link: '#',
      price: '¥59',
      author: 'Gang of Four',
      tags: ['设计模式', '软件工程']
    },
    {
      id: 'book-4',
      title: '二手：Vue.js 权威指南',
      description: '九成新，Vue.js 学习参考书',
      category: 'books',
      link: '#',
      price: '¥45',
      author: '尤雨溪',
      tags: ['Vue', '二手', '前端']
    }
  ],
  'agricultural-product': [
    {
      id: 'ap-1',
      title: '有机大米 5kg',
      description: '来自东北的优质有机大米，绿色健康',
      category: 'agricultural-product',
      link: 'https://s.taobao.com/search?q=有机大米',
      price: '¥68',
      isExternal: true,
      tags: ['大米', '有机', '东北']
    },
    {
      id: 'ap-2',
      title: '新鲜苹果 10斤装',
      description: '山东烟台红富士，脆甜多汁',
      category: 'agricultural-product',
      link: 'https://s.taobao.com/search?q=烟台苹果',
      price: '¥39.9',
      isExternal: true,
      tags: ['苹果', '新鲜', '烟台']
    },
    {
      id: 'ap-3',
      title: '农家土鸡蛋 30枚',
      description: '散养土鸡蛋，营养丰富',
      category: 'agricultural-product',
      link: 'https://s.taobao.com/search?q=土鸡蛋',
      price: '¥45',
      isExternal: true,
      tags: ['鸡蛋', '土鸡蛋', '农家']
    },
    {
      id: 'ap-4',
      title: '有机蔬菜礼盒',
      description: '多种有机蔬菜组合，健康营养',
      category: 'agricultural-product',
      link: 'https://s.taobao.com/search?q=有机蔬菜',
      price: '¥88',
      isExternal: true,
      tags: ['蔬菜', '有机', '礼盒']
    }
  ]
}

