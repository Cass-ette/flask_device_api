# 使用官方Python镜像（阿里云国内源加速下载）
FROM registry.cn-hangzhou.aliyuncs.com/library/python:3.9-slim

# 设置工作目录
WORKDIR /app

# 配置清华pip源（解决国内安装慢的问题）
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

# 复制文件（利用Docker缓存层优化）
COPY requirements.txt .
COPY *.py .

# 安装依赖（使用--no-cache-dir减小镜像体积）
RUN pip install --no-cache-dir -r requirements.txt gunicorn==20.1.0

# 创建数据目录（设置可写权限）
RUN mkdir -p /app/instance && chmod 777 /app/instance

# 设置时区（解决日志时间问题）
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 生产环境配置
ENV FLASK_APP=app.py FLASK_ENV=production

# 暴露端口
EXPOSE 5000

# 使用gunicorn启动（生产级服务器）
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
