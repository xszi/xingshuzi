# MySQL部署方案选择指南

本文档帮助您快速选择适合的MySQL部署方案。

## 📊 三种部署方案对比

| 方案 | 适用场景 | 优点 | 缺点 | 推荐指数 |
|------|---------|------|------|---------|
| **方案一：使用已有线上MySQL** | 已有MySQL服务 | 简单、无需额外部署 | 依赖外部服务 | ⭐⭐⭐ |
| **方案二：独立部署MySQL容器** | 生产环境 | 易管理、易备份、安全 | 需要单独管理 | ⭐⭐⭐⭐⭐ |
| **方案三：Server+MySQL一体化** | 开发测试 | 一键部署、简单快捷 | 扩展性有限 | ⭐⭐⭐⭐ |

---

## 🎯 方案一：使用已有线上MySQL（当前方案）

### 适用场景
- ✅ 已有MySQL服务器
- ✅ 多个应用共享数据库
- ✅ 需要独立管理数据库

### 配置方式

后端 `.env` 文件：
```env
MYSQL_HOST=120.76.247.123
MYSQL_PORT=3306
MYSQL_DB=xingshuzi
MYSQL_USER=root
MYSQL_PASSWORD=MyStrongRootPassword123
```

### 部署步骤

```bash
# 1. 确保MySQL可访问
mysql -h 120.76.247.123 -P 3306 -uroot -pMyStrongRootPassword123

# 2. 部署后端
cd /root/xingshuzi/server
./deploy.sh

# 3. 初始化数据库
docker exec xingshuzi-api python3 create_db.py
docker exec xingshuzi-api python3 init_admin.py
```

### 优缺点
✅ 无需额外部署  
✅ 数据独立，不受容器影响  
❌ 依赖外部网络  
❌ 需要单独管理MySQL服务器

---

## 🎯 方案二：独立部署MySQL容器（推荐生产环境）

### 适用场景
- ✅ 生产环境部署
- ✅ 需要完全容器化
- ✅ 需要数据持久化和备份
- ✅ 需要独立管理数据库

### 文件位置
```
xingshuzi/mysql-standalone/
├── docker-compose.yml    # Docker配置
├── my.cnf               # MySQL配置
├── init.sql             # 初始化脚本
├── deploy.sh            # 部署脚本
├── backup.sh            # 备份脚本
└── README.md            # 说明文档
```

### 部署步骤

```bash
# 1. 上传配置文件到ECS（通过Git）
cd /root
git clone git@github.com:your-username/xingshuzi.git
cd xingshuzi/mysql-standalone

# 2. 部署MySQL
chmod +x deploy.sh
./deploy.sh

# 3. 验证MySQL
docker ps | grep xingshuzi-mysql
docker compose exec mysql mysql -uroot -pMyStrongRootPassword123

# 4. 修改后端配置连接Docker MySQL
cd /root/xingshuzi/server
nano .env
# 设置: MYSQL_HOST=120.76.247.123 (或 localhost)

# 5. 部署后端
./deploy.sh

# 6. 初始化数据库
docker exec xingshuzi-api python3 create_db.py
docker exec xingshuzi-api python3 init_admin.py
```

### 架构图

```
ECS (120.76.247.123)
│
├── MySQL容器 (端口 3306)
│   └── 数据卷: mysql_data (持久化)
│
└── API容器 (端口 5001)
    └── 连接: 120.76.247.123:3306
```

### 优缺点
✅ 完全容器化，易于迁移  
✅ 数据持久化，易于备份  
✅ 独立管理，互不影响  
✅ 安全可控  
❌ 需要分别管理两个服务

### 管理命令

```bash
# MySQL管理
cd /root/xingshuzi/mysql-standalone
docker compose logs -f mysql          # 查看日志
docker compose restart mysql          # 重启
./backup.sh                           # 备份

# 后端管理
cd /root/xingshuzi/server
docker compose logs -f api            # 查看日志
docker compose restart api            # 重启
```

---

