# 快速部署指南

## 🚀 5 分钟快速部署（PM2 方式）

### 1. 服务器准备

```bash
# 安装 Node.js (使用 nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20

# 安装 PM2
npm install -g pm2
```

### 2. 上传项目

```bash
# 方式 1: 使用 Git
git clone your-repo-url
cd xingshuzi

# 方式 2: 使用 scp (从本地)
scp -r ./xingshuzi user@server:/path/to/destination
```

### 3. 安装和构建

```bash
cd /path/to/xingshuzi

# 安装依赖
npm ci

# 构建生产版本
npm run build
```

### 4. 启动应用

```bash
# 使用 PM2 启动
pm2 start ecosystem.config.cjs

# 设置开机自启
pm2 save
pm2 startup  # 按提示执行生成的命令
```

### 5. 配置 Nginx（可选）

```bash
# 复制配置文件
sudo cp nginx.conf.example /etc/nginx/sites-available/xingshuzi

# 编辑配置（修改域名和路径）
sudo nano /etc/nginx/sites-available/xingshuzi

# 启用配置
sudo ln -s /etc/nginx/sites-available/xingshuzi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. 配置 SSL（可选）

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## ✅ 验证部署

```bash
# 检查 PM2 状态
pm2 status

# 查看日志
pm2 logs xingshuzi

# 测试访问
curl http://localhost:3000
```

## 📝 常用命令

```bash
# 重启应用
pm2 restart xingshuzi

# 查看监控
pm2 monit

# 更新部署
git pull
npm ci
npm run build
pm2 restart xingshuzi
```

## 🐳 Docker 快速部署

```bash
# 构建镜像
docker build -t xingshuzi .

# 运行容器
docker run -d -p 3000:3000 --name xingshuzi --restart unless-stopped xingshuzi

# 或使用 docker-compose
docker-compose up -d
```

## 📚 更多信息

详细部署说明请查看 [DEPLOY.md](./DEPLOY.md)

