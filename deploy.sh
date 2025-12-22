#!/bin/bash
# 服务器部署脚本
# 使用方法: bash deploy.sh

set -e

echo "🚀 开始部署行书子项目..."

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到 Node.js，请先安装 Node.js${NC}"
    exit 1
fi

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到 npm，请先安装 npm${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js 版本: $(node -v)${NC}"
echo -e "${GREEN}✅ npm 版本: $(npm -v)${NC}"

# 安装依赖
echo -e "${YELLOW}📦 安装依赖...${NC}"
npm ci --production=false

# 构建项目
echo -e "${YELLOW}🔨 构建生产版本...${NC}"
npm run build

# 检查 PM2
if command -v pm2 &> /dev/null; then
    echo -e "${YELLOW}🔄 使用 PM2 重启应用...${NC}"
    
    # 如果应用已运行，先停止
    if pm2 list | grep -q "xingshuzi"; then
        echo -e "${YELLOW}⏹️  停止现有应用...${NC}"
        pm2 stop xingshuzi || true
        pm2 delete xingshuzi || true
    fi
    
    # 启动应用
    echo -e "${GREEN}▶️  启动应用...${NC}"
    pm2 start ecosystem.config.cjs
    
    # 保存 PM2 配置
    pm2 save
    
    echo -e "${GREEN}✅ 部署完成！${NC}"
    echo -e "${GREEN}📊 查看状态: pm2 status${NC}"
    echo -e "${GREEN}📋 查看日志: pm2 logs xingshuzi${NC}"
else
    echo -e "${YELLOW}⚠️  未找到 PM2，使用 npm start 启动...${NC}"
    echo -e "${YELLOW}💡 建议安装 PM2: npm install -g pm2${NC}"
    npm run start
fi