## 🎯 方案三：Server + MySQL 一体化部署

### 适用场景
- ✅ 开发测试环境
- ✅ 快速部署需求
- ✅ 小型项目
- ✅ 单机部署

### 文件位置
```
xingshuzi/server/
├── docker-compose.with-mysql.yml    # 一体化配置
├── deploy-with-mysql.sh             # 一键部署脚本
└── README_WITH_MYSQL.md             # 说明文档
```

### 部署步骤

```bash
# 1. 进入server目录
cd /root/xingshuzi/server

# 2. 一键部署（包含MySQL和API）
chmod +x deploy-with-mysql.sh
./deploy-with-mysql.sh

# 3. 初始化数据库
docker exec xingshuzi-api python3 create_db.py
docker exec xingshuzi-api python3 init_admin.py

# 4. 验证
curl http://localhost:5001/api/home/banners
```

### 架构图

```
Docker Network: xingshuzi-network
│
├── MySQL容器 (内部端口 3306)
│   └── 数据卷: mysql_data
│
└── API容器 (外部端口 5001)
    └── 连接: mysql:3306 (通过Docker网络)
```

### 优缺点
✅ 一键部署，超级简单  
✅ 服务间网络通信快  
✅ 统一管理，方便维护  
❌ 扩展性有限  
❌ 重启后端可能影响数据库（实际上不会，但感觉上容易混淆）

### 管理命令

```bash
cd /root/xingshuzi/server

# 统一管理
docker compose -f docker-compose.with-mysql.yml logs -f   # 查看日志
docker compose -f docker-compose.with-mysql.yml restart   # 重启所有
docker compose -f docker-compose.with-mysql.yml down      # 停止所有

# 单独管理
docker compose -f docker-compose.with-mysql.yml restart mysql  # 只重启MySQL
docker compose -f docker-compose.with-mysql.yml restart api    # 只重启API

# 备份
docker exec xingshuzi-mysql mysqldump -uroot -pMyStrongRootPassword123 xingshuzi > backup.sql
```

---

## 🤔 如何选择？

### 快速决策树

```
开始
  │
  ├─ 已有MySQL服务器？
  │   └─ 是 → 方案一（使用已有MySQL）
  │
  ├─ 是生产环境？
  │   └─ 是 → 方案二（独立部署MySQL容器）⭐推荐
  │
  └─ 开发测试/快速部署？
      └─ 是 → 方案三（一体化部署）
```

### 详细建议

**选择方案一（使用已有MySQL）：**
- 已经有稳定的MySQL服务器
- 多个应用共享同一数据库
- 不想增加额外的容器管理

**选择方案二（独立MySQL容器）：**
- 生产环境部署 ⭐
- 需要数据隔离和安全性
- 需要方便的备份和恢复
- 希望完全容器化
- 可能需要扩展到多台服务器

**选择方案三（一体化部署）：**
- 开发测试环境
- 快速原型验证
- 小型项目
- 追求部署简单快捷

---

## 📖 详细文档索引

### 主文档
- **`MYSQL_DOCKER_DEPLOY.md`** - MySQL Docker部署完整指南（15KB）
  - 三种方案的详细说明
  - 数据库管理、备份恢复
  - 性能优化、故障排查
  - 安全建议

### 方案二：独立部署
- **`mysql-standalone/README.md`** - 独立部署快速指南
- **`mysql-standalone/docker-compose.yml`** - Docker配置
- **`mysql-standalone/deploy.sh`** - 一键部署脚本
- **`mysql-standalone/backup.sh`** - 备份脚本

### 方案三：一体化部署
- **`server/README_WITH_MYSQL.md`** - 一体化部署指南
- **`server/docker-compose.with-mysql.yml`** - 一体化配置
- **`server/deploy-with-mysql.sh`** - 一键部署脚本

---

## ✅ 快速上手

### 我想用独立MySQL容器（推荐）

