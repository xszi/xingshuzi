# 登录和后台管理功能说明

## 功能概述

本项目实现了完整的用户登录和后台管理系统，包括：

1. **用户登录/注册**
2. **普通用户和管理员角色区分**
3. **管理员后台入口（仅管理员可见）**
4. **后台管理系统**，包含各资源分类的增删改查功能

## 核心文件结构

```
app/
├── composables/
│   └── useAuth.ts                    # 用户认证 composable
├── utils/
│   └── api.ts                        # 带 Token 的 API 请求工具
├── pages/
│   ├── login.vue                     # 登录/注册页面
│   └── admin/
│       ├── index.vue                 # 后台首页
│       ├── programming-courses.vue   # 编程课程管理
│       ├── music-courses.vue         # 音乐课程管理
│       ├── music-albums.vue          # 音乐专辑管理
│       ├── books.vue                 # 书籍管理
│       └── agricultural-products.vue # 助农产品管理
├── layouts/
│   ├── default.vue                   # 前台布局（已添加登录入口）
│   └── admin.vue                     # 后台管理布局
└── components/
    └── admin/
        ├── DataTable.vue             # 通用数据表格组件
        └── FormModal.vue             # 通用表单弹窗组件
```

## 功能详解

### 1. 用户登录流程

#### 登录接口

**请求：**
```javascript
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin123",
  "password": "admin123"
}
```

**响应：**
```javascript
{
  "code": 200,
  "msg": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "username": "admin123",
      "role": "admin"  // 或 "user"
    }
  }
}
```

#### 前端实现

`app/composables/useAuth.ts` 提供了以下方法：

```typescript
const { 
  user,          // 当前用户信息
  token,         // 当前 token
  isLoggedIn,    // 是否已登录
  isAdmin,       // 是否是管理员
  login,         // 登录方法
  register,      // 注册方法
  logout         // 登出方法
} = useAuth()
```

**使用示例：**

```vue
<script setup>
const { login } = useAuth()

const handleLogin = async () => {
  const result = await login('admin123', 'admin123')
  if (result.success) {
    // 登录成功，跳转
    navigateTo('/')
  } else {
    // 显示错误信息
    alert(result.message)
  }
}
</script>
```

### 2. 判断是否是管理员后台入口

在 `app/layouts/default.vue` 中，使用 `v-if="isAdmin"` 来控制后台管理入口的显示：

```vue
<template>
  <!-- 只有管理员才能看到这个链接 -->
  <NuxtLink v-if="isAdmin" to="/admin" class="nav-link admin-link">
    后台管理
  </NuxtLink>
  
  <!-- 用户状态 -->
  <div class="user-section">
    <NuxtLink v-if="!isLoggedIn" to="/login" class="nav-link login-btn">
      登录
    </NuxtLink>
    <div v-else class="user-menu">
      <span class="user-name">{{ user?.username }}</span>
      <button @click="handleLogout" class="logout-btn">退出</button>
    </div>
  </div>
</template>

<script setup>
const { user, isLoggedIn, isAdmin, logout } = useAuth()
</script>
```

### 3. 调用管理接口时带上 Token

`app/utils/api.ts` 提供了自动带 Token 的 API 请求工具：

```typescript
// 自动从 localStorage 读取 token 并添加到请求头
import { api } from '~/utils/api'

// GET 请求
const data = await api.get('/courses/programming/list')

// POST 请求
await api.post('/courses/programming', {
  title: '新课程',
  description: '课程描述',
  author: '作者',
  price: '99'
})

// PUT 请求
await api.put('/courses/programming/123', {
  title: '更新后的标题'
})

// DELETE 请求
await api.delete('/courses/programming/123')
```

**请求头格式：**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**401 处理：**
如果后端返回 401 未授权，`api.ts` 会自动清除登录信息并跳转到登录页。

## 后台管理功能

### 后台首页

访问 `/admin` 可以看到：
- 各资源分类的统计卡片
- 欢迎信息

### 各分类管理页面

每个分类管理页面提供：

1. **数据列表展示**（表格形式）
2. **添加功能**（点击"添加"按钮）
3. **编辑功能**（点击"编辑"按钮）
4. **删除功能**（点击"删除"按钮，有二次确认）

