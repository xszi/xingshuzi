#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化管理员账号到线上数据库
"""

import pymysql
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

print("=" * 60)
print("  初始化管理员账号")
print("=" * 60)

# 读取配置
MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
MYSQL_DB = os.getenv('MYSQL_DB', 'xingshuzi')

print(f"\n连接数据库: {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")

try:
    # 连接数据库
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        connect_timeout=5
    )
    
    cursor = conn.cursor()
    
    # 管理员信息
    admin_username = 'admin'
    admin_password = 'admin123'
    admin_email = 'admin@xingshuzi.com'
    admin_role = 'admin'
    
    # 生成密码哈希（使用pbkdf2兼容旧Python版本）
    password_hash = generate_password_hash(admin_password, method='pbkdf2:sha256')
    
    # 检查管理员是否已存在
    cursor.execute("SELECT id, username, role FROM users WHERE username = %s", (admin_username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        print(f"\n⚠️  管理员 '{admin_username}' 已存在")
        print(f"   ID: {existing_user[0]}")
        print(f"   角色: {existing_user[2]}")
        
        # 更新密码和角色
        cursor.execute(
            "UPDATE users SET password = %s, role = %s, email = %s WHERE username = %s",
            (password_hash, admin_role, admin_email, admin_username)
        )
        conn.commit()
        print(f"\n✅ 已更新管理员密码和角色")
    else:
        # 插入新管理员
        cursor.execute(
            "INSERT INTO users (username, password, email, role, status) VALUES (%s, %s, %s, %s, %s)",
            (admin_username, password_hash, admin_email, admin_role, 'active')
        )
        conn.commit()
        print(f"\n✅ 管理员账号创建成功！")
    
    # 显示所有用户
    print(f"\n👥 当前用户列表:")
    cursor.execute("SELECT id, username, email, role, status, created_at FROM users")
    users = cursor.fetchall()
    
    for user in users:
        print(f"  ID: {user[0]}")
        print(f"    用户名: {user[1]}")
        print(f"    邮箱: {user[2]}")
        print(f"    角色: {user[3]}")
        print(f"    状态: {user[4]}")
        print(f"    创建时间: {user[5]}")
        print()
    
    conn.close()
    
    print("=" * 60)
    print("✅ 初始化完成！")
    print("=" * 60)
    print(f"管理员账号: {admin_username}")
    print(f"管理员密码: {admin_password}")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()

