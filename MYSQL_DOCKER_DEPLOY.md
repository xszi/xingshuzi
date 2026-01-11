# MySQL数据库 Docker部署文档

本文档介绍如何在Docker中部署MySQL数据库，供星书子项目使用。

## 📋 部署方案对比

### 方案一：使用已有的线上MySQL（当前方案）
- ✅ 简单，无需额外部署
- ✅ 数据独立，不受容器影响
- ❌ 依赖外部服务

### 方案二：Docker独立部署MySQL（本文档）
- ✅ 完全容器化，易于管理
- ✅ 数据持久化，易于备份
- ✅ 隔离性好，安全可控
- ⚠️ 需要配置数据卷

### 方案三：Server + MySQL 一体化部署
- ✅ 一键部署，简单快捷
- ✅ 服务间网络通信快
- ⚠️ 重启Server时可能影响数据库

## 🚀 方案一：独立部署MySQL容器（推荐生产环境）

### 1. 创建MySQL部署目录

```bash
# SSH登录ECS
ssh root@120.76.247.123

# 创建MySQL部署目录
mkdir -p /root/xingshuzi-mysql
cd /root/xingshuzi-mysql
```

### 2. 创建docker-compose.yml

```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: xingshuzi-mysql
    restart: unless-stopped
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: MyStrongRootPassword123
      MYSQL_DATABASE: xingshuzi
      MYSQL_USER: xingshuzi_user
      MYSQL_PASSWORD: xingshuzi_pass
      TZ: Asia/Shanghai
    volumes:
      # 数据持久化
      - mysql_data:/var/lib/mysql
      # 配置文件
      - ./my.cnf:/etc/mysql/conf.d/my.cnf
      # 初始化脚本
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    command:
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      - --default-authentication-plugin=mysql_native_password
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-p${MYSQL_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

volumes:
  mysql_data:
    driver: local
```

### 3. 创建MySQL配置文件 (my.cnf)

```ini
[mysqld]
# 字符集
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci

# 性能优化
max_connections=500
max_connect_errors=100
wait_timeout=28800
interactive_timeout=28800

# 缓存设置
key_buffer_size=32M
table_open_cache=128
sort_buffer_size=768K
read_buffer_size=768K

# InnoDB设置
innodb_buffer_pool_size=256M
innodb_log_file_size=64M
innodb_flush_log_at_trx_commit=1
innodb_lock_wait_timeout=50

# 日志设置
log_error=/var/log/mysql/error.log
slow_query_log=1
slow_query_log_file=/var/log/mysql/slow.log
long_query_time=2

# 时区
default-time-zone='+08:00'

[client]
default-character-set=utf8mb4
```

### 4. 创建初始化脚本 (init.sql)

```sql
-- 设置字符集
SET NAMES utf8mb4;

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS xingshuzi DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE xingshuzi;

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` varchar(20) DEFAULT 'user',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入默认管理员账号
INSERT INTO `users` (`username`, `password`, `email`, `role`) 
VALUES ('admin', 'pbkdf2:sha256:600000$...(需要生成密码hash)', 'admin@xingshuzi.com', 'admin')
ON DUPLICATE KEY UPDATE username=username;

-- 书籍表
CREATE TABLE IF NOT EXISTS `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  `cover` varchar(500) DEFAULT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT '0',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 课程表
CREATE TABLE IF NOT EXISTS `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `teacher` varchar(100) DEFAULT NULL,
  `cover` varchar(500) DEFAULT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `duration` int DEFAULT NULL COMMENT '课程时长(分钟)',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 音乐表
CREATE TABLE IF NOT EXISTS `music` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `artist` varchar(100) DEFAULT NULL,
  `cover` varchar(500) DEFAULT NULL,
  `audio_url` varchar(500) DEFAULT NULL,
  `duration` int DEFAULT NULL COMMENT '音乐时长(秒)',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 商品表
CREATE TABLE IF NOT EXISTS `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `cover` varchar(500) DEFAULT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT '0',
  `category` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 轮播图表
CREATE TABLE IF NOT EXISTS `banner` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `image` varchar(500) NOT NULL,
  `link` varchar(500) DEFAULT NULL,
  `sort` int DEFAULT '0',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 5. 创建部署脚本 (deploy.sh)

```bash
#!/bin/bash
set -e

echo "=========================================="
echo "  MySQL数据库 Docker部署"
echo "=========================================="

# 检查文件
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 错误: docker-compose.yml 不存在"
    exit 1
fi

# 创建日志目录
echo "📁 创建日志目录..."
mkdir -p logs

# 停止旧容器（如果存在）
echo "🛑 停止旧容器..."
docker compose down 2>/dev/null || true

# 构建并启动
echo "🚀 启动MySQL容器..."
docker compose up -d

