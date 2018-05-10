# questionnaire
问卷系统(2018.5.5 6:49更新)

### 关于:如何运行从git下载来的项目

1. pycharm直接打开下载来的项目,如果重新自己创建一个的话,运行的时候可能会出现路径问题

2. Ctrl+Tab 选择 Terminal,进入python命令行端口

3. 下载文件里面的配置
    ```bash
    pip install -r requirements.txt
    ```

4. 同步数据库
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. 读题目,运行 test_paper 文件夹中的 test.py 文件(注意linux与win的换行区别,此处的正则式要用win的换行)

6. 命令端口运行项目
    ```bash
    python manage.py runserver
    ```