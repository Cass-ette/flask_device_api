# 使用官方Python镜像（国内用户可替换为阿里云源）
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 配置清华pip源加速
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

# 复制必要文件
COPY requirements.txt .
COPY app.py .
COPY devices.py .

# 安装依赖（SQLite3已内置在Python中，无需单独安装）
RUN pip install --no-cache-dir -r requirements.txt gunicorn==20.1.0

# 创建数据目录（SQLite数据库存放位置）
RUN mkdir -p /app/instance && chmod 777 /app/instance

# 设置上海时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 生产环境配置
ENV FLASK_APP=app.py FLASK_ENV=production

# 暴露端口
EXPOSE 5000

# 启动命令（Gunicorn生产服务器）
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
