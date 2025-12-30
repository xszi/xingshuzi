# 阿里云 ECS Ubuntu 部署文档

本文档介绍如何在阿里云 ECS Ubuntu 服务器上部署 xingshuzi-back Flask 项目。

## 一、服务器环境准备

### 1.1 更新系统

```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 安装 Python 3.9+

```bash
# 安装 Python 3.9 和 pip
sudo apt install python3 python3-pip python3-venv -y

# 验证安装
python3 --version
pip3 --version
```

### 1.3 安装 MySQL 客户端（如果需要本地测试）

```bash
sudo apt install mysql-client -y
```

### 1.4 安装 Git（用于拉取代码）

```bash
sudo apt install git -y
```

## 二、项目部署

### 2.1 创建项目目录

```bash
# 创建项目目录
sudo mkdir -p /opt/xingshuzi-back
sudo chown $USER:$USER /opt/xingshuzi-back
cd /opt/xingshuzi-back
```

### 2.2 上传项目文件

**方式一：使用 Git（推荐）**

```bash
# 如果项目在 Git 仓库中
git clone <your-repo-url> .
```

**方式二：使用 SCP 上传**

在本地机器执行：

```bash
scp -r /path/to/xingshuzi-back root@your-server-ip:/opt/
```

**方式三：使用 SFTP 工具**

使用 FileZilla、WinSCP 等工具上传项目文件到 `/opt/xingshuzi-back`

### 2.3 创建虚拟环境

```bash
cd /opt/xingshuzi-back
python3 -m venv venv
source venv/bin/activate
```

### 2.4 安装项目依赖

```bash
# 激活虚拟环境后
pip install --upgrade pip
pip install -r requirements.txt

# 如果网络较慢，可以使用国内镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 2.5 配置环境变量

创建 `.env` 文件：

```bash
cd /opt/xingshuzi-back
nano .env
```

在 `.env` 文件中配置：

```ini
# MySQL 数据库配置
MYSQL_USER=jhadmin
MYSQL_PASSWORD=Ww@204417
MYSQL_HOST=120.76.247.123
MYSQL_PORT=3306
MYSQL_DB=xingshuzi

# Flask 密钥（请修改为随机字符串）
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
```

**重要：生产环境请务必修改 SECRET_KEY 和 JWT_SECRET_KEY 为随机字符串！**

生成随机密钥：

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 2.6 初始化数据库

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 创建数据库（如果需要）
python3 create_db.py

# 创建数据库表
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('数据库表创建成功！')"

# 创建管理员账号（可选）
python3 init_admin.py
```

## 三、使用 Systemd 管理服务

### 3.1 创建 Systemd 服务文件

```bash
sudo nano /etc/systemd/system/xingshuzi-back.service
```

添加以下内容：

```ini
[Unit]
Description=xingshuzi-back Flask Application
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/xingshuzi-back
Environment="PATH=/opt/xingshuzi-back/venv/bin"
ExecStart=/opt/xingshuzi-back/venv/bin/python3 /opt/xingshuzi-back/run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**注意：**
- 将 `User=root` 改为你的实际用户名（建议创建专用用户）
- 确保路径正确

### 3.2 创建生产环境启动脚本（推荐）

由于 `run.py` 中使用了 `debug=True`，生产环境需要修改。创建生产环境启动脚本：

```bash
nano /opt/xingshuzi-back/run_prod.py
```

内容：

```python
from app import create_app, db
import os

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized.")

if __name__ == '__main__':
    # Ensure tables are created
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")
            print("Make sure your MySQL server is running and the database exists.")
    
    # 生产环境配置
    app.run(host='0.0.0.0', port=5001, debug=False)
```

然后修改 systemd 服务文件中的 `ExecStart`：

```ini
ExecStart=/opt/xingshuzi-back/venv/bin/python3 /opt/xingshuzi-back/run_prod.py
```

### 3.3 启动和管理服务

```bash
# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start xingshuzi-back

# 设置开机自启
sudo systemctl enable xingshuzi-back

# 查看服务状态
sudo systemctl status xingshuzi-back

# 查看日志
sudo journalctl -u xingshuzi-back -f

# 停止服务
sudo systemctl stop xingshuzi-back

# 重启服务
sudo systemctl restart xingshuzi-back
```

## 四、配置 Nginx 反向代理（推荐）

### 4.1 安装 Nginx

```bash
sudo apt install nginx -y
```

### 4.2 配置 Nginx

```bash
sudo nano /etc/nginx/sites-available/xingshuzi-back
```

添加以下配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或服务器IP

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 4.3 启用配置

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/xingshuzi-back /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx

# 设置开机自启
sudo systemctl enable nginx
```

### 4.4 配置 HTTPS（可选，推荐）

使用 Let's Encrypt 免费 SSL 证书：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书（需要域名已解析到服务器）
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

## 五、防火墙配置

### 5.1 阿里云安全组配置

在阿里云控制台配置安全组规则：

- **入方向规则**：
  - HTTP (80) - 允许
  - HTTPS (443) - 允许
  - SSH (22) - 允许（仅限你的IP）

### 5.2 Ubuntu 防火墙配置（如果启用了 UFW）

```bash
# 允许 HTTP 和 HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp

# 如果直接访问 5001 端口（不推荐）
sudo ufw allow 5001/tcp

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status
```

## 六、安全建议

### 6.1 创建专用用户（推荐）

```bash
# 创建专用用户
sudo useradd -m -s /bin/bash xingshuzi
sudo chown -R xingshuzi:xingshuzi /opt/xingshuzi-back

