# 星书子项目 Docker 分开部署指南（Git方式）

本文档用于在阿里云ECS (Ubuntu)上通过Docker分开部署server和web项目，使用Git获取代码，使用IP访问（无域名）。

## 📋 部署架构

```
阿里云ECS Ubuntu (120.76.247.123)
├── Git仓库克隆
├── Flask后端 (Docker容器)
│   └── 端口: 5001
│   └── 访问: http://120.76.247.123:5001/api
│
└── Nuxt前端 (Docker容器)
    └── 端口: 3000
    └── 访问: http://120.76.247.123:3000
    └── 连接API: http://120.76.247.123:5001/api

线上MySQL数据库 (120.76.247.123:3306)
```

## 🚀 快速部署

### 前置条件

1. **ECS配置**
   - Ubuntu 20.04 或 22.04
   - 2核4GB内存（最低）
   - 已安装Docker、Docker Compose、Git

2. **安全组配置**
   - 开放端口: 22 (SSH), 3000 (Web), 5001 (API)

3. **数据库**
   - MySQL 8.0运行在120.76.247.123:3306
   - 数据库名: xingshuzi

4. **Git仓库**
   - 代码已推送到Git仓库（GitHub/Gitee等）
   - 确保ECS可以访问Git仓库

---

## 📦 一、环境准备（仅需执行一次）

### 1.1 SSH登录ECS

```bash
ssh root@120.76.247.123
```

### 1.2 安装Docker和Docker Compose

```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com | sh

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
docker compose version
```

### 1.3 安装Git

```bash
# 安装Git
sudo apt install git -y

# 验证安装
git --version

# 配置Git（可选）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 1.4 配置Git访问权限（如果是私有仓库）

**使用SSH密钥方式（推荐）：**

```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
# 按回车使用默认路径，可以设置密码或直接回车

# 查看公钥
cat ~/.ssh/id_rsa.pub

# 复制公钥内容，添加到Git仓库的SSH Keys中
# GitHub: Settings → SSH and GPG keys → New SSH key
# Gitee: 设置 → SSH公钥 → 添加公钥
```

**或使用Personal Access Token方式：**

```bash
# 克隆时使用token
git clone https://用户名:TOKEN@github.com/用户名/仓库名.git
```

---

## 📦 二、首次部署

### 2.1 克隆代码仓库

```bash
# SSH登录ECS
ssh root@120.76.247.123

# 进入工作目录
cd /root

# 克隆代码（替换为你的仓库地址）
git clone git@github.com:your-username/xingshuzi.git
# 或使用HTTPS: git clone https://github.com/your-username/xingshuzi.git

# 进入项目目录
cd xingshuzi
```

### 2.2 部署Flask后端

```bash
# 进入server目录
cd /root/xingshuzi/server

# 配置环境变量
cp .env.example .env

# 编辑配置（如需修改）
nano .env

# 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

部署完成后，后端将运行在：
- 内部: http://localhost:5001
- 外部: http://120.76.247.123:5001/api

**验证后端：**
```bash
curl http://localhost:5001/api/home/banners
# 应该返回: {"code":200,"data":[],"msg":"success"}
```

### 2.3 部署Nuxt前端

```bash
# 进入web目录
cd /root/xingshuzi/web

# 运行部署脚本（构建需要5-10分钟）
chmod +x deploy.sh
./deploy.sh
```

部署完成后，前端将运行在：
- 外部: http://120.76.247.123:3000

**验证前端：**
```bash
curl -I http://localhost:3000
# 应该返回: HTTP/1.1 200 OK
```

---

## 🔄 三、更新部署（使用Git）

### 3.1 更新后端

```bash
# SSH登录ECS
ssh root@120.76.247.123

# 进入项目目录
cd /root/xingshuzi

# 拉取最新代码
git pull origin main
# 或: git pull origin master

# 重新部署后端
cd server
./deploy.sh
```

### 3.2 更新前端

```bash
# SSH登录ECS
ssh root@120.76.247.123

# 进入项目目录
cd /root/xingshuzi

# 拉取最新代码（如果还未拉取）
git pull origin main

# 重新部署前端
cd web
./deploy.sh
```

### 3.3 仅更新某个服务

**只更新后端：**
```bash
cd /root/xingshuzi
git pull origin main
cd server && ./deploy.sh
```

**只更新前端：**
```bash
cd /root/xingshuzi
git pull origin main
cd web && ./deploy.sh
```

---

## 🌐 访问地址

### 前端访问
- **首页**: http://120.76.247.123:3000
- **登录**: http://120.76.247.123:3000/login
- **后台**: http://120.76.247.123:3000/admin

### 后端API
- **API基础地址**: http://120.76.247.123:5001/api
- **健康检查**: http://120.76.247.123:5001/api/home/banners

### 默认账号
- 用户名: `admin`
- 密码: `admin123`

