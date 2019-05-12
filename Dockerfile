FROM python:3.7

#设置时区
ENV TZ "Asia/Shanghai"

#声明镜像制作者
MAINTAINER niracler niracler@gmail.com

# 设置系统环境变量DOCKER_SRC
ENV DOCKER_SRC=/usr/src/app

#MySQL-Python必须得先安装这个库
RUN mkdir /usr/src/app

#设置工作目录
WORKDIR $DOCKER_SRC

#暴露端口8001，到时候执行docker run 的时候才好把宿主机端口映射到8000
EXPOSE 8000

RUN  pip3 install gunicorn
RUN  pip3 install django==2.0.5  -i https://pypi.tuna.tsinghua.edu.cn/simple


#install any needed pacakges in requirements.txt，你要把所有需要安装的Python模块加到这文件中。
COPY requirements.txt ./
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


