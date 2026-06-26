#!/bin/bash
set -e

echo "=========================================="
echo "  Nuxt前端 简化部署脚本"
echo "=========================================="

# 停止旧容器
echo "🛑 停止旧容器..."
docker compose down 2>/dev/null || true

# 清理
echo "🧹 清理Docker资源..."
docker system prune -f

# 检查磁盘空间
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "⚠️  磁盘使用率较高: ${DISK_USAGE}%"
    echo "清理Docker镜像..."
    docker image prune -a -f
fi

# 检查内存
FREE_MEM=$(free -m | grep Mem | awk '{print $7}')
echo "📊 可用内存: ${FREE_MEM}MB"

if [ $FREE_MEM -lt 1000 ]; then
    echo "⚠️  可用内存不足1GB，构建可能会很慢"
    echo "建议选择方案2：在服务器上直接构建"
fi

echo ""
echo "开始构建（这可能需要5-10分钟）..."
echo "如果长时间无响应，请按 Ctrl+C 停止"
echo ""

# 设置构建超时
export COMPOSE_HTTP_TIMEOUT=600
export DOCKER_CLIENT_TIMEOUT=600

# 构建并启动
docker compose build \
  --build-arg NODE_OPTIONS="--max-old-space-size=2048" \
  --progress=plain

echo ""
echo "🚀 启动容器..."
docker compose up -d

# 等待启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查状态
if docker ps | grep -q xingshuzi-web; then
    echo ""
    echo "=========================================="
    echo "  ✅ 部署成功！"
    echo "=========================================="
    echo "访问地址: http://120.76.247.123:3000"
    echo ""
    echo "查看日志:"
    echo "  docker logs -f xingshuzi-web"
    echo "=========================================="
else
    echo ""
    echo "❌ 容器启动失败，查看日志:"
    docker compose logs
fi

