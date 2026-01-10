import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL Database Configuration
    # 默认使用本机 MySQL，避免远程数据库不可达导致接口阻塞/超时
    # 如需连接远程服务器，请通过环境变量覆盖：MYSQL_HOST / MYSQL_USER / MYSQL_PASSWORD 等
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
    MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_DB = os.getenv('MYSQL_DB', 'xingshuzi')

    # URL encode password to handle special characters like @
    encoded_password = quote_plus(MYSQL_PASSWORD)
    # 加上连接超时参数，避免网络问题导致请求一直卡住
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        f"?charset=utf8mb4&connect_timeout=5&read_timeout=10&write_timeout=10"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = 3600 * 24  # 24 hours

