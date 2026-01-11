# MySQL独立部署说明

本目录包含MySQL数据库的独立Docker部署配置。

## 📋 文件说明

- `docker-compose.yml` - Docker Compose配置文件
- `my.cnf` - MySQL配置文件
- `init.sql` - 数据库初始化脚本（创建表结构）
- `deploy.sh` - 一键部署脚本
- `backup.sh` - 数据库备份脚本

## 🚀 快速部署

### 1. 上传文件到ECS

将整个 `mysql-standalone` 目录上传到ECS：

```bash
# 方式一：使用Git（推荐）
# 在本地推送代码到Git仓库后，在ECS上：
cd /root
git clone git@github.com:your-username/xingshuzi.git
cd xingshuzi/mysql-standalone

# 方式二：使用scp上传
scp -r mysql-standalone root@120.76.247.123:/root/

# 方式三：在ECS上手动创建文件
# 参考 MYSQL_DOCKER_DEPLOY.md 文档
```

### 2. 执行部署

```bash
cd /root/xingshuzi/mysql-standalone

# 给脚本执行权限
chmod +x deploy.sh

# 执行部署
./deploy.sh
```

### 3. 验证部署

```bash
# 检查容器状态
docker ps | grep xingshuzi-mysql

# 连接数据库
docker compose exec mysql mysql -uroot -pMyStrongRootPassword123

# 查看数据库
SHOW DATABASES;
USE xingshuzi;
SHOW TABLES;
```

## 🔧 初始化管理员账号

MySQL部署完成后，需要初始化管理员账号：

```bash
# 进入后端项目目录
cd /root/xingshuzi/server

# 修改.env，连接到Docker MySQL
nano .env
# 设置: MYSQL_HOST=120.76.247.123 (或使用localhost)

# 初始化管理员账号
python3 init_admin.py
```

## 📊 数据库连接信息

**Root账号（管理用）：**
- 主机: `120.76.247.123`
- 端口: `3306`
- 用户: `root`
- 密码: `MyStrongRootPassword123`
- 数据库: `xingshuzi`

**应用账号（推荐用于后端）：**
- 用户: `xingshuzi_user`
- 密码: `xingshuzi_pass`

## 🔐 安全建议

部署到生产环境后，建议：

1. **修改默认密码**
2. **使用应用专用账号**（而不是root）
3. **定期备份数据**
4. **监控数据库性能**

详见主文档 `MYSQL_DOCKER_DEPLOY.md`

## ✅ 常用命令

```bash
# 查看状态
docker compose ps

# 查看日志
docker compose logs -f mysql

# 重启
docker compose restart mysql

# 停止
docker compose down

# 连接数据库
docker compose exec mysql mysql -uroot -pMyStrongRootPassword123

# 备份数据库
docker compose exec mysql mysqldump -uroot -pMyStrongRootPassword123 xingshuzi > backup_$(date +%Y%m%d).sql
```

