# xingshuzi-back

基于 Flask 开发的星书子项目后端 API 服务，提供用户认证、内容管理等功能。

## 🚀 快速开始（Docker 部署）

### 前提条件

- 阿里云 ECS Ubuntu 服务器
- 已安装 Docker 和 Docker Compose

### 一键部署

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd xingshuzi-back

# 2. 运行部署脚本
chmod +x deploy.sh
sudo ./deploy.sh
```

### 手动部署

```bash
# 1. 创建环境变量文件
cat > .env << 'EOF'
MYSQL_USER=root
MYSQL_PASSWORD=MyStrongRootPassword123
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DB=xingshuzi
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
EOF

# 2. 启动服务
docker compose up -d

# 3. 等待 30 秒后初始化数据库
sleep 30
docker compose exec app python3 -c "from app import create_app, db; from app.models.user import User; app = create_app(); app.app_context().push(); db.create_all()"
docker compose exec app python3 init_admin.py

# 4. 验证部署
curl http://localhost:5000/api/home/banners
```

## 📋 技术栈

- **Python 3.11** - 编程语言
- **Flask** - Web 框架
- **MySQL 8.0** - 数据库
- **Flask-SQLAlchemy** - ORM
- **Flask-JWT-Extended** - JWT 认证
- **Docker** - 容器化部署

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| MYSQL_USER | MySQL 用户名 | root |
| MYSQL_PASSWORD | MySQL 密码 | MyStrongRootPassword123 |
| MYSQL_HOST | MySQL 主机 | mysql |
| MYSQL_PORT | MySQL 端口 | 3306 |
| MYSQL_DB | 数据库名 | xingshuzi |
| SECRET_KEY | Flask 密钥 | - |
| JWT_SECRET_KEY | JWT 密钥 | - |

## 🎯 默认账号

- **用户名**: `admin`
- **密码**: `admin123`

⚠️ **请在首次登录后立即修改密码！**

## 📚 API 文档

详细 API 文档请参考 [API.md](./API.md)

### 主要接口

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/home/banners` - 获取首页轮播图
- `GET /api/courses/programming` - 获取编程课程
- `GET /api/music/albums` - 获取音乐专辑
- `GET /api/books/list` - 获取书籍列表
- `GET /api/products/agriculture` - 获取助农产品

### 后台管理接口（需要管理员权限）

- `GET /api/courses/admin/list` - 课程管理
- `GET /api/music/admin/list` - 音乐专辑管理
- `GET /api/books/admin/list` - 书籍管理
- `GET /api/products/admin/list` - 产品管理
- `GET /api/home/admin/banners` - 轮播图管理

## 🛠️ 常用命令

### Docker 管理

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
docker compose logs -f app    # 只查看应用日志

# 启动/停止/重启服务
docker compose start
docker compose stop
docker compose restart

# 重新构建
docker compose build
docker compose up -d
```

### 数据库管理

```bash
# 备份数据库
docker compose exec mysql mysqldump -u root -pMyStrongRootPassword123 xingshuzi > backup.sql

# 恢复数据库
docker compose exec -T mysql mysql -u root -pMyStrongRootPassword123 xingshuzi < backup.sql

# 进入 MySQL 容器
docker compose exec mysql mysql -u root -pMyStrongRootPassword123
```

### 应用管理

```bash
# 进入应用容器
docker compose exec app bash

# 重置管理员密码
docker compose exec app python3 << 'EOF'
from app import create_app, db
from app.models.user import User
app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    admin.set_password('新密码')
    db.session.commit()
    print('密码已重置')
EOF

# 创建示例数据
docker compose exec app python3 create_sample_data.py
```

## 📖 部署文档

详细部署文档请参考 [DEPLOY.md](./DEPLOY.md)

## 🔒 安全建议

1. ✅ 修改默认管理员密码
2. ✅ 修改 SECRET_KEY 和 JWT_SECRET_KEY
3. ✅ 配置防火墙和安全组规则
4. ✅ 使用 Nginx 反向代理
5. ✅ 配置 HTTPS
6. ✅ 定期备份数据库
7. ✅ 定期更新系统和依赖

## 📁 项目结构

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
│       └── auth.py          # 权限验证
├── config/
│   └── config.py            # 配置文件
├── Dockerfile               # Docker 镜像定义
├── docker-compose.yml       # Docker Compose 配置
├── requirements.txt         # Python 依赖
├── run.py                   # 应用入口
├── init_admin.py           # 初始化管理员
├── create_sample_data.py   # 创建示例数据
├── deploy.sh               # 一键部署脚本
├── API.md                  # API 文档
├── DEPLOY.md               # 部署文档
└── README.md               # 项目说明
```

## 🐛 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker compose logs app
docker compose logs mysql

# 重新构建
docker compose build --no-cache
docker compose up -d
```

### 数据库连接失败

```bash
# 检查 MySQL 容器状态
docker compose ps mysql

# 测试数据库连接
docker compose exec mysql mysql -u root -pMyStrongRootPassword123 -e "SHOW DATABASES;"
```

### 端口被占用

```bash
# 查看端口占用
netstat -tlnp | grep 5000

# 修改 docker-compose.yml 中的端口映射
# 例如：将 "5000:5000" 改为 "8000:5000"
```

## 📝 更新日志

### v1.0.0 (2025-12-24)

- ✅ 初始版本发布
- ✅ 实现用户认证系统
- ✅ 实现内容管理 CRUD 接口
- ✅ Docker 容器化部署
- ✅ 完善 API 文档

## 📄 License

MIT License

## 👥 联系方式

如有问题，请通过以下方式联系：

- 提交 Issue
- 发送邮件

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**
