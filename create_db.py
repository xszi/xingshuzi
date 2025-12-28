import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('MYSQL_USER', 'jhadmin')
password = os.getenv('MYSQL_PASSWORD', 'Ww@204417')
host = os.getenv('MYSQL_HOST', '120.76.247.123')
port = int(os.getenv('MYSQL_PORT', 3306))
db_name = os.getenv('MYSQL_DB', 'xingshuzi')

print(f"Connecting to MySQL at {host}:{port} as {user}...")

try:
    conn = pymysql.connect(host=host, user=user, password=password, port=port)
    cursor = conn.cursor()
    print(f"Creating database {db_name} if not exists...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("Database created successfully.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
