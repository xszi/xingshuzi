#!/bin/bash
set -e

echo "=========================================="
echo "  MySQL数据库 Docker部署"
echo "=========================================="

# 检查文件
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 错误: docker-compose.yml 不存在"
    exit 1
fi

if [ ! -f "my.cnf" ]; then
    echo "❌ 错误: my.cnf 不存在"
    exit 1
fi

if [ ! -f "init.sql" ]; then
    echo "❌ 错误: init.sql 不存在"
    exit 1
fi

# 停止旧容器（如果存在）
echo "🛑 停止旧容器..."
docker compose down 2>/dev/null || true

# 启动MySQL
echo "🚀 启动MySQL容器..."
docker compose up -d

# 等待MySQL启动
echo "⏳ 等待MySQL启动..."
sleep 15

# 检查健康状态
echo "🔍 检查MySQL状态..."
for i in {1..30}; do
    if docker compose exec mysql mysqladmin ping -h localhost -uroot -pMyStrongRootPassword123 --silent 2>/dev/null; then
        echo "✅ MySQL启动成功！"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ MySQL启动超时"
        echo "查看日志:"
        docker compose logs mysql
        exit 1
    fi
    echo "等待中... ($i/30)"
    sleep 2
done

# 显示状态
echo ""
echo "=========================================="
echo "  MySQL部署完成"
echo "=========================================="
echo "容器名称: xingshuzi-mysql"
echo "端口: 3306"
echo "数据库: xingshuzi"
echo ""
echo "Root账号:"
echo "  用户名: root"
echo "  密码: MyStrongRootPassword123"
echo ""
echo "应用账号:"
echo "  用户名: xingshuzi_user"
echo "  密码: xingshuzi_pass"
echo ""
echo "连接命令:"
echo "  docker compose exec mysql mysql -uroot -pMyStrongRootPassword123"
echo ""
echo "查看日志:"
echo "  docker compose logs -f mysql"
echo ""
echo "备份数据库:"
echo "  docker compose exec mysql mysqldump -uroot -pMyStrongRootPassword123 xingshuzi > backup.sql"
echo "=========================================="

