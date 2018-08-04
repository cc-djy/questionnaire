'''
这里是将题目读到数据库的模块
步骤：
1.将题目从文件读到字符串对象中
2.将题目从字符串对象读到数据库中

'''

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