# 修改 systemd 服务文件中的 User
sudo nano /etc/systemd/system/xingshuzi-back.service
# 将 User=root 改为 User=xingshuzi
```

### 6.2 修改生产环境配置

确保 `run_prod.py` 中 `debug=False`

### 6.3 保护敏感信息

- `.env` 文件权限设置为 600
```bash
chmod 600 /opt/xingshuzi-back/.env
```

- 不要将 `.env` 文件提交到 Git

### 6.4 定期备份

```bash
# 创建备份脚本
nano /opt/backup_xingshuzi.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份数据库（需要 mysqldump）
mysqldump -h 120.76.247.123 -u jhadmin -p'Ww@204417' xingshuzi > $BACKUP_DIR/db_$DATE.sql

# 备份项目文件
tar -czf $BACKUP_DIR/xingshuzi-back_$DATE.tar.gz /opt/xingshuzi-back

# 删除 7 天前的备份
find $BACKUP_DIR -type f -mtime +7 -delete
```

```bash
chmod +x /opt/backup_xingshuzi.sh

# 添加到 crontab（每天凌晨 2 点备份）
crontab -e
# 添加：0 2 * * * /opt/backup_xingshuzi.sh
```

## 七、验证部署

### 7.1 检查服务状态

```bash
# 检查 Flask 服务
sudo systemctl status xingshuzi-back

# 检查 Nginx 服务
sudo systemctl status nginx

# 检查端口监听
sudo netstat -tlnp | grep 5001
```

### 7.2 测试 API

```bash
# 测试首页接口
curl http://localhost:5001/api/home/banners

# 测试登录接口
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 7.3 查看日志

```bash
# Flask 应用日志
sudo journalctl -u xingshuzi-back -f

# Nginx 访问日志
sudo tail -f /var/log/nginx/access.log

# Nginx 错误日志
sudo tail -f /var/log/nginx/error.log
```

## 八、常见问题

### 8.1 服务启动失败

```bash
# 查看详细错误
sudo journalctl -u xingshuzi-back -n 50

# 检查虚拟环境
source /opt/xingshuzi-back/venv/bin/activate
python3 -c "import flask; print(flask.__version__)"

# 检查数据库连接
python3 -c "from app import create_app; app = create_app(); print('OK')"
```

### 8.2 数据库连接失败

- 检查 `.env` 文件配置是否正确
- 检查数据库服务器是否允许远程连接
- 检查安全组是否开放 3306 端口（如果数据库在 ECS 上）

### 8.3 端口被占用

```bash
# 查找占用端口的进程
sudo lsof -i :5001

# 杀死进程
sudo kill -9 <PID>
```

### 8.4 权限问题

```bash
# 确保项目目录权限正确
sudo chown -R xingshuzi:xingshuzi /opt/xingshuzi-back
chmod 600 /opt/xingshuzi-back/.env
```

## 九、快速部署脚本

创建一键部署脚本 `deploy.sh`：

```bash
#!/bin/bash
set -e

echo "开始部署 xingshuzi-back..."

# 1. 更新系统
echo "更新系统..."
sudo apt update

# 2. 安装依赖
echo "安装 Python 和依赖..."
sudo apt install -y python3 python3-pip python3-venv git

# 3. 创建项目目录
echo "创建项目目录..."
sudo mkdir -p /opt/xingshuzi-back
sudo chown $USER:$USER /opt/xingshuzi-back

# 4. 创建虚拟环境
echo "创建虚拟环境..."
cd /opt/xingshuzi-back
python3 -m venv venv
source venv/bin/activate

# 5. 安装 Python 依赖
echo "安装 Python 依赖..."
pip install --upgrade pip
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 6. 初始化数据库
echo "初始化数据库..."
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('数据库表创建成功！')"

# 7. 创建 systemd 服务
echo "配置 systemd 服务..."
sudo tee /etc/systemd/system/xingshuzi-back.service > /dev/null <<EOF
[Unit]
Description=xingshuzi-back Flask Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/xingshuzi-back
Environment="PATH=/opt/xingshuzi-back/venv/bin"
ExecStart=/opt/xingshuzi-back/venv/bin/python3 /opt/xingshuzi-back/run_prod.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 8. 启动服务
echo "启动服务..."
sudo systemctl daemon-reload
sudo systemctl enable xingshuzi-back
sudo systemctl start xingshuzi-back

echo "部署完成！"
echo "查看服务状态: sudo systemctl status xingshuzi-back"
echo "查看日志: sudo journalctl -u xingshuzi-back -f"
```

使用：

```bash
chmod +x deploy.sh
./deploy.sh
```

## 十、更新部署

当代码更新后：

```bash
cd /opt/xingshuzi-back

# 如果使用 Git
git pull

# 激活虚拟环境
source venv/bin/activate

# 更新依赖（如果有）
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 重启服务
sudo systemctl restart xingshuzi-back

# 查看日志确认
sudo journalctl -u xingshuzi-back -f
```

---

## 总结

部署完成后，你的服务将：

- ✅ 运行在 `http://your-server-ip:5001` 或通过 Nginx 在 `http://your-domain.com`
- ✅ 自动启动和重启（systemd 管理）
- ✅ 连接到线上 MySQL 数据库
- ✅ 支持 HTTPS（如果配置了 SSL）

如有问题，请查看日志文件排查。


