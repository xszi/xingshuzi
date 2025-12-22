# 星数字 (XingShuZi)

一个基于 Nuxt 4 的服务端渲染 (SSR) PC 端应用项目。

## 项目特性

- ✅ **服务端渲染 (SSR)** - 基于 Nuxt 的服务端渲染，提供更好的 SEO 和首屏加载性能
- ✅ **TypeScript 支持** - 完整的 TypeScript 支持，提供类型安全
- ✅ **现代化 UI** - 响应式设计，适配 PC 端
- ✅ **开发工具** - 集成 Nuxt DevTools，提升开发体验

## 技术栈

- [Nuxt 4](https://nuxt.com/) - 全栈 Vue 框架
- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [TypeScript](https://www.typescriptlang.org/) - 类型安全的 JavaScript
- [Vue Router](https://router.vuejs.org/) - Vue.js 官方路由管理器

## Setup

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## 本地部署

### 构建生产版本

构建应用的生产版本：

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

### 启动本地生产服务器

构建完成后，可以使用以下任一方式启动本地生产服务器：

**方式 1: 使用 npm 脚本（推荐）**
```bash
npm run start
```

**方式 2: 使用 Nuxt 预览命令**
```bash
npm run preview
```

**方式 3: 使用启动脚本**
- Windows (CMD): 双击 `start-server.bat` 或运行 `start-server.bat`
- Windows (PowerShell): 运行 `.\start-server.ps1`
- 跨平台: 运行 `node start-server.js`

**方式 4: 直接运行服务器文件**
```bash
node .output/server/index.mjs
```

服务器启动后，访问 **http://localhost:3000** 查看应用。

### 停止服务器

在运行服务器的终端中按 `Ctrl + C` 停止服务器。

## 部署到生产环境

### 快速开始

详细的服务器部署指南请查看 [DEPLOY.md](./DEPLOY.md)

### 部署方式概览

1. **PM2 部署（推荐）** - 适合大多数场景，简单易用
   ```bash
   npm ci
   npm run build
   pm2 start ecosystem.config.cjs
   ```

2. **Docker 部署** - 适合容器化环境
   ```bash
   docker build -t xingshuzi .
   docker run -d -p 3000:3000 xingshuzi
   ```

3. **systemd 部署** - 适合 Linux 系统服务

### 部署文件说明

- `ecosystem.config.cjs` - PM2 配置文件
- `nginx.conf.example` - Nginx 反向代理配置示例
- `Dockerfile` - Docker 镜像构建文件
- `docker-compose.yml` - Docker Compose 配置
- `deploy.sh` - 自动化部署脚本
- `DEPLOY.md` - 详细部署文档

### 相关资源

- [详细部署指南](./DEPLOY.md)
- [Nuxt 部署文档](https://nuxt.com/docs/getting-started/deployment)
