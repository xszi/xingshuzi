#!/usr/bin/env python3
"""
数据库连接测试脚本
用于诊断数据库连接问题
"""
import pymysql
import os
import sys
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('MYSQL_USER', 'jhadmin')
password = os.getenv('MYSQL_PASSWORD', 'Ww@204417')
host = os.getenv('MYSQL_HOST', '120.76.247.123')
port = int(os.getenv('MYSQL_PORT', 3306))
db_name = os.getenv('MYSQL_DB', 'xingshuzi')

print("=" * 60)
print("数据库连接诊断工具")
print("=" * 60)
print(f"主机: {host}")
print(f"端口: {port}")
print(f"用户: {user}")
print(f"数据库: {db_name}")
print(f"密码: {'*' * len(password) if password else '(未设置)'}")
print("=" * 60)
print()

# 获取当前服务器 IP
try:
    import socket
    current_ip = socket.gethostbyname(socket.gethostname())
    print(f"当前服务器 IP: {current_ip}")
except:
    print("无法获取当前服务器 IP")
print()

# 测试连接
print("正在测试连接...")
try:
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        connect_timeout=10
    )
    print("✅ 连接成功！")
    
    cursor = conn.cursor()
    
    # 显示当前用户权限
    print("\n当前用户权限信息:")
    cursor.execute("SELECT user, host FROM mysql.user WHERE user = %s", (user,))
    users = cursor.fetchall()
    if users:
        print("找到以下用户:")
        for u, h in users:
            print(f"  - {u}@{h}")
    else:
        print(f"⚠️  未找到用户: {user}")
    
    # 显示数据库
    print(f"\n检查数据库 '{db_name}' 是否存在...")
    cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
    if cursor.fetchone():
        print(f"✅ 数据库 '{db_name}' 已存在")
    else:
        print(f"⚠️  数据库 '{db_name}' 不存在")
        print("尝试创建数据库...")
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.commit()
            print(f"✅ 数据库 '{db_name}' 创建成功")
        except Exception as e:
            print(f"❌ 创建数据库失败: {e}")
    
    conn.close()
    print("\n✅ 所有测试通过！")
    sys.exit(0)
    
except pymysql.err.OperationalError as e:
    error_code, error_msg = e.args
    print(f"\n❌ 连接失败: ({error_code}) {error_msg}")
    
    if error_code == 1045:
        print("\n可能的原因:")
        print("1. 用户名或密码错误")
        print("2. 用户没有从当前 IP 地址访问的权限")
        print("3. MySQL 服务器配置了 IP 白名单")
        print("\n解决方案:")
        print("1. 检查 .env 文件中的 MYSQL_USER 和 MYSQL_PASSWORD 是否正确")
        print("2. 在 MySQL 服务器上执行以下命令授予权限:")
        print(f"   GRANT ALL PRIVILEGES ON {db_name}.* TO '{user}'@'%' IDENTIFIED BY 'your_password';")
        print("   FLUSH PRIVILEGES;")
        print("3. 或者使用允许所有 IP 的用户:")
        print(f"   GRANT ALL PRIVILEGES ON {db_name}.* TO '{user}'@'%' IDENTIFIED BY 'your_password';")
        print("   FLUSH PRIVILEGES;")
    elif error_code == 2003:
        print("\n可能的原因:")
        print("1. MySQL 服务器未启动")
        print("2. 防火墙阻止了连接")
        print("3. 安全组未开放 3306 端口")
        print("\n解决方案:")
        print("1. 检查 MySQL 服务是否运行")
        print("2. 检查阿里云安全组是否开放 3306 端口")
        print("3. 检查服务器防火墙设置")
    elif error_code == 1049:
        print(f"\n数据库 '{db_name}' 不存在，但连接正常")
        print("可以运行 create_db.py 创建数据库")
    
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ 发生未知错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


