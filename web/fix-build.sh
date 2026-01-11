#!/bin/bash
set -e

echo "=========================================="
echo "  Nuxt前端 修复构建脚本"
echo "=========================================="

# 停止所有构建
echo "🛑 停止当前构建..."
docker compose down 2>/dev/null || true
docker stop $(docker ps -aq) 2>/dev/null || true

# 清理构建缓存
echo "🧹 清理Docker缓存..."
docker builder prune -f

# 检查系统资源
echo ""
echo "📊 系统资源检查:"
echo "内存使用:"
free -h | grep Mem
echo ""
echo "磁盘使用:"
df -h | grep -E "/$|/var"
echo ""

# 询问用户选择
echo "=========================================="
echo "请选择构建方式："
echo "=========================================="
echo "1. 使用优化版Dockerfile构建（推荐）"
echo "2. 在服务器上直接构建（不使用Docker多阶段）"
echo "3. 跳过构建，使用开发模式运行"
echo ""
read -p "请选择 [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "📦 使用优化版Dockerfile构建..."
        docker compose build --build-arg NODE_OPTIONS="--max-old-space-size=2048"
        docker compose up -d
        ;;
    2)
        echo ""
        echo "📦 直接在服务器构建..."
        
        # 停止旧容器
        docker compose down
        
        # 在服务器上构建
        npm config set registry https://registry.npmmirror.com
        npm ci
        NODE_OPTIONS="--max-old-space-size=2048" npm run build
        
        # 使用已构建的文件启动
        docker compose up -d
        ;;
    3)
        echo ""
        echo "⚠️  使用开发模式（不推荐生产环境）..."
        
        # 创建临时开发Dockerfile
        cat > Dockerfile.dev << 'EOF'
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm config set registry https://registry.npmmirror.com
RUN npm install

COPY . .

ENV NUXT_PUBLIC_API_BASE=http://120.76.247.123:5001/api
EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
EOF
        
        docker build -f Dockerfile.dev -t xingshuzi-web-dev .
        docker run -d -p 3000:3000 --name xingshuzi-web xingshuzi-web-dev
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "  部署完成"
echo "=========================================="
echo "访问地址: http://120.76.247.123:3000"
echo ""
echo "查看日志:"
echo "  docker logs -f xingshuzi-web"
echo "=========================================="

