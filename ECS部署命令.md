# ECS上部署MySQL的命令

## 🚀 现在在ECS上执行以下命令：

```bash
# 1. 进入项目目录并拉取最新代码
cd /root/projects/xingshuzi
git pull origin main

# 2. 进入MySQL部署目录
cd mysql-standalone

# 3. 验证文件是否存在
ls -la
# 应该看到: docker-compose.yml, my.cnf, init.sql, deploy.sh, backup.sh

# 4. 给脚本执行权限（如果还没有）
chmod +x deploy.sh backup.sh

# 5. 执行部署
./deploy.sh
```

## ✅ 部署成功后的验证

```bash
# 检查容器状态
docker ps | grep xingshuzi-mysql

# 连接MySQL验证
docker compose exec mysql mysql -uroot -pMyStrongRootPassword123

# 在MySQL中执行
SHOW DATABASES;
USE xingshuzi;
SHOW TABLES;
```

## 📝 后续步骤

### 如果要使用这个Docker MySQL（推荐）

```bash
# 1. 修改后端配置
cd /root/projects/xingshuzi/server
nano .env

# 修改以下内容：
# MYSQL_HOST=120.76.247.123  (或 localhost)
# MYSQL_PORT=3306
# MYSQL_DB=xingshuzi
# MYSQL_USER=root
# MYSQL_PASSWORD=MyStrongRootPassword123

# 2. 重新部署后端
./deploy.sh

# 3. 初始化数据库
docker exec xingshuzi-api python3 create_db.py
docker exec xingshuzi-api python3 init_admin.py

# 4. 验证
curl http://localhost:5001/api/home/banners
```

## 🔧 常用管理命令

```bash
# 查看MySQL日志
cd /root/projects/xingshuzi/mysql-standalone
docker compose logs -f mysql

# 重启MySQL
docker compose restart mysql

# 停止MySQL
docker compose down

# 备份数据库
./backup.sh

# 查看容器状态
docker compose ps
```

## 💡 提示

- MySQL数据存储在Docker volume中，即使删除容器数据也不会丢失
- 端口3306已对外开放，可以使用Navicat等工具远程连接
- 定期备份数据库：`./backup.sh`
- 备份文件保存在 `/root/mysql_backups/` 目录

---

**现在去ECS上执行这些命令吧！** 🚀

