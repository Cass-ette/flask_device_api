# 使用CentOS 7作为基础镜像
FROM centos:7

# 安装Python和pip
RUN yum install -y python3 python3-pip

# 设置容器内的工作目录为/app
WORKDIR /app

# 把本地文件复制到镜像里
COPY requirements.txt.
COPY app.py.
COPY devices.py.

# 安装Python依赖，使用清华大学PyPI镜像源
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 创建存放数据库的目录并设置权限
RUN mkdir -p /app/instance && chmod 777 /app/instance

# 声明容器运行时暴露5000端口（Flask默认端口）
EXPOSE 5000

# 使用Gunicorn启动Flask应用，开启4个工作进程，绑定到0.0.0.0:5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
