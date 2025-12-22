# 服务器部署指南

本文档介绍如何将行书子项目部署到生产服务器。

## 目录

- [前置要求](#前置要求)
- [部署方式](#部署方式)
  - [方式一：使用 PM2（推荐）](#方式一使用-pm2推荐)
  - [方式二：使用 Docker](#方式二使用-docker)
  - [方式三：使用 systemd](#方式三使用-systemd)
- [Nginx 反向代理配置](#nginx-反向代理配置)
- [SSL/HTTPS 配置](#sslhttps-配置)
- [环境变量配置](#环境变量配置)
- [监控和维护](#监控和维护)

## 前置要求

### 服务器要求

- **操作系统**: Linux (Ubuntu 20.04+ / CentOS 7+ 推荐)
- **Node.js**: v18.x 或 v20.x
- **内存**: 至少 1GB RAM
- **磁盘空间**: 至少 2GB 可用空间

### 必需软件

```bash
# 安装 Node.js (使用 NodeSource)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 或使用 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20

# 安装 PM2 (推荐)
sudo npm install -g pm2

# 安装 Nginx (用于反向代理)
sudo apt-get update
sudo apt-get install -y nginx
```

## 部署方式

### 方式一：使用 PM2（推荐）

PM2 是一个强大的 Node.js 进程管理器，支持自动重启、负载均衡、日志管理等功能。

#### 1. 上传项目到服务器

```bash
# 使用 git
git clone your-repo-url
cd xingshuzi

# 或使用 scp
scp -r ./xingshuzi user@your-server:/path/to/destination
```

#### 2. 安装依赖并构建

```bash
cd /path/to/xingshuzi

# 安装依赖
npm ci

# 构建生产版本
npm run build
```

#### 3. 使用 PM2 启动

```bash
# 使用配置文件启动（推荐）
pm2 start ecosystem.config.cjs

# 或直接启动
pm2 start .output/server/index.mjs --name xingshuzi -i 2

# 保存 PM2 配置（开机自启）
pm2 save
pm2 startup  # 按照提示执行生成的命令
```

#### 4. PM2 常用命令

```bash
# 查看状态
pm2 status

# 查看日志
pm2 logs xingshuzi

# 重启应用
pm2 restart xingshuzi

# 停止应用
pm2 stop xingshuzi

# 删除应用
pm2 delete xingshuzi

# 监控
pm2 monit
```

#### 5. 使用部署脚本

项目提供了自动化部署脚本：

```bash
# 给脚本添加执行权限
chmod +x deploy.sh

# 运行部署脚本
bash deploy.sh
```

### 方式二：使用 Docker

#### 1. 构建 Docker 镜像

```bash
# 构建镜像
docker build -t xingshuzi:latest .

# 或使用 docker-compose
docker-compose build
```

#### 2. 运行容器

```bash
# 直接运行
docker run -d \
  --name xingshuzi \
  -p 3000:3000 \
  --restart unless-stopped \
  xingshuzi:latest

# 或使用 docker-compose
docker-compose up -d
```

#### 3. 查看日志

```bash
docker logs -f xingshuzi
```

### 方式三：使用 systemd

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/xingshuzi.service
```

内容如下：

```ini
[Unit]
Description=XingShuZi Nuxt Application
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/xingshuzi
Environment=NODE_ENV=production
Environment=PORT=3000
Environment=HOST=0.0.0.0
ExecStart=/usr/bin/node .output/server/index.mjs
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start xingshuzi

# 设置开机自启
sudo systemctl enable xingshuzi

# 查看状态
sudo systemctl status xingshuzi
```

## Nginx 反向代理配置

### 1. 创建 Nginx 配置

```bash
sudo nano /etc/nginx/sites-available/xingshuzi
```

复制 `nginx.conf.example` 的内容，并修改以下内容：

- `server_name`: 你的域名
- `/path/to/your/project`: 项目的实际路径

### 2. 启用配置

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/xingshuzi /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

### 3. 防火墙配置

```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## SSL/HTTPS 配置

### 使用 Let's Encrypt (免费)

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书（自动配置 Nginx）
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期测试
sudo certbot renew --dry-run
```

证书会自动续期，无需手动操作。

## 环境变量配置

### 创建 .env 文件

```bash
nano .env.production
```

示例内容：

```env
NODE_ENV=production
PORT=3000
HOST=0.0.0.0
NUXT_PUBLIC_API_BASE=https://api.example.com
```

### 在 nuxt.config.ts 中使用

```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    // 服务端私有配置
    apiSecret: process.env.API_SECRET,
    
    // 客户端公开配置
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:3000'
    }
  }
})
```

## 监控和维护

### 1. 日志管理

```bash
# PM2 日志
pm2 logs xingshuzi --lines 100

# Nginx 日志
sudo tail -f /var/log/nginx/xingshuzi_access.log
sudo tail -f /var/log/nginx/xingshuzi_error.log

# systemd 日志
sudo journalctl -u xingshuzi -f
```

### 2. 性能监控

```bash
# PM2 监控
pm2 monit

# 系统资源
htop
```

### 3. 更新部署

```bash
# 拉取最新代码
git pull origin main

# 重新安装依赖（如果有新依赖）
npm ci

# 重新构建
npm run build

# 重启应用
pm2 restart xingshuzi
# 或使用部署脚本
bash deploy.sh
```

### 4. 备份

定期备份以下内容：

- 项目代码（Git 仓库）
- 数据库（如果有）
- 环境变量文件
- 日志文件

## 常见问题

### 1. 端口被占用

```bash
# 查看端口占用
sudo lsof -i :3000
# 或
sudo netstat -tulpn | grep 3000

# 修改端口（在 ecosystem.config.cjs 或环境变量中）
```

### 2. 内存不足

```bash
# 增加 PM2 内存限制
# 在 ecosystem.config.cjs 中修改 max_memory_restart
```

### 3. 应用无法访问

- 检查防火墙设置
- 检查 Nginx 配置
- 检查应用是否正常运行：`pm2 status`
- 查看错误日志：`pm2 logs xingshuzi`

## 安全建议

1. **使用非 root 用户运行应用**
2. **定期更新依赖**: `npm audit` 和 `npm update`
3. **配置防火墙**: 只开放必要端口
4. **使用 HTTPS**: 保护数据传输
5. **设置环境变量**: 不要硬编码敏感信息
6. **定期备份**: 防止数据丢失

## 相关资源

- [Nuxt 部署文档](https://nuxt.com/docs/getting-started/deployment)
- [PM2 文档](https://pm2.keymetrics.io/docs/usage/quick-start/)
- [Nginx 文档](https://nginx.org/en/docs/)
- [Docker 文档](https://docs.docker.com/)