# 等待MySQL启动
echo "⏳ 等待MySQL启动..."
sleep 10

# 检查健康状态
echo "🔍 检查MySQL状态..."
for i in {1..30}; do
    if docker compose exec mysql mysqladmin ping -h localhost -uroot -pMyStrongRootPassword123 --silent 2>/dev/null; then
        echo "✅ MySQL启动成功！"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ MySQL启动超时"
        docker compose logs mysql
        exit 1
    fi
    echo "等待中... ($i/30)"
    sleep 2
done

# 显示状态
echo ""
echo "=========================================="
echo "  MySQL部署完成"
echo "=========================================="
echo "容器名称: xingshuzi-mysql"
echo "端口: 3306"
echo "数据库: xingshuzi"
echo "Root密码: MyStrongRootPassword123"
echo "普通用户: xingshuzi_user"
echo "普通密码: xingshuzi_pass"
echo ""
echo "连接命令:"
echo "  docker compose exec mysql mysql -uroot -p"
echo ""
echo "查看日志:"
echo "  docker compose logs -f mysql"
echo "=========================================="
```

### 6. 部署MySQL

```bash
# 创建配置文件
cat > my.cnf << 'EOF'
[mysqld]
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
max_connections=500
innodb_buffer_pool_size=256M
default-time-zone='+08:00'

[client]
default-character-set=utf8mb4
EOF

# 创建初始化脚本（简化版）
cat > init.sql << 'EOF'
SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS xingshuzi DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EOF

# 给脚本执行权限
chmod +x deploy.sh

# 执行部署
./deploy.sh
```

### 7. 验证部署

```bash
# 检查容器状态
docker ps | grep xingshuzi-mysql

# 连接MySQL
docker compose exec mysql mysql -uroot -pMyStrongRootPassword123

# 在MySQL中执行
SHOW DATABASES;
USE xingshuzi;
SHOW TABLES;
```

### 8. 修改后端配置连接Docker MySQL

```bash
# 编辑server/.env
cd /root/xingshuzi/server
nano .env

# 修改为
MYSQL_HOST=120.76.247.123  # 或使用容器名
MYSQL_PORT=3306
MYSQL_DB=xingshuzi
MYSQL_USER=root
MYSQL_PASSWORD=MyStrongRootPassword123
```

---

## 🚀 方案二：Server + MySQL 一体化部署

### 创建统一的docker-compose.yml

在 `/root/xingshuzi/server/` 目录下：

```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: xingshuzi-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: MyStrongRootPassword123
      MYSQL_DATABASE: xingshuzi
      TZ: Asia/Shanghai
    volumes:
      - mysql_data:/var/lib/mysql
    command:
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      - --default-authentication-plugin=mysql_native_password
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-pMyStrongRootPassword123"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - xingshuzi-network

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: xingshuzi-api
    restart: unless-stopped
    ports:
      - "5001:5001"
    environment:
      - MYSQL_HOST=mysql  # 使用服务名
      - MYSQL_PORT=3306
      - MYSQL_DB=xingshuzi
      - MYSQL_USER=root
      - MYSQL_PASSWORD=MyStrongRootPassword123
      - SECRET_KEY=${SECRET_KEY:-your-secret-key}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY:-your-jwt-secret-key}
      - FLASK_PORT=5001
    depends_on:
      mysql:
        condition: service_healthy
    networks:
      - xingshuzi-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5001/api/home/banners"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  mysql_data:
    driver: local

networks:
  xingshuzi-network:
    driver: bridge
```

### 部署命令

```bash
cd /root/xingshuzi/server

# 一键部署（包含MySQL和API）
./deploy.sh
```

---

## 🔧 数据库管理

### 1. 连接数据库

```bash
# 方式一：通过容器
docker compose exec mysql mysql -uroot -pMyStrongRootPassword123

# 方式二：从宿主机（如果安装了mysql客户端）
mysql -h 120.76.247.123 -P 3306 -uroot -pMyStrongRootPassword123

# 方式三：使用图形化工具（Navicat、DBeaver等）
# 主机: 120.76.247.123
# 端口: 3306
# 用户: root
# 密码: MyStrongRootPassword123
```

### 2. 数据库初始化

```bash
# 进入项目server目录
cd /root/xingshuzi/server

# 初始化数据库表
docker compose exec api python3 create_db.py

# 创建管理员账号
docker compose exec api python3 init_admin.py
```

### 3. 备份数据库

```bash
# 备份到文件
docker compose exec mysql mysqldump -uroot -pMyStrongRootPassword123 xingshuzi > backup_$(date +%Y%m%d_%H%M%S).sql

