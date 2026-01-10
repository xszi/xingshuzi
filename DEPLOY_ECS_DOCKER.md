# 阿里云 ECS 使用 Docker 部署（行书子：Nuxt SSR + Flask API + MySQL + Nginx + HTTPS）
本指南用于把本仓库的**前端 `web`（Nuxt SSR）**与**后端 `server`（Flask）**部署到阿里云 ECS（Ubuntu）上，并通过 **Nginx** 提供统一域名访问与 HTTPS。

> 推荐架构：只对外开放 `80/443/22`，不直接暴露 `3000/5000/3306`。

---

## 部署目标

- 访问站点：`https://你的域名/` → Nuxt SSR（容器：`web`）
- 访问接口：`https://你的域名/api/*` → Flask API（容器：`api`）
- 数据库：MySQL（容器：`mysql`，仅内网）
- 反向代理：Nginx（容器：`nginx`，对外暴露 `80/443`）

---

## 1. ECS 前置准备

### 1.1 安全组放行

在阿里云控制台 → ECS → 安全组 → 入方向规则：

- **22/TCP**：SSH（建议限制为你的办公/家庭公网 IP）
- **80/TCP**：HTTP
- **443/TCP**：HTTPS

> 不要对公网开放 3306（数据库）和 5000（后端）/3000（前端）。统一走 Nginx。

### 1.2 域名解析

在域名解析处添加：

- `A 记录`：`@` → 指向 ECS 公网 IP
- `A 记录`：`www` → 指向 ECS 公网 IP（可选）

---

## 2. ECS 安装 Docker（Ubuntu 20.04/22.04）

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

docker --version
docker compose version
```

（可选）配置镜像加速：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 3. 拉取代码并准备配置

### 3.1 代码目录

```bash
sudo mkdir -p /opt/xingshuzi
sudo chown -R $USER:$USER /opt/xingshuzi
cd /opt/xingshuzi
git clone <你的仓库地址> .
```

### 3.2 创建生产环境 `.env`

在项目根目录创建 `.env`（**不要提交到 Git**）：

```bash
cd /opt/xingshuzi
cat > .env << 'EOF'
# ===== 基础域名（务必改成你的） =====
SITE_DOMAIN=your-domain.com

# ===== Nuxt 运行时配置（务必改成你的）=====
NUXT_PUBLIC_SITE_URL=https://your-domain.com
NUXT_PUBLIC_API_BASE=https://your-domain.com/api

# ===== MySQL（务必改强密码）=====
MYSQL_ROOT_PASSWORD=MyStrongRootPassword_ChangeMe
MYSQL_DATABASE=xingshuzi

# ===== Flask（生产环境务必改）=====
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
EOF
```

建议生成随机密钥：

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 4. 使用 Docker Compose 启动全栈

本仓库已提供 `web/Dockerfile`、`server/Dockerfile`。我额外提供了根目录的一份组合编排：`docker-compose.ecs.yml`（见下节文件）。

### 4.1 启动（首次会构建镜像）

```bash
cd /opt/xingshuzi
docker compose -f docker-compose.ecs.yml up -d --build
docker compose -f docker-compose.ecs.yml ps
```

### 4.2 初始化数据库 & 管理员

> 首次启动需要等待 MySQL healthcheck 通过（通常 20~60 秒）。

```bash
docker compose -f docker-compose.ecs.yml exec api python3 -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all(); print('db ok')"
docker compose -f docker-compose.ecs.yml exec api python3 init_admin.py
```

（可选）生成示例数据：

```bash
docker compose -f docker-compose.ecs.yml exec api python3 create_sample_data.py
```

### 4.3 验证

```bash
# 服务器本机测试（HTTP，尚未配置 HTTPS 前）
curl -I http://127.0.0.1
curl -sS http://127.0.0.1/api/home/banners | head
```

---

## 5. Nginx 与 HTTPS（Let’s Encrypt）

### 5.1 先用 HTTP 跑通

`docker-compose.ecs.yml` 默认会启动 Nginx 并暴露 `80`。确认域名已解析到该 ECS 后：

- 浏览器打开：`http://your-domain.com/`
- 接口测试：`http://your-domain.com/api/home/banners`

### 5.2 申请 HTTPS 证书

推荐直接在 ECS 上安装 certbot（证书保存在宿主机，再挂载给 Nginx 容器使用）：

```bash
sudo apt update
sudo apt install -y certbot
```

停止 nginx 容器占用 80（只在签发时需要一次）：

```bash
cd /opt/xingshuzi
docker compose -f docker-compose.ecs.yml stop nginx
```

签发证书（standalone 模式，`SITE_DOMAIN` 替换为你的域名；可加 `-d www.xxx.com`）：

```bash
sudo certbot certonly --standalone -d your-domain.com
```

启动 nginx 容器：

```bash
docker compose -f docker-compose.ecs.yml start nginx
```

### 5.3 开启 HTTPS（修改 Nginx 配置）

编辑 `deploy/nginx/xingshuzi.conf`，把 `443 ssl` 段落解注释，并将证书路径改为（Let’s Encrypt 默认）：

- `/etc/letsencrypt/live/your-domain.com/fullchain.pem`
- `/etc/letsencrypt/live/your-domain.com/privkey.pem`

然后重载：

```bash
docker compose -f docker-compose.ecs.yml exec nginx nginx -t
docker compose -f docker-compose.ecs.yml restart nginx
```

### 5.4 证书自动续期

```bash
sudo crontab -e
```

添加（每天凌晨 3 点尝试续期，成功后重启 nginx 容器加载新证书）：

```cron
0 3 * * * certbot renew --quiet && cd /opt/xingshuzi && docker compose -f docker-compose.ecs.yml restart nginx
```

---

## 6. 日常运维

### 6.1 查看日志

```bash
cd /opt/xingshuzi
docker compose -f docker-compose.ecs.yml logs -f --tail=200
docker compose -f docker-compose.ecs.yml logs -f api --tail=200
docker compose -f docker-compose.ecs.yml logs -f web --tail=200
```

### 6.2 更新代码并滚动发布

```bash
cd /opt/xingshuzi
git pull
docker compose -f docker-compose.ecs.yml up -d --build
```

### 6.3 数据库备份

```bash
cd /opt/xingshuzi
mkdir -p /opt/backups
docker compose -f docker-compose.ecs.yml exec mysql mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" > /opt/backups/xingshuzi_$(date +%Y%m%d_%H%M%S).sql
```

---

## 7. 常见问题

### 7.1 页面打不开 / 502

- 看 nginx 日志：`docker compose -f docker-compose.ecs.yml logs -f nginx`
- 看后端日志：`docker compose -f docker-compose.ecs.yml logs -f api`
- 看前端日志：`docker compose -f docker-compose.ecs.yml logs -f web`

### 7.2 数据库连接失败

- 看 mysql 健康检查：`docker compose -f docker-compose.ecs.yml ps`
- 进入 mysql 容器测试：

```bash
docker compose -f docker-compose.ecs.yml exec mysql mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES;"
```

---

## 相关文件

- `docker-compose.ecs.yml`：ECS 全栈编排（web + api + mysql + nginx）
- `deploy/nginx/xingshuzi.conf`：Nginx 反向代理模板（含 /api 转发）
- `web/Dockerfile`、`server/Dockerfile`：镜像构建文件



