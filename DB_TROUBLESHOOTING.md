# 数据库连接问题排查指南

## 错误：Access denied for user 'jhadmin'@'xxx.xxx.xxx.xxx'

这个错误表示 MySQL 用户没有从当前服务器 IP 地址访问的权限。

## 解决方案

### 方案一：在 MySQL 服务器上授予远程访问权限（推荐）

1. **登录到 MySQL 服务器**（120.76.247.123）

```bash
mysql -u root -p
```

2. **检查当前用户权限**

```sql
SELECT user, host FROM mysql.user WHERE user = 'jhadmin';
```

3. **授予远程访问权限**

如果用户已存在，更新权限：

```sql
-- 允许从任何 IP 访问（生产环境建议限制 IP）
GRANT ALL PRIVILEGES ON xingshuzi.* TO 'jhadmin'@'%' IDENTIFIED BY 'Ww@204417';
FLUSH PRIVILEGES;
```

或者只允许从特定 IP 访问（更安全）：

```sql
-- 替换 YOUR_ECS_IP 为你的 ECS 服务器 IP
GRANT ALL PRIVILEGES ON xingshuzi.* TO 'jhadmin'@'YOUR_ECS_IP' IDENTIFIED BY 'Ww@204417';
FLUSH PRIVILEGES;
```

如果用户不存在，创建新用户：

```sql
-- 创建用户并授予权限
CREATE USER 'jhadmin'@'%' IDENTIFIED BY 'Ww@204417';
GRANT ALL PRIVILEGES ON xingshuzi.* TO 'jhadmin'@'%';
FLUSH PRIVILEGES;
```

4. **验证权限**

```sql
SHOW GRANTS FOR 'jhadmin'@'%';
```

### 方案二：检查 MySQL 配置文件

确保 MySQL 允许远程连接：

1. **检查 MySQL 配置文件** (`/etc/mysql/mysql.conf.d/mysqld.cnf` 或 `/etc/my.cnf`)

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

确保有以下配置：

```ini
bind-address = 0.0.0.0  # 允许所有 IP 连接，或指定具体 IP
```

2. **重启 MySQL 服务**

```bash
sudo systemctl restart mysql
```

### 方案三：检查防火墙和安全组

1. **阿里云安全组配置**

在阿里云控制台：
- 进入 ECS 实例 → 安全组
- 添加规则：允许 TCP 3306 端口（入方向）
- 源地址：你的 ECS 服务器 IP 或 0.0.0.0/0（不推荐，仅测试用）

2. **服务器防火墙**

如果服务器启用了防火墙：

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 3306/tcp

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --reload
```

## 诊断步骤

### 1. 运行诊断脚本

在 ECS 服务器上运行：

```bash
python3 test_db_connection.py
```

这个脚本会：
- 显示连接配置信息
- 测试数据库连接
- 显示详细的错误信息和解决方案

### 2. 手动测试连接

```bash
# 使用 MySQL 客户端测试（如果已安装）
mysql -h 120.76.247.123 -u jhadmin -p
# 输入密码: Ww@204417
```

### 3. 检查网络连通性

```bash
# 测试端口是否开放
telnet 120.76.247.123 3306

# 或使用 nc
nc -zv 120.76.247.123 3306
```

## 常见问题

### Q1: 密码包含特殊字符（如 @）怎么办？

密码中的特殊字符在连接字符串中需要 URL 编码。项目已经自动处理了这个问题（在 `config.py` 中使用 `quote_plus`）。

如果手动连接，确保密码正确：
- 密码：`Ww@204417`
- 在命令行中使用引号：`mysql -u jhadmin -p'Ww@204417'`

### Q2: 如何查看当前连接的用户和 IP？

在 MySQL 服务器上执行：

```sql
SELECT user, host, db FROM information_schema.processlist;
```

### Q3: 如何撤销远程访问权限？

```sql
-- 删除用户
DROP USER 'jhadmin'@'%';

-- 或只撤销权限
REVOKE ALL PRIVILEGES ON xingshuzi.* FROM 'jhadmin'@'%';
FLUSH PRIVILEGES;
```

### Q4: 如何创建数据库？

如果数据库不存在，在 MySQL 服务器上执行：

```sql
CREATE DATABASE IF NOT EXISTS xingshuzi 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

或者在 ECS 服务器上运行（如果连接成功）：

```bash
python3 create_db.py
```

## 安全建议

1. **限制 IP 访问**：不要使用 `'%'`，而是指定具体的 ECS 服务器 IP
2. **使用强密码**：确保数据库密码足够复杂
3. **最小权限原则**：只授予必要的权限
4. **定期检查**：定期检查用户权限和访问日志

## 快速修复命令

如果 MySQL 服务器在本地或可以 SSH 访问，执行以下命令：

```bash
mysql -u root -p <<EOF
CREATE DATABASE IF NOT EXISTS xingshuzi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'jhadmin'@'%' IDENTIFIED BY 'Ww@204417';
GRANT ALL PRIVILEGES ON xingshuzi.* TO 'jhadmin'@'%';
FLUSH PRIVILEGES;
SELECT user, host FROM mysql.user WHERE user = 'jhadmin';
EOF
```

然后在 ECS 服务器上测试：

```bash
python3 test_db_connection.py
```


