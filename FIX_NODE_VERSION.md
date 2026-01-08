# 修复 Node.js 版本问题

## 问题说明

项目需要 Node.js >= 20.19.0，但当前使用的是 v20.6.0，导致以下错误：
- `Cannot redefine property: File` (@babel/core 错误)
- `Loading @nuxt/vite-builder builder failed`

## 解决方案

### 方法 1: 使用 Homebrew 安装最新 Node.js（推荐）

```bash
# 安装 Node.js 20 LTS 最新版本
brew install node@20

# 或者安装最新 LTS 版本
brew install node@22
```

### 方法 2: 从官网下载安装

访问 https://nodejs.org/ 下载并安装 Node.js 20.19.0 或更高版本。

### 方法 3: 安装真正的 nvm 来管理版本

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 重新加载 shell 配置
source ~/.zshrc

# 安装 Node.js 20.19.0
nvm install 20.19.0

# 使用新版本
nvm use 20.19.0
```

## 验证安装

安装完成后，验证版本：

```bash
node -v  # 应该显示 v20.19.0 或更高
npm -v
```

## 重新安装项目依赖

升级 Node.js 后，清理并重新安装依赖：

```bash
# 清理缓存和构建文件
rm -rf node_modules .nuxt .output .cache

# 重新安装依赖（使用 npm）
npm install

# 或者使用 pnpm（如果已安装）
pnpm install
```

## 启动开发服务器

```bash
npm run dev
```