---

## 🔧 管理命令

### Flask后端管理

```bash
cd /root/xingshuzi/server

# 查看日志
docker compose logs -f

# 查看容器状态
docker compose ps

# 重启服务
docker compose restart

# 停止服务
docker compose down

# 重新部署
./deploy.sh
```

### Nuxt前端管理

```bash
cd /root/xingshuzi/web

# 查看日志
docker compose logs -f

# 查看容器状态
docker compose ps

# 重启服务
docker compose restart

# 停止服务
docker compose down

# 重新部署
./deploy.sh
```

### Git相关命令

```bash
cd /root/xingshuzi

# 查看当前分支
git branch

# 切换分支
git checkout develop

# 查看状态
git status

# 查看最新提交
git log -5 --oneline

# 拉取最新代码
git pull origin main

# 放弃本地修改（谨慎使用）
git reset --hard HEAD
git pull origin main
```

---

## 📁 文件结构

```
/root/xingshuzi/                # Git仓库根目录
├── .git/                       # Git版本控制
├── server/                     # Flask后端
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .dockerignore
│   ├── .env.example
│   ├── .env                    # 需手动创建
│   ├── deploy.sh
│   ├── app/
│   ├── config/
│   ├── requirements.txt
│   └── run.py
├── web/                        # Nuxt前端
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .dockerignore
│   ├── deploy.sh
│   ├── app/
│   ├── package.json
│   └── nuxt.config.ts
└── DEPLOY_README.md           # 本文档
```

---

## ⚙️ 配置说明

### Backend配置 (.env)

```bash
# 编辑配置
cd /root/xingshuzi/server
nano .env
```

配置内容：
```env
# MySQL数据库
MYSQL_HOST=120.76.247.123
MYSQL_PORT=3306
MYSQL_DB=xingshuzi
MYSQL_USER=root
MYSQL_PASSWORD=MyStrongRootPassword123

# Flask密钥
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

### Frontend配置

前端API地址已在Dockerfile中配置：
- `NUXT_PUBLIC_API_BASE=http://120.76.247.123:5001/api`

如需修改，编辑 `web/Dockerfile` 第17行。

---

## 🐛 故障排查

### 1. Git克隆失败

```bash
# 检查网络连接
ping github.com

# 检查SSH密钥
ssh -T git@github.com

# 如果SSH失败，使用HTTPS
git clone https://github.com/your-username/xingshuzi.git

# 如果是私有仓库，需要输入用户名和密码/token
```

### 2. Git权限问题

```bash
# 确保SSH密钥已添加到Git平台
cat ~/.ssh/id_rsa.pub

# 测试GitHub连接
ssh -T git@github.com
# 应显示: Hi username! You've successfully authenticated...

# 测试Gitee连接
ssh -T git@gitee.com
```

### 3. 后端无法启动

```bash
# 查看日志
cd /root/xingshuzi/server
docker compose logs

# 检查端口占用
netstat -tlnp | grep 5001

# 检查数据库连接
docker compose exec api python3 -c "from app import create_app; app = create_app(); print('OK')"
```

### 4. 前端无法访问

```bash
# 查看日志
cd /root/xingshuzi/web
docker compose logs

# 检查端口占用
netstat -tlnp | grep 3000

# 检查容器状态
docker compose ps
```

### 5. 代码更新后未生效

```bash
# 确保拉取了最新代码
cd /root/xingshuzi
git pull origin main

# 重新构建镜像
cd server  # 或 cd web
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## 📝 Git工作流程建议

### 开发流程

```bash
# 本地开发完成后
git add .
git commit -m "feature: 添加新功能"
git push origin main

# ECS服务器更新
ssh root@120.76.247.123
cd /root/xingshuzi
git pull origin main

# 重新部署变更的服务
cd server && ./deploy.sh  # 如果后端有变更
cd web && ./deploy.sh     # 如果前端有变更
```

### 分支管理（可选）

```bash
# 使用develop分支开发
git checkout -b develop
git push origin develop

# ECS服务器切换到develop分支
ssh root@120.76.247.123
cd /root/xingshuzi
git fetch origin
git checkout develop
git pull origin develop

# 测试完成后合并到main
git checkout main
git merge develop
git push origin main
```

### 回滚到之前版本

```bash
# 查看提交历史
cd /root/xingshuzi
git log --oneline -10

# 回滚到指定版本
git reset --hard <commit-id>

# 重新部署
cd server && ./deploy.sh
cd web && ./deploy.sh

# 如果需要强制推送（谨慎使用）
git push origin main --force
```

---

## 🔐 安全建议

### 1. 保护.env文件

```bash
# 确保.env不被提交到Git
cd /root/xingshuzi
echo ".env" >> .gitignore
echo "server/.env" >> .gitignore

