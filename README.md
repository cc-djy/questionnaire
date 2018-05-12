# questionnaire
问卷系统(2018.5.11更新)

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

6. 命令端口运行项目
    ```bash
    python manage.py runserver [port]
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

# 关于为什么这样分割模块
1. 因为这样耦合度应该会比较低。
2. 基本上只要协调好表单就可以了。

# 其他要解决的问题
1. 微信接口方面，了解一下微信接口怎么弄？ @xxx-032 
2. 讨论一下用什么数据库？
3. 关于计算分数的模块，是否可以考虑一下在前端计算？
> @worksg 之前已经考虑过在前端做分数计算，但目前还是不打算在前端做分数的计算过程，目前放在后端做分数评价主要因为分数计算模块需要从数据库中提取题目id和选项id，而后再拼接成JSON格式，此时已经完全可以在后端做计算，如果放在前端需要在前端另外设计获取此类资源的JSON请求方式，同时将数据库的有关信息嵌在网页中，只能说放在前端计算有点多此一举，另一方面前端不完全受控于服务器，前端的返回结果不受信任，有可能会随意生成用户的评价分数然后写进数据库

# 数据库设计
![untitled diagram](https://user-images.githubusercontent.com/24842631/39868835-e4a1784e-548d-11e8-978b-2e70cd8efdf9.png)

代码记录
===

## 从文字插入数据库 [仅供参考]
```python
import sqlite3
import re
import codecs

filepath = r'question.txt'
re_str_1 = r"^(\d{1,2})\s*、\s*([^\r]+?？)[\r\n]+A\s*[\.．]\s*([^\r]+)[\r\n]+B\s*[\.．]\s*([^\r]+)[\r\n]+"
re_str_2 = r"(\d{1,2})\s*、\s*A\s*[\.．]\s*([^\s]+)\s+B\s*[\.．]\s*([^\r]+)[\r\n]+"

with codecs.open(filepath, 'r', encoding='utf-8') as fr:
    raw_str = fr.read()

read_str_1_3 = raw_str.replace("\xa0", "_")
one_three = re.compile(re_str_1, re.M | re.I)
find_list_1_3 = one_three.findall(read_str_1_3)

print(len(find_list_1_3))
print(find_list_1_3)

read_str_2 = raw_str
two = re.compile(re_str_2, re.M | re.I)
find_list_2 = two.findall(read_str_2)

print(len(find_list_2))
print(find_list_2)


conn = sqlite3.connect('../db.sqlite3')
cursor = conn.cursor()

cursor.execute("INSERT INTO test_paper (paper_name) VALUES ('问卷一')")
cursor.execute("INSERT INTO question_type (description,paper_id) VALUES ('哪一答案最接近地描述了你通常的思考和行为方式。',1)")
cursor.execute("INSERT INTO question_type (description,paper_id) VALUES ('在以下各对词中，你更倾向于哪一个。考虑以下这些词的意思，而不是它们好不好听或好不好看。',1)")
cursor.execute("INSERT INTO question_type (description,paper_id) VALUES ('哪个答案最接近地描述了你通常的思考和行为方式。',1)")

i = 1

for item in find_list_1_3[:26]:
    question_description = item[1]
    option_descriptions = item[2:]
    cursor.execute("INSERT INTO question (question_description,question_type_id) VALUES ('%s',%d)" % (question_description, 1))

    for it in option_descriptions:
        cursor.execute("INSERT INTO option (option_description,question_id) VALUES ('%s',%d)" % (it, i))
    i += 1

for item in find_list_2:
    question_description = ""
    option_descriptions = item[1:]
    cursor.execute(
    "INSERT INTO question (question_description,question_type_id) VALUES ('%s',%d)" % (
    question_description, 2))

    for it in option_descriptions:
        cursor.execute("INSERT INTO option (option_description,question_id) VALUES ('%s',%d)" % (it, i))
    i += 1

for item in find_list_1_3[26:]:
    question_description = item[1]
    option_descriptions = item[2:]
    cursor.execute("INSERT INTO question (question_description,question_type_id) VALUES ('%s',%d)" % (question_description, 3))

    for it in option_descriptions:
        cursor.execute("INSERT INTO option (option_description,question_id) VALUES ('%s',%d)" % (it, i))
    i += 1

cursor.close()
conn.commit()
conn.close()

