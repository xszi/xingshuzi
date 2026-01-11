# Git仓库配置指南

本文档说明如何将星书子项目推送到Git仓库，以便在ECS上通过Git方式部署。

## 📋 选择Git平台

推荐使用以下Git平台之一：

1. **GitHub** (https://github.com)
   - 全球最大的代码托管平台
   - 适合开源项目
   - 私有仓库需要付费（或免费有限制）

2. **Gitee** (https://gitee.com)
   - 国内访问速度快
   - 免费私有仓库
   - 适合国内部署

3. **GitLab** (https://gitlab.com)
   - 功能强大
   - 免费私有仓库
   - 支持CI/CD

## 🚀 首次推送到Git仓库

### 方案一：使用GitHub

#### 1. 在GitHub创建仓库

1. 登录 https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - Repository name: `xingshuzi`
   - Description: `星书子项目`
   - 选择 `Private` 或 `Public`
4. 不要勾选 "Initialize this repository with a README"
5. 点击 "Create repository"

#### 2. 推送代码到GitHub

```bash
# 进入项目目录
cd /Users/jiuhua-pc/Desktop/xingshuzi

# 初始化Git（如果还未初始化）
git init

# 添加远程仓库
git remote add origin git@github.com:your-username/xingshuzi.git
# 或使用HTTPS: git remote add origin https://github.com/your-username/xingshuzi.git

# 查看当前状态
git status

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 星书子项目首次提交"

# 推送到远程仓库
git push -u origin main
# 如果是master分支: git push -u origin master
```

### 方案二：使用Gitee（国内推荐）

#### 1. 在Gitee创建仓库

1. 登录 https://gitee.com
2. 点击右上角 "+" → "新建仓库"
3. 填写仓库信息：
   - 仓库名称: `xingshuzi`
   - 仓库介绍: `星书子项目`
   - 选择 `私有` 或 `开源`
4. 不要勾选 "使用Readme文件初始化这个仓库"
5. 点击 "创建"

#### 2. 推送代码到Gitee

```bash
# 进入项目目录
cd /Users/jiuhua-pc/Desktop/xingshuzi

# 初始化Git（如果还未初始化）
git init

# 添加远程仓库
git remote add origin git@gitee.com:your-username/xingshuzi.git
# 或使用HTTPS: git remote add origin https://gitee.com/your-username/xingshuzi.git

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 星书子项目首次提交"

# 推送到远程仓库
git push -u origin master
```

## 🔐 配置SSH密钥（推荐）

使用SSH密钥可以避免每次推送都输入密码。

### 1. 生成SSH密钥（本地Mac）

```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# 按提示操作：
# - 按回车使用默认路径 (~/.ssh/id_rsa)
# - 可以设置密码或直接回车

# 查看公钥
cat ~/.ssh/id_rsa.pub
```

### 2. 添加公钥到GitHub

1. 复制 `~/.ssh/id_rsa.pub` 的内容
2. 登录 GitHub
3. 点击头像 → Settings → SSH and GPG keys
4. 点击 "New SSH key"
5. Title: `Mac电脑` （可自定义）
6. Key: 粘贴公钥内容
7. 点击 "Add SSH key"

### 3. 添加公钥到Gitee

1. 复制 `~/.ssh/id_rsa.pub` 的内容
2. 登录 Gitee
3. 点击头像 → 设置 → SSH公钥
4. 标题: `Mac电脑` （可自定义）
5. 公钥: 粘贴公钥内容
6. 点击 "确定"

### 4. 测试SSH连接

```bash
# 测试GitHub
ssh -T git@github.com
# 成功会显示: Hi username! You've successfully authenticated...

# 测试Gitee
ssh -T git@gitee.com
# 成功会显示: Hi username! You've successfully authenticated...
```

## 📝 .gitignore 配置

确保敏感文件不被提交到Git仓库：

```bash
# 查看当前.gitignore
cat /Users/jiuhua-pc/Desktop/xingshuzi/.gitignore
```

应该包含以下内容：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg
*.egg-info/
dist/
build/

# 环境变量
.env
.env.local
server/.env

# Node.js
node_modules/
.nuxt/
.output/
dist/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# 日志
*.log
logs/
```

## 🔄 日常Git操作

### 提交代码

```bash
cd /Users/jiuhua-pc/Desktop/xingshuzi

# 查看修改
git status

# 添加修改的文件
git add .

# 或添加特定文件
git add server/app/routes/auth.py
git add web/app/pages/login.vue

# 提交
git commit -m "feat: 添加登录功能"

# 推送到远程
git push origin main
```

### 拉取最新代码

```bash
# 拉取最新代码
git pull origin main

# 或先fetch再merge
git fetch origin
git merge origin/main
```

### 查看历史

```bash
# 查看提交历史
git log --oneline -10

# 查看详细历史
git log -5

# 查看某个文件的历史
git log -- server/app/routes/auth.py
```

### 创建分支

```bash
# 创建并切换到新分支
git checkout -b develop

# 推送新分支到远程
git push -u origin develop

# 切换回main分支
git checkout main
```

## 🔗 在ECS上配置Git访问

### 1. ECS生成SSH密钥

```bash
# SSH登录ECS
ssh root@120.76.247.123

# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "ecs@xingshuzi.com"

# 查看公钥
cat ~/.ssh/id_rsa.pub
```

### 2. 添加ECS公钥到Git平台

将ECS的公钥添加到GitHub或Gitee（步骤同上）

### 3. 测试ECS的Git连接

```bash
# 在ECS上测试
ssh -T git@github.com
# 或
ssh -T git@gitee.com
```

### 4. 克隆仓库

```bash
# SSH方式
cd /root
git clone git@github.com:your-username/xingshuzi.git

# HTTPS方式（需要输入用户名密码）
git clone https://github.com/your-username/xingshuzi.git
```

## 🛡️ 安全建议

### 1. 使用Deploy Keys（推荐）

为ECS创建专用的部署密钥，只有读取权限：

#### GitHub:
1. 仓库页面 → Settings → Deploy keys
2. 点击 "Add deploy key"
3. 粘贴ECS的公钥
4. 勾选 "Allow write access" （如果需要）
5. 点击 "Add key"

#### Gitee:
1. 仓库页面 → 管理 → 部署公钥管理
2. 点击 "添加部署公钥"
3. 粘贴ECS的公钥
4. 点击 "确定"

### 2. 使用Personal Access Token

如果使用HTTPS方式，可以使用Personal Access Token代替密码：

#### GitHub:
1. Settings → Developer settings → Personal access tokens
2. 点击 "Generate new token"
3. 设置权限：`repo` (完整控制)
4. 生成并保存token

#### Gitee:
1. 设置 → 私人令牌
2. 点击 "生成新令牌"
3. 设置权限
4. 生成并保存token

使用token克隆：
```bash
git clone https://用户名:TOKEN@github.com/用户名/xingshuzi.git
```

### 3. 保护敏感文件

```bash
# 确保.env文件被忽略
echo ".env" >> .gitignore
echo "server/.env" >> .gitignore

# 如果.env已被提交，从Git历史中删除
git rm --cached server/.env
git commit -m "Remove .env from git"
git push origin main
```

## 📊 Git工作流建议

### 简单流程（单人开发）

```
main (生产) ← 直接提交和部署
```

### 标准流程（团队协作）

```
main (生产)
  ↑
develop (开发) ← 日常开发
  ↑
feature/* (功能分支) ← 新功能开发
```

工作步骤：
```bash
# 1. 创建功能分支
git checkout -b feature/user-login

# 2. 开发并提交
git add .
git commit -m "feat: 实现用户登录"

# 3. 推送功能分支
git push origin feature/user-login

# 4. 合并到develop
git checkout develop
git merge feature/user-login

# 5. 测试通过后合并到main
git checkout main
git merge develop
git push origin main

# 6. ECS部署
ssh root@120.76.247.123
cd /root/xingshuzi
git pull origin main
cd server && ./deploy.sh
```

## ✅ 检查清单

推送代码前：
- [ ] 确保.gitignore配置正确
- [ ] .env文件已被忽略
- [ ] 敏感信息已删除或加密
- [ ] 代码已测试无误

首次推送：
- [ ] 已创建Git仓库
- [ ] 已配置SSH密钥
- [ ] 成功推送代码
- [ ] 远程仓库可访问

ECS配置：
- [ ] ECS已生成SSH密钥
- [ ] ECS公钥已添加到Git平台
- [ ] 成功克隆仓库
- [ ] 可以git pull拉取代码

## 🎯 快速命令参考

```bash
# === 本地操作 ===
git status                          # 查看状态
git add .                          # 添加所有修改
git commit -m "message"            # 提交
git push origin main               # 推送

# === ECS操作 ===
cd /root/xingshuzi
git pull origin main               # 拉取最新代码
cd server && ./deploy.sh           # 部署后端
cd web && ./deploy.sh             # 部署前端

# === 查看和管理 ===
git log --oneline -10             # 查看历史
git remote -v                     # 查看远程仓库
git branch -a                     # 查看所有分支
```

---

**配置完成后，即可使用Git方式在ECS上部署！** 🎉

