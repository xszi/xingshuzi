FROM node:20-alpine AS builder

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 使用淘宝npm镜像加速（国内部署）
RUN npm config set registry https://registry.npmmirror.com

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

# 设置环境变量
ENV NUXT_PUBLIC_API_BASE=http://120.76.247.123:5001/api

# 构建Nuxt应用
RUN npm run build

# 生产环境镜像
FROM node:20-alpine

WORKDIR /app

# 复制构建产物
COPY --from=builder /app/.output /app/.output

# 暴露端口
EXPOSE 3000

# 设置环境变量
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

# 启动命令（使用node用户，Alpine镜像已内置）
USER node

CMD ["node", ".output/server/index.mjs"]