# 验证.gitignore
git status
```

### 2. 使用SSH密钥

```bash
# 生成专用的部署密钥
ssh-keygen -t rsa -b 4096 -f ~/.ssh/deploy_key
# 将deploy_key.pub添加到Git仓库的Deploy Keys

# 使用指定密钥克隆
GIT_SSH_COMMAND="ssh -i ~/.ssh/deploy_key" git clone git@github.com:user/repo.git
```

### 3. 定期更新系统

```bash
# 更新Ubuntu系统
sudo apt update
sudo apt upgrade -y

# 更新Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

---

## 📊 自动化部署脚本（可选）

创建一个自动拉取和部署的脚本：

```bash
# 创建自动部署脚本
cat > /root/auto_deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "开始自动部署..."

# 进入项目目录
cd /root/xingshuzi

# 记录当前提交
OLD_COMMIT=$(git rev-parse HEAD)

# 拉取最新代码
echo "拉取最新代码..."
git pull origin main

# 获取新提交
NEW_COMMIT=$(git rev-parse HEAD)

# 检查是否有更新
if [ "$OLD_COMMIT" = "$NEW_COMMIT" ]; then
    echo "没有新的更新"
    exit 0
fi

echo "发现新的更新，开始部署..."

# 检查哪些文件变更
CHANGED_FILES=$(git diff --name-only $OLD_COMMIT $NEW_COMMIT)

# 判断是否需要重新部署后端
if echo "$CHANGED_FILES" | grep -q "^server/"; then
    echo "后端有变更，重新部署..."
    cd /root/xingshuzi/server
    ./deploy.sh
fi

# 判断是否需要重新部署前端
if echo "$CHANGED_FILES" | grep -q "^web/"; then
    echo "前端有变更，重新部署..."
    cd /root/xingshuzi/web
    ./deploy.sh
fi

echo "自动部署完成！"
EOF

# 添加执行权限
chmod +x /root/auto_deploy.sh

# 测试运行
/root/auto_deploy.sh
```

### 设置定时自动部署（可选）

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每10分钟检查一次）
*/10 * * * * /root/auto_deploy.sh >> /root/deploy.log 2>&1

# 或每天凌晨2点部署
0 2 * * * /root/auto_deploy.sh >> /root/deploy.log 2>&1

# 查看部署日志
tail -f /root/deploy.log
```

---

## 📊 性能监控（可选）

### 查看容器资源使用

```bash
# 查看所有容器资源使用
docker stats

# 查看特定容器
docker stats xingshuzi-api xingshuzi-web
```

### 查看日志

```bash
# 实时查看后端日志
docker logs -f xingshuzi-api

# 实时查看前端日志
docker logs -f xingshuzi-web

# 查看最近100行
docker logs --tail 100 xingshuzi-api
```

---

## ✅ 部署检查清单

### 首次部署前
- [ ] ECS已安装Docker、Docker Compose、Git
- [ ] 安全组已开放3000和5001端口
- [ ] MySQL数据库可访问
- [ ] Git仓库可访问（SSH密钥或Token已配置）
- [ ] 代码已推送到Git仓库

### 首次部署后
- [ ] 成功克隆Git仓库
- [ ] 后端API正常响应
- [ ] 前端页面可访问
- [ ] 前端可以调用后端API
- [ ] 登录功能正常

### 更新部署
- [ ] git pull成功拉取最新代码
- [ ] 变更的服务已重新部署
- [ ] 服务正常运行

---

## 🎯 快速命令参考

```bash
# === Git操作 ===
cd /root/xingshuzi
git pull origin main              # 拉取最新代码
git status                        # 查看状态
git log -5 --oneline             # 查看最近5次提交

# === 部署后端 ===
cd /root/xingshuzi/server
./deploy.sh                      # 部署

# === 部署前端 ===
cd /root/xingshuzi/web
./deploy.sh                      # 部署

# === 查看日志 ===
docker logs -f xingshuzi-api     # 后端日志
docker logs -f xingshuzi-web     # 前端日志

# === 管理容器 ===
docker ps                         # 查看运行中的容器
docker compose ps                 # 查看项目容器
docker compose restart            # 重启服务
docker compose down               # 停止服务

# === 系统管理 ===
docker system prune -a            # 清理无用镜像（谨慎）
df -h                            # 查看磁盘使用
free -h                          # 查看内存使用
```

---

## 🎯 总结

使用Git方式部署的优势：

- ✅ **版本控制** - 完整的代码版本历史
- ✅ **快速更新** - git pull即可获取最新代码
- ✅ **易于回滚** - 可以轻松回滚到任意版本
- ✅ **团队协作** - 多人可以协同开发和部署
- ✅ **分支管理** - 支持开发、测试、生产环境分离
- ✅ **自动化** - 可以配置自动部署脚本

**访问地址**: http://120.76.247.123:3000

**部署完成后即可使用！** 🎉