# 或使用脚本自动备份
cat > /root/backup_mysql.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/root/mysql_backups"
mkdir -p $BACKUP_DIR
BACKUP_FILE="$BACKUP_DIR/xingshuzi_$(date +%Y%m%d_%H%M%S).sql"

docker compose -f /root/xingshuzi-mysql/docker-compose.yml exec mysql \
  mysqldump -uroot -pMyStrongRootPassword123 xingshuzi > $BACKUP_FILE

# 压缩备份
gzip $BACKUP_FILE

# 删除7天前的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "备份完成: ${BACKUP_FILE}.gz"
EOF

chmod +x /root/backup_mysql.sh
```

### 4. 恢复数据库

```bash
# 从备份恢复
docker compose exec -T mysql mysql -uroot -pMyStrongRootPassword123 xingshuzi < backup_20260111_120000.sql

# 如果是压缩文件
gunzip -c backup_20260111_120000.sql.gz | docker compose exec -T mysql mysql -uroot -pMyStrongRootPassword123 xingshuzi
```

### 5. 定时备份（crontab）

```bash
# 编辑定时任务
crontab -e

# 添加每天凌晨2点备份
0 2 * * * /root/backup_mysql.sh >> /root/backup_mysql.log 2>&1
```

---

## 📊 性能优化

### 1. MySQL配置优化（根据服务器配置）

**2核4GB内存配置：**
```ini
[mysqld]
innodb_buffer_pool_size=1G
max_connections=300
innodb_log_file_size=128M
```

**4核8GB内存配置：**
```ini
[mysqld]
innodb_buffer_pool_size=2G
max_connections=500
innodb_log_file_size=256M
```

### 2. 查看MySQL性能

```bash
# 连接MySQL后执行
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW STATUS LIKE 'Threads_connected';
SHOW PROCESSLIST;
```

---

## 🐛 故障排查

### 1. MySQL无法启动

```bash
# 查看日志
docker compose logs mysql

# 检查数据卷
docker volume ls
docker volume inspect xingshuzi-mysql_mysql_data

# 删除数据卷重新开始（会丢失数据！）
docker compose down -v
docker compose up -d
```

### 2. 无法连接MySQL

```bash
# 检查端口
netstat -tlnp | grep 3306

# 检查容器状态
docker ps | grep mysql

# 测试连接
docker compose exec mysql mysqladmin ping -h localhost -uroot -pMyStrongRootPassword123
```

### 3. 性能问题

```bash
# 查看慢查询日志
docker compose exec mysql tail -f /var/log/mysql/slow.log

# 查看错误日志
docker compose exec mysql tail -f /var/log/mysql/error.log
```

---

## 🔐 安全建议

### 1. 修改默认密码

```sql
-- 连接MySQL后执行
ALTER USER 'root'@'%' IDENTIFIED BY '新的强密码';
FLUSH PRIVILEGES;
```

### 2. 创建应用专用账号（推荐）

```sql
-- 创建专用用户
CREATE USER 'xingshuzi_app'@'%' IDENTIFIED BY '强密码';
GRANT SELECT, INSERT, UPDATE, DELETE ON xingshuzi.* TO 'xingshuzi_app'@'%';
FLUSH PRIVILEGES;

-- 后端.env使用专用账号
MYSQL_USER=xingshuzi_app
MYSQL_PASSWORD=强密码
```

### 3. 限制远程访问（如果不需要）

```yaml
# docker-compose.yml中
services:
  mysql:
    ports:
      - "127.0.0.1:3306:3306"  # 只允许本地访问
```

---

## ✅ 快速命令参考

```bash
# === 部署MySQL ===
cd /root/xingshuzi-mysql
./deploy.sh

# === 管理MySQL ===
docker compose ps                    # 查看状态
docker compose logs -f mysql         # 查看日志
docker compose restart mysql         # 重启
docker compose stop mysql            # 停止
docker compose start mysql           # 启动
docker compose down                  # 完全停止

# === 连接MySQL ===
docker compose exec mysql mysql -uroot -pMyStrongRootPassword123

# === 备份恢复 ===
./backup_mysql.sh                    # 备份
docker compose exec -T mysql mysql -uroot -p xingshuzi < backup.sql  # 恢复

# === 查看数据 ===
docker volume ls                     # 查看数据卷
docker exec xingshuzi-mysql du -sh /var/lib/mysql  # 查看数据大小
```

---

## 📖 推荐方案总结

| 场景 | 推荐方案 | 理由 |
|------|----------|------|
| **生产环境** | 方案一（独立MySQL） | 稳定、易备份、易扩展 |
| **开发测试** | 方案二（一体化） | 简单、快速、便于调试 |
| **现有数据库** | 使用线上MySQL | 无需迁移、风险小 |

---

**MySQL Docker部署完成，数据安全可靠！** 🎉