### 后端 API 接口要求

#### 编程课程

- `GET /api/courses/admin/list?category=programming` - 获取列表（需要 Token）
- `POST /api/courses/admin` - 添加（需要 Token + admin 权限）
- `GET /api/courses/admin/:id` - 获取单个（需要 Token）
- `PUT /api/courses/admin/:id` - 更新（需要 Token + admin 权限）
- `DELETE /api/courses/admin/:id` - 删除（需要 Token + admin 权限）

#### 音乐课程

- `GET /api/courses/admin/list?category=music` - 获取列表
- `POST /api/courses/admin` - 添加（category: 'music'）
- `GET /api/courses/admin/:id` - 获取单个
- `PUT /api/courses/admin/:id` - 更新
- `DELETE /api/courses/admin/:id` - 删除

#### 音乐专辑

- `GET /api/music/albums/admin/list` - 获取列表
- `POST /api/music/albums/admin` - 添加
- `PUT /api/music/albums/admin/:id` - 更新
- `DELETE /api/music/albums/admin/:id` - 删除

#### 各类书籍

- `GET /api/books/admin/list` - 获取列表
- `POST /api/books/admin` - 添加
- `PUT /api/books/admin/:id` - 更新
- `DELETE /api/books/admin/:id` - 删除

#### 助农产品

- `GET /api/products/agriculture` - 获取列表
- `POST /api/products/agriculture/admin` - 添加
- `PUT /api/products/agriculture/admin/:id` - 更新
- `DELETE /api/products/agriculture/admin/:id` - 删除

### 请求/响应格式

**POST/PUT 请求体：**

课程（编程/音乐）：
```json
{
  "title": "标题",
  "description": "描述",
  "author": "作者",
  "price": "99",
  "link": "https://example.com",
  "cover_url": "https://example.com/image.jpg",
  "tags": ["标签1", "标签2"],
  "category": "programming" // 或 "music"
}
```

其他资源：
```json
{
  "title": "标题",
  "description": "描述",
  "author": "作者",
  "price": "99",
  "link": "https://example.com",
  "cover_url": "https://example.com/image.jpg",
  "tags": ["标签1", "标签2"],
  "category": "album" // 或 "books", "agriculture"
}
```

**响应格式：**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": { ... }
}
```

## 环境配置

在 `.env` 文件中配置后端 API 地址：

```bash
# 后端 API 地址
NUXT_PUBLIC_API_BASE=http://127.0.0.1:5000/api

# 生产环境
# NUXT_PUBLIC_API_BASE=https://api.xingshuzi.com/api
```

## 安全注意事项

1. **Token 存储**：Token 存储在 `localStorage` 中
2. **权限验证**：
   - 前端：`app/layouts/admin.vue` 会检查用户是否是管理员
   - 后端：必须验证 Token 和用户权限
3. **HTTPS**：生产环境必须使用 HTTPS
4. **Token 过期**：后端应该实现 Token 过期机制

## 使用流程

### 普通用户

1. 访问网站首页
2. 点击右上角"登录"按钮
3. 输入用户名和密码
4. 登录成功后可以浏览资源

### 管理员

1. 使用管理员账号登录
2. 登录后右上角会显示"后台管理"入口
3. 点击进入后台管理系统
4. 在左侧菜单选择要管理的分类
5. 进行增删改查操作

## 测试账号

请在后端数据库中创建测试账号：

```sql
-- 管理员账号
username: admin123
password: admin123
role: admin

-- 普通用户账号
username: user123
password: user123
role: user
```

## 开发调试

```bash
# 启动开发服务器
npm run dev

# 访问前台
http://localhost:3000

# 访问登录页
http://localhost:3000/login

# 访问后台（需要先登录管理员账号）
http://localhost:3000/admin
```

## 部署说明

部署时注意：

1. 配置正确的 `NUXT_PUBLIC_API_BASE` 环境变量
2. 确保后端 API 已部署并可访问
3. 配置 CORS（如果前后端分离）
4. 使用 HTTPS（生产环境必须）

