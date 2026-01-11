#!/bin/bash

set -e

echo "=========================================="
echo "  Nuxt前端服务 Docker 部署脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker未安装${NC}"
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo -e "${RED}错误: Docker Compose未安装${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker和Docker Compose已安装"

echo ""
echo "=========================================="
echo "  开始部署Nuxt前端..."
echo "=========================================="
echo ""

# 停止旧容器
echo "1. 停止旧容器..."
docker compose down 2>/dev/null || true

# 构建镜像（前端构建较慢）
echo ""
echo "2. 构建Docker镜像（约需5-10分钟）..."
docker compose build --no-cache

# 启动服务
echo ""
echo "3. 启动服务..."
docker compose up -d

# 等待服务启动
echo ""
echo "4. 等待服务启动..."
sleep 15

# 检查服务状态
echo ""
echo "5. 检查服务状态..."
docker compose ps

# 健康检查
echo ""
echo "6. 健康检查..."
if curl -I http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Web服务正常${NC}"
else
    echo -e "${YELLOW}⚠ Web服务可能未就绪，请查看日志${NC}"
fi

echo ""
echo "=========================================="
echo -e "  ${GREEN}部署完成！${NC}"
echo "=========================================="
echo ""
echo "服务信息:"
echo "  容器名称: xingshuzi-web"
echo "  端口: 3000"
echo "  访问地址: http://120.76.247.123:3000"
echo "  API地址: http://120.76.247.123:5001/api"
echo ""
echo "常用命令:"
echo "  查看日志: docker compose logs -f"
echo "  重启服务: docker compose restart"
echo "  停止服务: docker compose down"
echo ""
echo -e "${YELLOW}注意: 确保ECS安全组已开放3000端口${NC}"
echo ""

