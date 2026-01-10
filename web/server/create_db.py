import pymysql
import os
import sys
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('MYSQL_USER', 'root')
password = os.getenv('MYSQL_PASSWORD', '123456')
host = os.getenv('MYSQL_HOST', '127.0.0.1')
port = int(os.getenv('MYSQL_PORT', 3306))
db_name = os.getenv('MYSQL_DB', 'xingshuzi')

print(f"Connecting to MySQL at {host}:{port} as {user}...")

try:
    conn = pymysql.connect(
        host=host, 
        user=user, 
        password=password, 
        port=port,
        connect_timeout=10
    )
    cursor = conn.cursor()
    print(f"Creating database {db_name} if not exists...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    print("Database created successfully.")
    conn.close()
except pymysql.err.OperationalError as e:
    error_code, error_msg = e.args
    print(f"Error ({error_code}): {error_msg}")
    
    if error_code == 1045:
        print("\n访问被拒绝！可能的原因：")
        print("1. 用户名或密码错误")
        print("2. 用户没有从当前服务器 IP 访问的权限")
        print("\n解决方案：")
        print("1. 检查 .env 文件中的用户名和密码是否正确")
        print("2. 在 MySQL 服务器上执行以下 SQL 命令：")
        print(f"   GRANT ALL PRIVILEGES ON *.* TO '{user}'@'%' IDENTIFIED BY 'your_password';")
        print("   FLUSH PRIVILEGES;")
        print("\n或者运行测试脚本获取更多信息：")
        print("   python3 test_db_connection.py")
    elif error_code == 2003:
        print("\n无法连接到 MySQL 服务器！")
        print("请检查：")
        print("1. MySQL 服务是否运行")
        print("2. 阿里云安全组是否开放 3306 端口")
        print("3. 服务器防火墙设置")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
