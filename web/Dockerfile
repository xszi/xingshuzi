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

# 复制构建产物和package文件
COPY --from=builder /app/.output /app/.output
COPY --from=builder /app/package*.json ./

# 使用淘宝npm镜像加速
RUN npm config set registry https://registry.npmmirror.com

# 只安装生产依赖
RUN npm ci --production

# 创建非root用户
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

# 暴露端口
EXPOSE 3000

# 设置环境变量
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

# 启动命令
CMD ["node", ".output/server/index.mjs"]

