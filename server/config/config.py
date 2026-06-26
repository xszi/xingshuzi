import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL Database Configuration
    MYSQL_USER = os.getenv('MYSQL_USER', 'jhadmin')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Ww@204417')
    MYSQL_HOST = os.getenv('MYSQL_HOST', '120.76.247.123')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_DB = os.getenv('MYSQL_DB', 'xingshuzi')

    # URL encode password to handle special characters like @
    encoded_password = quote_plus(MYSQL_PASSWORD)
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = 3600 * 24  # 24 hours

    # 对外可访问的后端根地址（用于生成 /uploads 图片 URL，避免存成 127.0.0.1）
    PUBLIC_BASE_URL = os.getenv('PUBLIC_BASE_URL', 'http://120.76.247.123:5001').rstrip('/')

    # 文件上传配置
    # 上传根目录（绝对路径），默认为项目内 server/uploads
    UPLOAD_FOLDER = os.getenv(
        'UPLOAD_FOLDER',
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
    )
    # 单文件最大 10MB
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    # 允许的图片扩展名
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

