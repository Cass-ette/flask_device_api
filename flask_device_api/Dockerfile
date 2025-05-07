# 使用CentOS 7官方镜像（建议指定具体版本号避免兼容性问题）
FROM centos:7

# 配置阿里云yum源（解决yum安装慢的问题）
RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup && \
    curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && \
    yum makecache

# 安装基础工具（添加-epel源）
RUN yum install -y epel-release && \
    yum install -y python3 python3-pip && \
    # 配置pip清华源（解决pip安装慢的问题）
    mkdir -p /root/.pip && \
    echo '[global]' > /root/.pip/pip.conf && \
    echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >> /root/.pip/pip.conf && \
    echo 'trusted-host = pypi.tuna.tsinghua.edu.cn' >> /root/.pip/pip.conf && \
    pip3 install --no-cache-dir --upgrade pip

# 设置工作目录（后续操作都在此目录执行）
WORKDIR /app

# 复制文件（使用分层复制优化构建缓存）
COPY requirements.txt .
COPY *.py .

# 安装依赖（利用缓存层加速重建）
RUN pip3 install --no-cache-dir -r requirements.txt && \
    # 安装gunicorn作为生产服务器
    pip3 install gunicorn==20.1.0

# 创建数据目录（设置权限允许写入）
RUN mkdir -p /app/instance && \
    chmod 777 /app/instance && \
    # 解决CentOS时区问题
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 声明环境变量（可被docker run覆盖）
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 暴露端口（仅起说明作用，实际映射需要在run时指定）
EXPOSE 5000

# 启动命令（使用gunicorn生产服务器）
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
