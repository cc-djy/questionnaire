# questionnaire
问卷系统
#2018.5.5 6:49更新

关于:如何运行从git下载来的项目

1..pycharm直接打开下载来的项目,如果重新自己创建一个的话,运行的时候可能会出现路径问题

2.Ctrl+Tab 选择 Terminal,进入python命令行端口

3.pip install -r requirements.txt 下载文件里面的配置

4.python manage.py makemigrations  同步数据库

  python manage.py migrate
  
5.命令端口运行项目
  python manage.py runserver
