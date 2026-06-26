#!/bin/bash
set -e

echo "========================================="
echo "xingshuzi-back Docker 快速部署脚本"
echo "========================================="

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "请使用 root 用户运行此脚本"
    exit 1
fi

# 1. 更新系统
echo "[1/6] 更新系统..."
apt update && apt upgrade -y

# 2. 安装 Docker
echo "[2/6] 安装 Docker..."
if ! command -v docker &> /dev/null; then
    echo "安装 Docker..."
    apt install -y ca-certificates curl gnupg lsb-release
    
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    systemctl start docker
    systemctl enable docker
    
    echo "Docker 安装完成"
else
    echo "Docker 已安装"
fi

# 验证 Docker Compose
if ! docker compose version &> /dev/null; then
    echo "错误：Docker Compose 未安装"
    exit 1
fi

# 3. 创建项目目录
echo "[3/6] 创建项目目录..."
mkdir -p /opt/xingshuzi-back
cd /opt/xingshuzi-back

# 4. 生成环境变量文件
echo "[4/6] 生成环境变量..."
if [ ! -f .env ]; then
    # 检查 Python3 是否安装
    if ! command -v python3 &> /dev/null; then
        apt install -y python3
    fi
    
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    cat > .env << EOF
MYSQL_USER=root
MYSQL_PASSWORD=MyStrongRootPassword123
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DB=xingshuzi
SECRET_KEY=$SECRET_KEY
JWT_SECRET_KEY=$JWT_SECRET_KEY
EOF
    echo "✓ .env 文件已创建"
else
    echo "✓ .env 文件已存在"
fi

# 5. 启动服务
echo "[5/6] 启动 Docker 服务..."
if [ -f docker-compose.yml ]; then
    docker compose up -d
    echo "✓ Docker 服务已启动"
else
    echo "错误：未找到 docker-compose.yml 文件"
    echo "请确保项目文件已上传到 /opt/xingshuzi-back 目录"
    exit 1
fi

# 6. 等待 MySQL 启动并初始化数据库
echo "[6/6] 初始化数据库..."
echo "等待 MySQL 启动（30秒）..."
sleep 30

echo "创建数据库表..."
docker compose exec -T app python3 << 'PYTHON_EOF'
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    db.create_all()
    print('数据库表创建成功！')
PYTHON_EOF

echo "创建管理员账号..."
docker compose exec -T app python3 init_admin.py || echo "管理员账号可能已存在"

echo ""
echo "========================================="
echo "✅ 部署完成！"
echo "========================================="
echo ""

# 获取服务器 IP
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')
echo "🌐 服务地址: http://$SERVER_IP:5000"
echo "👤 管理员账号: admin"
echo "🔑 管理员密码: admin123"
echo ""
echo "📝 常用命令:"
echo "  查看日志: cd /opt/xingshuzi-back && docker compose logs -f"
echo "  停止服务: cd /opt/xingshuzi-back && docker compose stop"
echo "  启动服务: cd /opt/xingshuzi-back && docker compose start"
echo "  重启服务: cd /opt/xingshuzi-back && docker compose restart"
echo "  查看状态: cd /opt/xingshuzi-back && docker compose ps"
echo ""
echo "⚠️  重要提醒:"
echo "  1. 请立即修改管理员密码"
echo "  2. 检查防火墙/安全组是否开放 5000 端口"
echo "  3. 建议配置 Nginx 反向代理"
echo ""
