# xingshuzi-back 后端项目

基于 Flask 开发的星书子项目后端 API 服务，提供用户认证、内容管理等功能。

## 技术栈

- **Python 3.x**
- **Flask** - Web 框架
- **Flask-SQLAlchemy** - ORM
- **Flask-JWT-Extended** - JWT 认证
- **Flask-CORS** - 跨域支持
- **PyMySQL** - MySQL 数据库驱动
- **MySQL** - 数据库

## 项目结构

```
xingshuzi-back/
├── app/
│   ├── __init__.py           # 应用初始化
│   ├── models/               # 数据模型
│   │   ├── user.py          # 用户模型
│   │   ├── course.py        # 课程模型
│   │   ├── music.py         # 音乐专辑模型
│   │   ├── book.py          # 书籍模型
│   │   ├── product.py       # 产品模型
│   │   └── home.py          # 首页模型
│   ├── routes/              # 路由控制器
│   │   ├── auth.py          # 认证相关
│   │   ├── courses.py       # 课程管理
│   │   ├── music.py         # 音乐管理
│   │   ├── books.py         # 书籍管理
│   │   ├── products.py      # 产品管理
│   │   └── home.py          # 首页管理
│   └── utils/
│       └── auth.py          # 权限验证装饰器
├── config/
│   └── config.py            # 配置文件
├── run.py                   # 启动文件
├── init_admin.py            # 初始化管理员脚本
├── requirements.txt         # 依赖列表
├── API.md                   # API 文档
└── README.md               # 项目说明
```

## 功能模块

### 1. 用户认证系统
- 用户注册/登录
- JWT Token 认证
- 角色权限控制（普通用户/管理员）

### 2. 内容管理
- **编程课程管理**：增删改查
- **音乐课程管理**：增删改查
- **音乐专辑管理**：增删改查
- **各类书籍管理**：增删改查
- **助农产品管理**：增删改查
- **首页轮播图管理**：增删改查

### 3. 公开接口
- 各类内容的列表展示
- 支持分页和分类筛选

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

如果遇到网络问题，可以使用国内镜像源：
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 2. 配置数据库

在项目根目录创建 `.env` 文件，配置数据库连接信息：

```ini
MYSQL_USER=jhadmin
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=xingshuzi
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

### 3. 创建数据库

在 MySQL 中执行：
```sql
CREATE DATABASE xingshuzi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 初始化数据库表

```bash
python -c "from run import app, db; from app.models.user import User; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### 5. 创建管理员账号

```bash
python init_admin.py
```

默认管理员账号：
- 用户名：`admin`
- 密码：`admin123`

**重要：首次登录后请立即修改密码！**

### 6. 启动服务

```bash
python run.py
```

服务将运行在 `http://127.0.0.1:5000`

## API 使用

详细 API 文档请参考 [API.md](./API.md)

### 快速测试

#### 1. 测试登录接口
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

#### 2. 使用返回的 Token 访问管理接口
```bash
curl -X GET http://127.0.0.1:5000/api/courses/admin/list \
  -H "Authorization: Bearer <your_token_here>"
```

## 前后端对接说明

### 前端用户界面实现要点

1. **用户登录后存储 Token**
   ```javascript
   // 登录成功后
   localStorage.setItem('token', response.data.token);
   localStorage.setItem('user', JSON.stringify(response.data.user));
   ```

2. **判断是否显示后台管理入口**
   ```javascript
   const user = JSON.parse(localStorage.getItem('user'));
   if (user && user.role === 'admin') {
     // 显示后台管理入口
   }
   ```

3. **请求时携带 Token**
   ```javascript
   const token = localStorage.getItem('token');
   fetch('/api/courses/admin/list', {
     headers: {
       'Authorization': `Bearer ${token}`,
       'Content-Type': 'application/json'
     }
   });
   ```

4. **后台管理页面路由结构建议**
   ```
   /admin
     /admin/courses          # 课程管理（编程+音乐）
     /admin/albums           # 音乐专辑管理
     /admin/books            # 书籍管理
     /admin/products         # 助农产品管理
     /admin/banners          # 首页轮播图管理
   ```

## 开发注意事项

1. **CORS 配置**：项目已启用 CORS，允许跨域访问
2. **调试模式**：生产环境请关闭 Debug 模式
3. **密码安全**：使用了 werkzeug 的密码哈希，确保安全
4. **Token 过期时间**：默认 24 小时，可在 config.py 中修改

## 数据库表结构

- `users` - 用户表
- `courses` - 课程表（包含编程和音乐课程）
- `music_albums` - 音乐专辑表
- `books` - 书籍表
- `products` - 产品表（助农产品等）
- `home_banners` - 首页轮播图表

## 常见问题

### 1. 连接数据库失败
- 检查 `.env` 文件中的数据库配置是否正确
- 确认 MySQL 服务已启动
- 确认数据库 `xingshuzi` 已创建

### 2. Token 认证失败
- 检查请求头中是否正确携带 `Authorization: Bearer <token>`
- Token 可能已过期，需要重新登录

### 3. 权限不足 (403 错误)
- 确认当前用户角色为 `admin`
- 部分接口仅管理员可访问

## License

MIT License
