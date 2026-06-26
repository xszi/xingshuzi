# xingshuzi-back API 文档

## 认证接口

所有后台管理接口需要在请求头中携带 JWT Token：
```
Authorization: Bearer <your_jwt_token>
```

### 1. 用户注册
**POST** `/api/auth/register`

请求体：
```json
{
  "username": "testuser",
  "password": "password123",
  "email": "test@example.com",
  "role": "user"  // 可选，默认为 "user"
}
```

响应：
```json
{
  "code": 200,
  "msg": "User registered successfully",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "role": "user",
    "created_at": "2025-12-24 12:00:00"
  }
}
```

### 2. 用户登录
**POST** `/api/auth/login`

请求体：
```json
{
  "username": "admin",
  "password": "admin123"
}
```

响应：
```json
{
  "code": 200,
  "msg": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@xingshuzi.com",
      "role": "admin",
      "created_at": "2025-12-24 12:00:00"
    }
  }
}
```

### 3. 获取当前用户信息
**GET** `/api/auth/me`

需要 Token，响应：
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@xingshuzi.com",
    "role": "admin",
    "created_at": "2025-12-24 12:00:00"
  }
}
```

---

## 前台接口（公开访问）

### 首页
**GET** `/api/home/banners` - 获取轮播图列表
**GET** `/api/home/featured` - 获取推荐内容

### 编程课程
**GET** `/api/courses/programming?page=1&limit=10` - 获取编程课程列表

### 音乐课程
**GET** `/api/courses/music?page=1&limit=10` - 获取音乐课程列表

### 音乐专辑
**GET** `/api/music/albums?page=1&limit=10` - 获取音乐专辑列表

### 书籍
**GET** `/api/books/list?page=1&limit=10&category=xxx` - 获取书籍列表（可选 category 参数）

### 助农产品
**GET** `/api/products/agriculture?page=1&limit=10` - 获取助农产品列表

---

## 后台管理接口（需要管理员权限）

所有后台接口都需要在请求头中携带 `Authorization: Bearer <token>`，且用户角色必须为 `admin`。

### 编程/音乐课程管理

#### 获取所有课程
**GET** `/api/courses/admin/list?page=1&limit=10&category=programming`

参数：
- `page`: 页码（可选，默认1）
- `limit`: 每页数量（可选，默认10）
- `category`: 类别过滤（可选，programming/music）

#### 创建课程
**POST** `/api/courses/admin`

请求体：
```json
{
  "title": "Python 入门教程",
  "description": "适合零基础学员",
  "category": "programming",
  "cover_image": "http://example.com/image.jpg",
  "price": 99.00
}
```

#### 获取单个课程
**GET** `/api/courses/admin/:id`

#### 更新课程
**PUT** `/api/courses/admin/:id`

请求体（所有字段可选）：
```json
{
  "title": "Python 进阶教程",
  "description": "适合有基础的学员",
  "category": "programming",
  "cover_image": "http://example.com/new-image.jpg",
  "price": 199.00
}
```

#### 删除课程
**DELETE** `/api/courses/admin/:id`

---

### 音乐专辑管理

#### 获取所有专辑
**GET** `/api/music/admin/list?page=1&limit=10`

#### 创建专辑
**POST** `/api/music/admin`

请求体：
```json
{
  "title": "夜的钢琴曲",
  "artist": "石进",
  "description": "优美的钢琴音乐",
  "cover_image": "http://example.com/album.jpg",
  "release_date": "2010-06-01"
}
```

#### 获取单个专辑
**GET** `/api/music/admin/:id`

#### 更新专辑
**PUT** `/api/music/admin/:id`

#### 删除专辑
**DELETE** `/api/music/admin/:id`

---

### 书籍管理

#### 获取所有书籍
**GET** `/api/books/admin/list?page=1&limit=10&category=xxx`

#### 创建书籍
**POST** `/api/books/admin`

请求体：
```json
{
  "title": "活着",
  "author": "余华",
  "category": "文学",
  "description": "一部经典文学作品",
  "cover_image": "http://example.com/book.jpg",
  "price": 35.00
}
```

#### 获取单个书籍
**GET** `/api/books/admin/:id`

#### 更新书籍
**PUT** `/api/books/admin/:id`

#### 删除书籍
**DELETE** `/api/books/admin/:id`

---

### 助农产品管理

#### 获取所有产品
**GET** `/api/products/admin/list?page=1&limit=10&category=agriculture`

#### 创建产品
**POST** `/api/products/admin`

请求体：
```json
{
  "name": "有机苹果",
  "description": "来自山区的新鲜有机苹果",
  "category": "agriculture",
  "origin": "陕西洛川",
  "price": 12.00,
  "image_url": "http://example.com/apple.jpg"
}
```

#### 获取单个产品
**GET** `/api/products/admin/:id`

#### 更新产品
**PUT** `/api/products/admin/:id`

#### 删除产品
**DELETE** `/api/products/admin/:id`

---

### 首页轮播图管理

#### 获取所有轮播图
**GET** `/api/home/admin/banners?page=1&limit=10`

#### 创建轮播图
**POST** `/api/home/admin/banners`

请求体：
```json
{
  "title": "新年活动",
  "image_url": "http://example.com/banner.jpg",
  "link_url": "http://example.com/activity",
  "sort_order": 1
}
```

#### 获取单个轮播图
**GET** `/api/home/admin/banners/:id`

#### 更新轮播图
**PUT** `/api/home/admin/banners/:id`

#### 删除轮播图
**DELETE** `/api/home/admin/banners/:id`

---

## 错误码说明

- `200`: 成功
- `400`: 请求参数错误
- `401`: 未授权（登录失败或 Token 无效）
- `403`: 权限不足（需要管理员权限）
- `404`: 资源不存在

## 默认管理员账号

- 用户名：`admin`
- 密码：`admin123`

**请在首次登录后修改密码！**


