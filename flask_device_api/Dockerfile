# 使用CentOS官方镜像
FROM centos:7

RUN pip install --upgrade pip
RUN pip install flask gunicorn
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask

# 安装基础依赖
RUN yum install -y python3 python3-pip && \
    pip3 install --no-cache-dir --upgrade pip

# 设置工作目录
WORKDIR /app

# 复制文件（比COPY更详细的说明）
COPY requirements.txt .
COPY app.py .
COPY devices.py .

# 安装Python依赖
RUN pip3 install -r requirements.txt

# 创建数据目录
RUN mkdir -p /app/instance && \
    chmod 777 /app/instance

# 暴露端口
EXPOSE 5000

# 启动命令（直接运行Flask开发服务器）
CMD ["python3", "app.py"]