```

## 服务器返回给前端页面的json封装格式 [仅供参考]
```json
{
    "paper_name":""
    "question_types":
    [
        "question_type_id":int
        "description":"",
        "questions":
        [
            {
            "question_id":int
            "title":"",
            "options":
                [
                    {
                        'option_id': "",
                        'option_description': ""
                    },{},{},...
                ]
            },{},{},...
        ]
    ]
},{},{},...
```


# 前端循环打印的列表，附带题号索引以及选项索引

```python
    context = {}  # 页面内容上下文

    test_paper = TestPaper.objects.filter(paper_id=1)  # 读取问卷
    context['paper_name'] = test_paper[0].paper_name

    question_types = QuestionType.objects.filter(paper_id=test_paper[0].paper_id)  # 读取问题类型
    context['question_types'] = []

    question_id = 1

    # 循环读取问题类型
    for question_type in question_types:
        # 问题类型字典
        question_type_dict = {
            'description': question_type.description,
            "questions": []
        }

        questions = Question.objects.filter(question_type_id=question_type.question_type_id)  # 读取问题

        # 循环读取问题
        for question in questions:
            # 问题字典
            question_dict = {
                'question_id': question_id,
                'title': question.question_description,
                'options': []
            }

            options = Option.objects.filter(question_id=question.question_id)  # 读取选项
            option_id = 1

            # 循环读取选项
            for option in options:
                option.option_id = (chr(64 + option_id))
                question_dict['options'].append(option) # 将选项放进问题字典
                option_id += 1

            # 将问题方法进问题字典
            question_type_dict['questions'].append(question_dict)
            question_id += 1


        # 将问题类型字典放进context
        context['question_types'].append(question_type_dict)
```

## 前端提交给服务器的json封装格式 [仅供参考]
```json
[
	{
		"index":int,
		"select":int
	},{},{},..
]
```
## 插入索引 [仅供参考]
{"题目索引_1":("题目id_1",{"选项索引_1":("选项id_1",[]),"选项索引_2":("选项id_2",[]),...}),...}

```python
PaperName = TestPaper.objects.filter(PaperID=1)
Subject_TypeId = Subject_Type.objects.filter(PaperID=1)
ques_id = 1
all_ques = {}
for item in Subject_TypeId:
  Dict_1 = {}
  QuestionId = Question.objects.filter(Subject_TypeId=item.Subject_TypeId)
  for items in QuestionId:
    Dict_2 = {ques_id: (items.QuestionId, {})}
    OptionID = Option.objects.filter(QuestionId=items.QuestionId)
    option_id = 1
    for itemss in OptionID:
      Dict_2[ques_id][1].update({option_id: (itemss.OptionID,[])})
      option_id += 1
    Dict_1.update(Dict_2)
    ques_id += 1
  all_ques.update(Dict_1)
```

## 评价规则 [仅供参考]
{"题目索引_1"：{"选项id_1":[],"选项id_2":[],...},...}

```python
Extroversion = {"A": (3, 7, 10, 19, 23, 32, 62, 74, 79, 81, 83), "B": (13, 16, 26, 38, 42, 57, 68, 77, 85, 91)} # E
Introversion = {"A": (13, 16, 26, 38, 42, 57, 68, 77, 85, 91), "B": (3, 7, 10, 19, 23, 32, 62, 74, 79, 81, 83)} # I
Sensing = {"A": (2, 9, 25, 30, 34, 39, 50, 52, 54, 60, 63, 73, 92),
      "B": (5, 11, 18, 22, 27, 44, 46, 48, 65, 67, 69, 71, 82)} # S
Intuition = {"A": (5, 11, 18, 22, 27, 44, 46, 48, 65, 67, 69, 71, 82),
       "B": (2, 9, 25, 30, 34, 39, 50, 52, 54, 60, 63, 73, 92)
       } # N
Thinking = {"A": (31, 33, 35, 43, 45, 47, 49, 56, 58, 61, 66, 75, 87),
      "B": (6, 15, 21, 29, 37, 40, 51, 53, 70, 72, 89)} # T
Feeling = {
  "A": (6, 15, 21, 29, 37, 40, 51, 53, 70, 72, 89), "B": (31, 33, 35, 43, 45, 47, 49, 56, 58, 61, 66, 75, 87)} # F
Judge = {"A": (1, 4, 12, 14, 20, 28, 36, 41, 64, 76, 86),
     "B": (8, 17, 24, 55, 59, 78, 80, 84, 88, 90, 93)} # J
Perceive = {
  "A": (8, 17, 24, 55, 59, 78, 80, 84, 88, 90, 93), "B": (1, 4, 12, 14, 20, 28, 36, 41, 64, 76, 86)} # P
sum = 0
for item in [Extroversion, Introversion, Sensing, Intuition, Thinking, Feeling, Judge, Perceive][::2]: # [1::2]
  # print(item)
  sum += len(item['A']) + len(item['B'])
  print(len(item['A']) + len(item['B']))
  # print(sum)

ques_ans = {}
init_list = [0, 0, 0, 0, 0, 0, 0, 0]
position = [Extroversion, Introversion, Sensing, Intuition, Thinking, Feeling, Judge, Perceive]
for i in range(1, sum + 1):
  init_group = []
  position_num_record = []
  for x in range(len(position[0])):
    init_group.append(init_list.copy())
    position_num_record.append([])

  y = 0
  for item in position:
    t = 0
    for x in item:
      if i in item[x]:
        position_num_record[t].append(y)
      t += 1
    y += 1

  ques_ans.update({i: {}})

  y = 0
  for item in init_group:
    for x in position_num_record[y]:
      item[x] = 1
    ques_ans[i].update({y + 1: item})
    y += 1

print(ques_ans)
```

pycharm专业版与社区版的区别
https://www.jetbrains.com/pycharm/features/editions_comparison_matrix.html

pycharm社区版 django项目构建
https://my.oschina.net/hevakelcj/blog/384070