```bash
# 1. 推送代码到Git（本地）
git add .
git commit -m "添加MySQL Docker部署配置"
git push origin main

# 2. 在ECS上部署MySQL
ssh root@120.76.247.123
cd /root/xingshuzi/mysql-standalone
./deploy.sh

# 3. 修改后端配置
cd /root/xingshuzi/server
nano .env  # 设置 MYSQL_HOST=120.76.247.123

# 4. 部署后端
./deploy.sh

# 5. 初始化
docker exec xingshuzi-api python3 create_db.py
docker exec xingshuzi-api python3 init_admin.py
```

### 我想一键部署全部

```bash
# 在ECS上执行
ssh root@120.76.247.123
cd /root/xingshuzi/server
./deploy-with-mysql.sh

# 初始化
docker exec xingshuzi-api python3 create_db.py
docker exec xingshuzi-api python3 init_admin.py
```

---

## 🔄 方案迁移

### 从方案一迁移到方案二

```bash
# 1. 备份现有数据
mysqldump -h 120.76.247.123 -uroot -pMyStrongRootPassword123 xingshuzi > backup.sql

# 2. 部署Docker MySQL
cd /root/xingshuzi/mysql-standalone
./deploy.sh

# 3. 导入数据
docker exec -i xingshuzi-mysql mysql -uroot -pMyStrongRootPassword123 xingshuzi < backup.sql

# 4. 修改后端配置连接Docker MySQL
cd /root/xingshuzi/server
nano .env  # 修改 MYSQL_HOST

# 5. 重启后端
docker compose restart
```

### 从方案三切换到方案二

```bash
# 1. 备份数据
docker exec xingshuzi-mysql mysqldump -uroot -pMyStrongRootPassword123 xingshuzi > backup.sql

# 2. 停止一体化部署
cd /root/xingshuzi/server
docker compose -f docker-compose.with-mysql.yml down

# 3. 部署独立MySQL
cd /root/xingshuzi/mysql-standalone
./deploy.sh

# 4. 导入数据
docker exec -i xingshuzi-mysql mysql -uroot -pMyStrongRootPassword123 xingshuzi < backup.sql

# 5. 修改后端配置
cd /root/xingshuzi/server
nano .env

# 6. 使用原来的部署方式
./deploy.sh
```

---

## 💡 最佳实践建议

### 生产环境推荐配置

1. **使用独立MySQL容器**（方案二）
2. **修改默认密码**为强密码
3. **创建应用专用账号**（不使用root）
4. **配置定时备份**
5. **监控数据库性能**
6. **定期更新Docker镜像**

### 完整生产环境部署流程

```bash
# 1. 部署独立MySQL
cd /root/xingshuzi/mysql-standalone
./deploy.sh

# 2. 创建应用专用账号
docker compose exec mysql mysql -uroot -pMyStrongRootPassword123 << EOF
CREATE USER 'app_user'@'%' IDENTIFIED BY 'StrongAppPassword456';
GRANT SELECT, INSERT, UPDATE, DELETE ON xingshuzi.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
EOF

# 3. 配置后端使用应用账号
cd /root/xingshuzi/server
cat > .env << EOF
MYSQL_HOST=120.76.247.123
MYSQL_USER=app_user
MYSQL_PASSWORD=StrongAppPassword456
MYSQL_DB=xingshuzi
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
EOF

# 4. 部署后端
./deploy.sh

# 5. 初始化数据库
docker exec xingshuzi-api python3 create_db.py
docker exec xingshuzi-api python3 init_admin.py

# 6. 配置定时备份
chmod +x /root/xingshuzi/mysql-standalone/backup.sh
crontab -e
# 添加: 0 2 * * * /root/xingshuzi/mysql-standalone/backup.sh
```

---

## 📞 获取帮助

遇到问题？查看以下文档：
- `MYSQL_DOCKER_DEPLOY.md` - 完整部署指南和故障排查
- `mysql-standalone/README.md` - 独立部署说明
- `server/README_WITH_MYSQL.md` - 一体化部署说明

---

**选择适合您的方案，开始部署吧！** 🚀

