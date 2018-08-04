# questionnaire

性格测试系统(2018.5.15更新)

# 关于:如何运行从git下载来的项目


1. pycharm直接打开下载来的项目,如果重新自己创建一个的话,运行的时候可能会出现路径问题

2. Ctrl+Tab 选择 Terminal,进入python命令行端口

3. 下载文件里面的配置
    ```bash
    pip install -r requirements.txt
    ```

4. 同步数据库
    ```bash
    python manage.py makemigrations <app_name>
    python manage.py migrate
    ```

5. 读题目,运行 test_paper 文件夹中的 test.py 文件(注意linux与win的换行区别,此处的正则式要用win的换行)

6. 命令端口运行项目 [Why does DEBUG=False setting make my django Static Files Access fail?
](https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail)
    ```bash
    python manage.py   runserver --insecure [port]
    ```
    
# 关于:如何在命令行模式下，使用git命令clone和push项目到dev分支
> @worksg 一下命令需要更改使用人名称和邮箱以及git项目的路径，切勿直接复制粘贴

	
	git config --global user.email "571940753@qq.com" #配置git邮箱信息
	git config --global user.name "worksg" #配置git维护者信息

	git clone https://github.com/worksg/questionnaire.git	#克隆仓库到本地

	git remote -v #命令列出所有远程主机及其网址
	git branch #查看当前HEAD所处分支
	git checkout -b dev origin/dev #在origin/dev的基础上，创建一个本地新分支[dev]并切换进去

	git add <file_or_filepath>	# add
	git commit -m "<your_comment>"	# commit
	git push -u origin dev	# push

# 项目结构

![untitled diagram](https://user-images.githubusercontent.com/24842631/39669156-92a82184-5116-11e8-9e02-4b176dd249a5.png)


1. **前端展示模块** @AntonioShi ，优化样式，主要是base.html 与 index.html

2. **django模块** @worksg ，写好响应用户的逻辑，接收用户的表单，并将用户信息存到数据库

3. **数据库模块** @worksg ，设计好数据库的结构，在学校服务器试着部署一下数据库，然后远程连接调试

4. **读题目模块** @uouobba , 将问卷的那个文档读到数据库

> @worksg 之前已经考虑过在前端做分数计算，但目前还是不打算在前端做分数的计算过程，目前放在后端做分数评价主要因为分数计算模块需要从数据库中提取题目id和选项id，而后再拼接成JSON格式，此时已经完全可以在后端做计算，如果放在前端需要在前端另外设计获取此类资源的JSON请求方式，同时将数据库的有关信息嵌在网页中，只能说放在前端计算有点多此一举，另一方面前端不完全受控于服务器，前端的返回结果不受信任，有可能会随意生成用户的评价分数然后写进数据库

# 数据库设计(略)


