# xingshuzi-back Docker 部署文档

本文档介绍如何在阿里云 ECS Ubuntu 服务器上使用 Docker 部署 xingshuzi-back Flask 项目。

## 📋 目录

- [一、服务器环境准备](#一服务器环境准备)
- [二、安装 Docker 和 Docker Compose](#二安装-docker-和-docker-compose)
- [三、部署应用](#三部署应用)
- [四、配置 Nginx 反向代理](#四配置-nginx-反向代理可选)
- [五、管理和维护](#五管理和维护)
- [六、常见问题](#六常见问题)

---

## 一、服务器环境准备

### 1.1 连接到服务器

```bash
ssh root@your-server-ip
```

### 1.2 更新系统

```bash
apt update
apt upgrade -y
```

### 1.3 安装基础工具

```bash
apt install -y git curl wget vim
```

---

## 二、安装 Docker 和 Docker Compose

### 2.1 安装 Docker

```bash
# 卸载旧版本（如果有）
apt remove docker docker-engine docker.io containerd runc

# 安装依赖
apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 添加 Docker 官方 GPG 密钥
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 设置 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker Engine
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 验证安装
docker --version
docker compose version
```

### 2.2 启动 Docker 服务

```bash
# 启动 Docker
systemctl start docker

# 设置开机自启
systemctl enable docker

# 查看状态
systemctl status docker
```

### 2.3 配置 Docker（可选）

```bash
# 添加当前用户到 docker 组（如果不是 root）
usermod -aG docker $USER

# 配置 Docker 镜像加速（阿里云镜像）
mkdir -p /etc/docker
tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
EOF

# 重启 Docker
systemctl daemon-reload
systemctl restart docker
```

---

## 三、部署应用

### 3.1 创建项目目录

```bash
mkdir -p /opt/xingshuzi-back
cd /opt/xingshuzi-back
```

### 3.2 上传项目文件

**方式一：使用 Git（推荐）**

```bash
git clone <your-repo-url> .
```

**方式二：使用 SCP**

在本地机器执行：

```bash
scp -r /path/to/xingshuzi-back root@your-server-ip:/opt/
```

**方式三：使用 SFTP 工具**

使用 FileZilla、WinSCP 等工具上传项目文件到 `/opt/xingshuzi-back`

### 3.3 创建环境变量文件

```bash
cd /opt/xingshuzi-back
cat > .env << 'EOF'
# MySQL 数据库配置
MYSQL_USER=root
MYSQL_PASSWORD=MyStrongRootPassword123
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DB=xingshuzi

# Flask 密钥（生产环境请修改）
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
EOF
```

**⚠️ 重要：生产环境请务必修改密钥！**

生成随机密钥：

```bash
# 生成 SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

# 生成 JWT_SECRET_KEY
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

### 3.4 构建并启动容器

```bash
# 构建并启动所有服务
docker compose up -d

# 查看启动日志
docker compose logs -f
```

### 3.5 初始化数据库

等待 MySQL 容器完全启动后（约 30 秒），执行数据库初始化：

```bash
# 创建数据库表
docker compose exec app python3 -c "from app import create_app, db; from app.models.user import User; app = create_app(); app.app_context().push(); db.create_all(); print('数据库表创建成功！')"

# 创建管理员账号
docker compose exec app python3 init_admin.py
```

**默认管理员账号：**
- 用户名：`admin`
- 密码：`admin123`

**⚠️ 首次登录后请立即修改密码！**

### 3.6 验证部署

```bash
# 测试首页接口
curl http://localhost:5000/api/home/banners

# 测试登录接口
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

如果返回正常的 JSON 数据，说明部署成功！

---

## 四、配置 Nginx 反向代理（可选）

### 4.1 使用 Docker 运行 Nginx

创建 Nginx 配置文件：

```bash
mkdir -p /opt/nginx/conf.d
cat > /opt/nginx/conf.d/xingshuzi.conf << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或 IP

    client_max_body_size 20M;

    location / {
        proxy_pass http://172.17.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS 支持
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS';
        add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
    }
}
EOF
```

启动 Nginx 容器：

```bash
docker run -d \
  --name nginx \
  --restart always \
  -p 80:80 \
  -p 443:443 \
  -v /opt/nginx/conf.d:/etc/nginx/conf.d \
  nginx:alpine
```

### 4.2 直接安装 Nginx（推荐）

```bash
# 安装 Nginx
apt install -y nginx

# 创建配置文件
cat > /etc/nginx/sites-available/xingshuzi << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/xingshuzi /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
systemctl enable nginx
```

### 4.3 配置 HTTPS（推荐）

```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 获取 SSL 证书（需要域名已解析）
certbot --nginx -d your-domain.com

# 自动续期
certbot renew --dry-run
```

---

## 五、管理和维护

### 5.1 Docker 容器管理

```bash
# 查看运行中的容器
docker compose ps

# 查看日志
docker compose logs -f
docker compose logs -f app    # 只查看应用日志
docker compose logs -f mysql  # 只查看数据库日志

# 停止服务
docker compose stop

# 启动服务
docker compose start

# 重启服务
docker compose restart

# 停止并删除容器
docker compose down

# 停止并删除容器和数据卷（⚠️ 会删除数据库数据）
docker compose down -v
```

### 5.2 更新应用

```bash
cd /opt/xingshuzi-back

# 拉取最新代码（如果使用 Git）
git pull

# 重新构建镜像
docker compose build

# 重启服务
docker compose down
docker compose up -d

# 查看日志确认
docker compose logs -f app
```

### 5.3 数据库备份

```bash
# 创建备份目录
mkdir -p /opt/backups

# 备份数据库
docker compose exec mysql mysqldump \
  -u root \
  -pMyStrongRootPassword123 \
  xingshuzi > /opt/backups/xingshuzi_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
docker compose exec -T mysql mysql \
  -u root \
  -pMyStrongRootPassword123 \
  xingshuzi < /opt/backups/xingshuzi_20231224_120000.sql
```

创建自动备份脚本：

```bash
cat > /opt/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份数据库
docker compose exec mysql mysqldump \
  -u root \
  -pMyStrongRootPassword123 \
  xingshuzi > $BACKUP_DIR/xingshuzi_$DATE.sql

# 压缩备份
gzip $BACKUP_DIR/xingshuzi_$DATE.sql

# 删除 7 天前的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Backup completed: xingshuzi_$DATE.sql.gz"
EOF

chmod +x /opt/backup.sh

# 添加到 crontab（每天凌晨 2 点备份）
crontab -e
# 添加：0 2 * * * cd /opt/xingshuzi-back && /opt/backup.sh
```

### 5.4 查看系统资源

```bash
# 查看容器资源使用
docker stats

# 查看磁盘使用
docker system df

# 清理未使用的镜像和容器
docker system prune -a
```

---

## 六、常见问题

### 6.1 容器无法启动

```bash
# 查看详细日志
docker compose logs app
docker compose logs mysql

# 检查容器状态
docker compose ps

# 重新构建
docker compose build --no-cache
docker compose up -d
```

### 6.2 数据库连接失败

**检查 MySQL 容器是否正常运行：**

```bash
docker compose ps mysql
docker compose logs mysql
```

**测试数据库连接：**

```bash
docker compose exec mysql mysql -u root -pMyStrongRootPassword123 -e "SHOW DATABASES;"
```

**常见原因：**
- MySQL 容器未完全启动（等待 30-60 秒）
- 密码配置错误（检查 `.env` 和 `docker-compose.yml`）
- 网络连接问题

### 6.3 端口被占用

```bash
# 查看端口占用
netstat -tlnp | grep 5000
netstat -tlnp | grep 3306

# 修改 docker-compose.yml 中的端口映射
# 例如：将 "5000:5000" 改为 "8000:5000"
```

### 6.4 忘记管理员密码

```bash
# 重置管理员密码
docker compose exec app python3 << 'EOF'
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.set_password('新密码')
        db.session.commit()
        print('密码已重置')
    else:
        print('管理员用户不存在')
EOF
```

### 6.5 清理所有数据重新开始

```bash
# ⚠️ 警告：这将删除所有数据！
cd /opt/xingshuzi-back

# 停止并删除容器和数据卷
docker compose down -v

# 重新启动
docker compose up -d

# 等待 30 秒后初始化数据库
sleep 30
docker compose exec app python3 -c "from app import create_app, db; from app.models.user import User; app = create_app(); app.app_context().push(); db.create_all(); print('OK')"
docker compose exec app python3 init_admin.py
```

---

## 七、防火墙和安全配置

### 7.1 阿里云安全组配置

在阿里云控制台配置安全组规则：

**入方向规则：**
| 端口 | 协议 | 说明 |
|------|------|------|
| 22 | TCP | SSH（限制来源 IP） |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |
| 5000 | TCP | Flask（如果不使用 Nginx，可选） |
| 3306 | TCP | MySQL（⚠️ 仅在需要外部访问数据库时开放） |

### 7.2 Ubuntu 防火墙（UFW）

```bash
# 启用防火墙
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# 查看状态
ufw status
```

### 7.3 安全建议

1. **修改默认密码**：
   - 管理员账号密码
   - MySQL root 密码
   - SECRET_KEY 和 JWT_SECRET_KEY

2. **限制 SSH 访问**：
```bash
# 编辑 SSH 配置
nano /etc/ssh/sshd_config

# 禁用 root 密码登录，使用密钥登录
PermitRootLogin prohibit-password
PasswordAuthentication no

# 重启 SSH
systemctl restart sshd
```

3. **定期更新**：
```bash
apt update && apt upgrade -y
```

4. **设置 fail2ban 防止暴力破解**：
```bash
apt install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

---

## 八、快速部署脚本

### 8.1 一键部署脚本

创建 `deploy.sh` 脚本：

```bash
#!/bin/bash
set -e

echo "========================================="
echo "xingshuzi-back Docker 快速部署脚本"
echo "========================================="

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "请使用 root 用户运行此脚本"
    exit 1
fi

# 1. 更新系统
echo "[1/6] 更新系统..."
apt update && apt upgrade -y

# 2. 安装 Docker
echo "[2/6] 安装 Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | bash
    systemctl start docker
    systemctl enable docker
else
    echo "Docker 已安装"
fi

# 3. 创建项目目录
echo "[3/6] 创建项目目录..."
mkdir -p /opt/xingshuzi-back
cd /opt/xingshuzi-back

# 4. 生成环境变量文件
echo "[4/6] 生成环境变量..."
if [ ! -f .env ]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    cat > .env << EOF
MYSQL_USER=root
MYSQL_PASSWORD=MyStrongRootPassword123
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DB=xingshuzi
SECRET_KEY=$SECRET_KEY
JWT_SECRET_KEY=$JWT_SECRET_KEY
EOF
    echo ".env 文件已创建"
else
    echo ".env 文件已存在"
fi

# 5. 启动服务
echo "[5/6] 启动 Docker 服务..."
docker compose up -d

# 6. 等待 MySQL 启动并初始化数据库
echo "[6/6] 初始化数据库..."
echo "等待 MySQL 启动（30秒）..."
sleep 30

docker compose exec app python3 -c "from app import create_app, db; from app.models.user import User; app = create_app(); app.app_context().push(); db.create_all(); print('数据库表创建成功！')"
docker compose exec app python3 init_admin.py

echo ""
echo "========================================="
echo "✅ 部署完成！"
echo "========================================="
echo ""
echo "服务地址: http://$(curl -s ifconfig.me):5000"
echo "管理员账号: admin"
echo "管理员密码: admin123"
echo ""
echo "查看日志: cd /opt/xingshuzi-back && docker compose logs -f"
echo "停止服务: cd /opt/xingshuzi-back && docker compose stop"
echo "启动服务: cd /opt/xingshuzi-back && docker compose start"
echo ""
```

使用脚本：

```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 九、监控和日志

### 9.1 查看实时日志

```bash
# 查看所有服务日志
docker compose logs -f

# 查看应用日志
docker compose logs -f app

# 查看最近 100 行日志
docker compose logs --tail=100 app
```

### 9.2 进入容器调试

```bash
# 进入应用容器
docker compose exec app bash

# 进入 MySQL 容器
docker compose exec mysql bash

# 在应用容器中执行 Python 命令
docker compose exec app python3 -c "from app import create_app; print(create_app())"
```

### 9.3 健康检查

```bash
# 检查容器健康状态
docker compose ps

# 测试 API 端点
curl http://localhost:5000/api/home/banners
```

---

## 十、性能优化

### 10.1 使用生产级 WSGI 服务器

修改 `Dockerfile`，使用 Gunicorn：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

创建 `run.py`（如果没有）：

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 10.2 资源限制

在 `docker-compose.yml` 中添加资源限制：

```yaml
services:
  app:
    # ... 其他配置
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## 总结

✅ **部署完成后，你的服务将：**

- 运行在 Docker 容器中，易于管理和迁移
- MySQL 数据持久化存储
- 自动重启（容器崩溃时）
- 通过 Docker Compose 统一管理
- 支持一键更新和回滚

📝 **重要提醒：**

1. 首次登录后立即修改管理员密码
2. 修改 `.env` 中的 SECRET_KEY 和 JWT_SECRET_KEY
3. 定期备份数据库
4. 配置防火墙和安全组规则
5. 建议配置 Nginx 反向代理和 HTTPS

🔗 **相关文档：**

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [Flask 部署指南](https://flask.palletsprojects.com/en/latest/deploying/)

如有问题，请检查日志文件排查：`docker compose logs -f`
