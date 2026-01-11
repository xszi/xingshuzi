#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试本地Server项目连接线上数据库
"""

import sys
import pymysql
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

print("=" * 60)
print("  测试本地Server连接线上MySQL数据库")
print("=" * 60)

# 读取配置
MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
MYSQL_DB = os.getenv('MYSQL_DB', 'xingshuzi')

print(f"\n📋 当前配置:")
print(f"  Host: {MYSQL_HOST}")
print(f"  Port: {MYSQL_PORT}")
print(f"  User: {MYSQL_USER}")
print(f"  Database: {MYSQL_DB}")
print(f"  Password: {'*' * len(MYSQL_PASSWORD)}")

print(f"\n🔌 正在连接...")

try:
    # 尝试连接
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        connect_timeout=5
    )
    
    print("✅ 数据库连接成功！")
    
    # 获取游标
    cursor = conn.cursor()
    
    # 查询数据库信息
    print(f"\n📊 数据库信息:")
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"  MySQL版本: {version[0]}")
    
    cursor.execute("SELECT DATABASE()")
    current_db = cursor.fetchone()
    print(f"  当前数据库: {current_db[0]}")
    
    # 查询表
    print(f"\n📋 数据表列表:")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    if tables:
        print(f"  共 {len(tables)} 个表:")
        for i, table in enumerate(tables, 1):
            print(f"    {i}. {table[0]}")
            
            # 查询每个表的记录数
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()
            print(f"       └─ 记录数: {count[0]}")
    else:
        print("  ⚠️  数据库中没有表")
        print("  需要运行: python3 create_db.py")
    
    # 测试查询用户
    print(f"\n👥 用户信息:")
    try:
        cursor.execute("SELECT id, username, role, created_at FROM users LIMIT 5")
        users = cursor.fetchall()
        if users:
            print(f"  共 {len(users)} 个用户:")
            for user in users:
                print(f"    - {user[1]} ({user[2]}) - 创建时间: {user[3]}")
        else:
            print("  ⚠️  没有用户记录")
            print("  需要运行: python3 init_admin.py")
    except pymysql.err.ProgrammingError as e:
        print(f"  ⚠️  users表不存在: {e}")
    
    # 关闭连接
    conn.close()
    
    print(f"\n" + "=" * 60)
    print("✅ 测试完成！数据库连接正常")
    print("=" * 60)
    sys.exit(0)
    
except pymysql.err.OperationalError as e:
    print(f"\n❌ 连接失败: {e}")
    print(f"\n💡 可能的原因:")
    print(f"  1. MySQL服务未启动")
    print(f"  2. 主机地址或端口错误")
    print(f"  3. 防火墙阻止了连接")
    print(f"  4. .env配置不正确")
    print(f"\n🔧 解决方案:")
    print(f"  1. 检查.env文件配置")
    print(f"  2. 确保MySQL服务运行在 {MYSQL_HOST}:{MYSQL_PORT}")
    print(f"  3. 测试网络连通性: ping {MYSQL_HOST}")
    print(f"  4. 测试端口: telnet {MYSQL_HOST} {MYSQL_PORT}")
    sys.exit(1)
    
except pymysql.err.ProgrammingError as e:
    print(f"\n❌ 数据库错误: {e}")
    print(f"\n💡 可能的原因:")
    print(f"  1. 数据库 '{MYSQL_DB}' 不存在")
    print(f"  2. 用户权限不足")
    print(f"\n🔧 解决方案:")
    print(f"  1. 创建数据库: CREATE DATABASE {MYSQL_DB}")
    print(f"  2. 检查用户权限")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ 未知错误: {e}")
    sys.exit(1)

