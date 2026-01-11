FROM python:3.11-slim

WORKDIR /app

# 使用阿里云镜像源加速（国内部署）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 使用阿里云pypi镜像加速
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5001

# 设置环境变量
ENV FLASK_PORT=5001

# 启动命令
CMD ["python3", "run.py"]

