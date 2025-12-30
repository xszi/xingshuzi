#!/bin/bash
set -e

echo "=========================================="
echo "开始部署 xingshuzi-back 到生产环境"
echo "=========================================="

# 检查是否为 root 用户
if [ "$EUID" -eq 0 ]; then 
   echo "请不要使用 root 用户运行此脚本"
   exit 1
fi

# 1. 更新系统
echo ""
echo "[1/8] 更新系统..."
sudo apt update -qq

# 2. 安装依赖
echo ""
echo "[2/8] 安装系统依赖..."
sudo apt install -y python3 python3-pip python3-venv git nginx

# 3. 创建项目目录
echo ""
echo "[3/8] 创建项目目录..."
PROJECT_DIR="/opt/xingshuzi-back"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# 4. 复制项目文件（假设脚本在项目根目录运行）
echo ""
echo "[4/8] 复制项目文件..."
if [ -f "run.py" ]; then
    cp -r . $PROJECT_DIR/
    echo "项目文件已复制到 $PROJECT_DIR"
else
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 5. 创建虚拟环境
echo ""
echo "[5/8] 创建虚拟环境..."
cd $PROJECT_DIR
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 6. 安装 Python 依赖
echo ""
echo "[6/8] 安装 Python 依赖..."
pip install --upgrade pip -q
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ -q

# 7. 检查 .env 文件
echo ""
echo "[7/8] 检查配置文件..."
if [ ! -f ".env" ]; then
    echo "警告: .env 文件不存在，请手动创建并配置数据库信息"
    echo "示例 .env 文件内容："
    echo "MYSQL_USER=your_user"
    echo "MYSQL_PASSWORD=your_password"
    echo "MYSQL_HOST=your_host"
    echo "MYSQL_PORT=3306"
    echo "MYSQL_DB=xingshuzi"
    echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
    echo "JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
else
    echo ".env 文件已存在"
    chmod 600 .env
fi

# 8. 初始化数据库
echo ""
echo "[8/8] 初始化数据库..."
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('数据库表创建成功！')" || {
    echo "警告: 数据库初始化失败，请检查数据库配置"
}

# 9. 创建 systemd 服务
echo ""
echo "配置 systemd 服务..."
sudo tee /etc/systemd/system/xingshuzi-back.service > /dev/null <<EOF
[Unit]
Description=xingshuzi-back Flask Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/python3 $PROJECT_DIR/run_prod.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 10. 启动服务
echo ""
echo "启动服务..."
sudo systemctl daemon-reload
sudo systemctl enable xingshuzi-back
sudo systemctl restart xingshuzi-back

# 等待服务启动
sleep 3

# 检查服务状态
if sudo systemctl is-active --quiet xingshuzi-back; then
    echo ""
    echo "=========================================="
    echo "✅ 部署成功！"
    echo "=========================================="
    echo ""
    echo "服务状态:"
    sudo systemctl status xingshuzi-back --no-pager -l
    echo ""
    echo "常用命令:"
    echo "  查看服务状态: sudo systemctl status xingshuzi-back"
    echo "  查看日志: sudo journalctl -u xingshuzi-back -f"
    echo "  重启服务: sudo systemctl restart xingshuzi-back"
    echo "  停止服务: sudo systemctl stop xingshuzi-back"
    echo ""
    echo "API 地址: http://$(hostname -I | awk '{print $1}'):5001"
    echo ""
    echo "下一步:"
    echo "  1. 配置 Nginx 反向代理（参考 DEPLOY.md）"
    echo "  2. 配置 SSL 证书（可选）"
    echo "  3. 配置防火墙规则"
else
    echo ""
    echo "❌ 服务启动失败，请查看日志:"
    echo "   sudo journalctl -u xingshuzi-back -n 50"
    exit 1
fi


