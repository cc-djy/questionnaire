def get_remark_rule():
    '''生成题目选项所对应的分数的索引'''
    Extroversion = {
        "A": (3, 7, 10, 19, 23, 32, 62, 74, 79, 81, 83),
        "B": (13, 16, 26, 38, 42, 57, 68, 77, 85, 91),
    }  # E
    Introversion = {
        "A": (13, 16, 26, 38, 42, 57, 68, 77, 85, 91),
        "B": (3, 7, 10, 19, 23, 32, 62, 74, 79, 81, 83),
    }  # I
    Sensing = {
        "A": (2, 9, 25, 30, 34, 39, 50, 52, 54, 60, 63, 73, 92),
        "B": (5, 11, 18, 22, 27, 44, 46, 48, 65, 67, 69, 71, 82),
    }  # S
    Intuition = {
        "A": (5, 11, 18, 22, 27, 44, 46, 48, 65, 67, 69, 71, 82),
        "B": (2, 9, 25, 30, 34, 39, 50, 52, 54, 60, 63, 73, 92),
    }  # N
    Thinking = {
        "A": (31, 33, 35, 43, 45, 47, 49, 56, 58, 61, 66, 75, 87),
        "B": (6, 15, 21, 29, 37, 40, 51, 53, 70, 72, 89),
    }  # T
    Feeling = {
        "A": (6, 15, 21, 29, 37, 40, 51, 53, 70, 72, 89),
        "B": (31, 33, 35, 43, 45, 47, 49, 56, 58, 61, 66, 75, 87),
    }  # F
    Judge = {
        "A": (1, 4, 12, 14, 20, 28, 36, 41, 64, 76, 86),
        "B": (8, 17, 24, 55, 59, 78, 80, 84, 88, 90, 93),
    }  # J
    Perceive = {
        "A": (8, 17, 24, 55, 59, 78, 80, 84, 88, 90, 93),
        "B": (1, 4, 12, 14, 20, 28, 36, 41, 64, 76, 86),
    }  # P

    position = [Extroversion, Introversion, Sensing, Intuition, Thinking, Feeling, Judge, Perceive]

    # 计算题目数量
    sum = 0
    for item in position[::2]:  # [1::2]
        sum += len(item['A']) + len(item['B'])

    ques_ans = {}
    init_list = [0, 0, 0, 0, 0, 0, 0, 0]

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

    return ques_ans


def get_json():
    """
        {"题目索引_1":
            (
                "题目id_1",{
                "选项索引_1":("选项id_1",[]),
                "选项索引_2":("选项id_2",[]),
                ...
                }
            ),"":(),"":(),...
        }
        :return: dict
    """
    from .models import TestPaper, QuestionType, Question, Option
    # PaperName = TestPaper.objects.filter(paper_id=1)
    Subjects = QuestionType.objects.filter(paper_id=1)
    ques_id = 1
    all_ques = {}
    remark_dict = get_remark_rule()
    for item in Subjects:
        Dict_1 = {}
        QuestionId = Question.objects.filter(question_type_id=item.question_type_id)
        for items in QuestionId:
            Dict_2 = {ques_id: (items.question_id, {})}
            OptionID = Option.objects.filter(question_id=items.question_id)
            option_id = 1
            for itemss in OptionID:
                Dict_2[ques_id][1].update({option_id: (itemss.option_id, remark_dict[ques_id][option_id])})
                option_id += 1
            Dict_1.update(Dict_2)
            ques_id += 1
        all_ques.update(Dict_1)
    return all_ques

def clac_score(arg_list):
    """
    Extroversion, Introversion, Sensing, Intuition, Thinking, Feeling, Judge, Perceive = 0,0,0,0,0,0,0,0
    :param arg_list:
    :return:
    """

    all_score = {
        "Extroversion": [0, 'E'],
        "Introversion": [0, 'I'],
        "Sensing": [0, 'S'],
        "Intuition": [0, 'N'],
        "Thinking": [0, 'T'],
        "Feeling": [0, 'F'],
        "Judge": [0, 'J'],
        "Perceive": [0, 'P']
    }

    for item in arg_list:
        all_score["Extroversion"][0] += item[0]
        all_score["Introversion"][0] += item[1]
        all_score["Sensing"][0] += item[2]
        all_score["Intuition"][0] += item[3]
        all_score["Thinking"][0] += item[4]
        all_score["Feeling"][0] += item[5]
        all_score["Judge"][0] += item[6]
        all_score["Perceive"][0] += item[7]

    return all_score


def get_result(all_score):
    '''
    得出最后性格的函数
    :param all_score:
    :return:
    '''

    character = []

    if all_score['Extroversion'][0] > all_score['Introversion'][0]:
        character .append(all_score['Extroversion'][1])
    else:
        character.append(all_score['Introversion'][1])

    if all_score['Sensing'][0] > all_score['Intuition'][0]:
        character .append(all_score['Sensing'][1])
    else:
        character.append(all_score['Intuition'][1])

    if all_score['Thinking'][0] > all_score['Feeling'][0]:
        character.append(all_score['Thinking'][1])
    else:
        character.append(all_score['Feeling'][1])

    if all_score['Judge'][0] > all_score['Perceive'][0]:
        character.append(all_score['Judge'][1])
    else:
        character.append(all_score['Perceive'][1])

    return "".join(character)
