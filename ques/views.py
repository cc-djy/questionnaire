from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import TestPaper, QuestionType, Question, Option


# @cache_page(60 * 15)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def index(request):
    '''
        关于index页面的视图,以及交给模板的字典格式如下:
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
    '''
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
            'question_type_id': question_type.question_type_id,
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
                question_dict['options'].append({
                    'option_id': chr(64 + option_id),
                    'option_num_id': option_id,
                    'option_description': option.option_description
                })  # 将选项放进问题字典
                option_id += 1

            # 将问题方法进问题字典
            question_type_dict['questions'].append(question_dict)
            question_id += 1

        # 将问题类型字典放进context
        context['question_types'].append(question_type_dict)

    return render(request, 'index.html', context)


def result(request):
    '''
        计算结果的视图
        模板页面的表单为：
        {
            "option1":"A"，
            "option2":"B",
            ,,,,
        }

        交给模板页面的字典为：
        {
            "name":"",
            "description":"",
        }
    '''

    # 定义所有的性格及其加分题目
    Extroversion = {
        "A": (3, 7, 10, 19, 23, 32, 62, 74, 79, 81, 83),
        "B": (13, 16, 26, 38, 42, 57, 68, 77, 85, 91),
        "score": 0,
        "name": "E",
    }  # E
    Introversion = {
        "A": (13, 16, 26, 38, 42, 57, 68, 77, 85, 91),
        "B": (3, 7, 10, 19, 23, 32, 62, 74, 79, 81, 83),
        "score": 0,
        "name": "I",
    }  # I
    Sensing = {
        "A": (2, 9, 25, 30, 34, 39, 50, 52, 54, 60, 63, 73, 92),
        "B": (5, 11, 18, 22, 27, 44, 46, 48, 65, 67, 69, 71, 82),
        "score": 0,
        "name": "S",
    }  # S
    Intuition = {
        "A": (5, 11, 18, 22, 27, 44, 46, 48, 65, 67, 69, 71, 82),
        "B": (2, 9, 25, 30, 34, 39, 50, 52, 54, 60, 63, 73, 92),
        "score": 0,
        "name": "N",
    }  # N
    Thinking = {
        "A": (31, 33, 35, 43, 45, 47, 49, 56, 58, 61, 66, 75, 87),
        "B": (6, 15, 21, 29, 37, 40, 51, 53, 70, 72, 89),
        "score": 0,
        "name": "T",
    }  # T
    Feeling = {
        "A": (6, 15, 21, 29, 37, 40, 51, 53, 70, 72, 89),
        "B": (31, 33, 35, 43, 45, 47, 49, 56, 58, 61, 66, 75, 87),
        "score": 0,
        "name": "F",
    }  # F
    Judge = {
        "A": (1, 4, 12, 14, 20, 28, 36, 41, 64, 76, 86),
        "B": (8, 17, 24, 55, 59, 78, 80, 84, 88, 90, 93),
        "score": 0,
        "name": "J",
    }  # J
    Perceive = {
        "A": (8, 17, 24, 55, 59, 78, 80, 84, 88, 90, 93),
        "B": (1, 4, 12, 14, 20, 28, 36, 41, 64, 76, 86),
        "score": 0,
        "name": "P",
    }  # P

    result = {
        "ISTJ": {
            "name": "检查员型",
            "description": "安静、严肃，通过全面性和可靠性获得成功。实际，有责任感。决定有逻辑性，并一步步地朝着目标前进，不易分心。喜欢将工作、家庭和生活都安排得井井有条。重视传统和忠诚。",
        },
        "ISFJ": {
            "name": "照顾者型",
            "description": "安静、友好、有责任感和良知。坚定地致力于完成他们的义务。全面、勤勉、精确，忠诚、体贴，留心和记得他们重视的人的小细节，关心他们的感受。努力把工作和家庭环境营造得有序而温馨。",
        },
        "INFJ": {
            "name": "博爱型",
            "description": "寻求思想、关系、物质等之间的意义和联系。希望了解什么能够激励人，对人有很强的洞察力。有责任心，坚持自己的价值观。对于怎样更好的服务大众有清晰的远景。在对于目标的实现过程中有计划而且果断坚定。 ",
        },
        "INTJ": {
            "name": "专家型",
            "description": "在实现自己的想法和达成自己的目标时有创新的想法和非凡的动力。能很快洞察到外界事物间的规律并形成长期的远景计划。一旦决定做一件事就会开始规划并直到完成为止。多疑、独立，对于自己和他人能力和表现的要求都非常高。 ",
        },
        "ISTP": {
            "name": "冒险家型",
            "description": "自己感兴趣的领域有超凡的集中精力深度解决问题的能力。多疑，有时会有点挑剔，喜欢分析。",
        },
        "ISFP": {
            "name": "艺术家型",
            "description": "安静、友好、敏感、和善。享受当前。喜欢有自己的空间，喜欢能按照自己的时间表工作。对于自己的价值观和自己觉得重要的人非常忠诚，有责任心。不喜欢争论和冲突。不会将自己的观念和价值观强加到别人身上。 ",
        },
        "INFP": {
            "name": "哲学家型",
            "description": "理想主义，对于自己的价值观和自己觉得重要的人非常忠诚。希望外部的生活和自己内心的价值观是统一的。好奇心重，很快能看到事情的可能性，能成为实现想法的催化剂。寻求理解别人和帮助他们实现潜能。适应力强，灵活，善于接受，除非是有悖于自己的价值观的。 ",
        },
        "INTP": {
            "name": "学者型",
            "description": "对于自己感兴趣的任何事物都寻求找到合理的解释。喜欢理论性的和抽象的事物，热衷于思考而非社交活动。安静、内向、灵活、适应力强。对于自己感兴趣的领域有超凡的集中精力深度解决问题的能力。多疑，有时会有点挑剔，喜欢分析。 ",
        },

        "ESTP": {
            "name": "挑战者型",
            "description": "灵活、忍耐力强，实际，注重结果。觉得理论和抽象的解释非常无趣。喜欢积极地采取行动解决问题。注重当前，自然不做作，享受和他人在一起的时刻。喜欢物质享受和时尚。学习新事物最有效的方式是通过亲身感受和练习。 ",
        },
        "ESFP": {
            "name": "表演者型",
            "description": "外向、友好、接受力强。热爱生活、人类和物质上的享受。喜欢和别人一起将事情做成功。在工作中讲究常识和实用性，并使工作显得有趣。灵活、自然不做作，对于新的任何事物都能很快地适应。学习新事物最有效的方式是和他人一起尝试。",
        },
        "ENFP": {
            "name": "公关型",
            "description": "热情洋溢、富有想象力。认为人生有很多的可能性。能很快地将事情和信息联系起来，然后很自信地根据自己的判断解决问题。总是需要得到别人的认可，也总是准备着给与他人赏识和帮助。灵活、自然不做作，有很强的即兴发挥的能力，言语流畅。",
        },
        "ENTP": {
            "name": "智多星型",
            "description": "反应快、睿智，有激励别人的能力，警觉性强、直言不讳。在解决新的、具有挑战性的问题时机智而有策略。善于找出理论上的可能性，然后再用战略的眼光分析。善于理解别人。不喜欢例行公事，很少会用相同的方法做相同的事情，倾向于一个接一个的发展新的爱好。 ",
        },
        "ESTJ": {
            "name": "管家型",
            "description": "实际、现实主义。果断，一旦下决心就会马上行动。善于将项目和人组织起来将事情完成，并尽可能用最有效率的方法得到结果。注重日常的细节。有一套非常清晰的逻辑标准，有系统性地遵循，并希望他人也同样遵循。在实施计划时强而有力。 ",
        },
        "ESFJ": {
            "name": "主人型",
            "description": "热心肠、有责任心、合作。希望周边的环境温馨而和谐，并为此果断地执行。喜欢和他人一起精确并及时地完成任务。事无巨细都会保持忠诚。能体察到他人在日常生活中的所需并竭尽全力帮助。希望自己和自己的所为能受到他人的认可和赏识。",
        },
        "ENFJ": {
            "name": "教导型",
            "description": "热情、为他人着想、易感应、有责任心。非常注重他人的感情、需求和动机。善于发现他人的潜能，并希望能帮助他们实现。能成为个人或群体成长和进步的催化剂。忠诚，对于赞扬和批评都会积极地回应。友善、好社交。在团体中能很好地帮助他人，并有鼓舞他人的领导能力。",
        },
        "ENTJ": {
            "name": "统帅型",
            "description": "坦诚、果断，有天生的领导能力。能很快看到公司/组织程序和政策中的不合理性和低效能性，发展并实施有效和全面的系统来解决问题。善于做长期的计划和目标的设定。通常见多识广，博览群书，喜欢拓广自己的知识面并将此分享给他人。在陈述自己的想法时非常强而有力。",
        },
    }

    context = {}

    # 遍历所有性格,并计算分数
    context['score'] = []
    positions = [Extroversion, Introversion, Sensing, Intuition, Thinking, Feeling, Judge, Perceive]
    for position in positions:

        # 对选项A进行处理
        for i in position['A']:
            if 'A' == request.POST["option" + str(i)]:
                position["score"] += 1

        # 对选项B进行处理
        for i in position['B']:
            if 'B' == request.POST["option" + str(i)]:
                position["score"] += 1

        # 将分数装好，传给模板页面
        context['score'].append(position["score"])

    print(context['score'])

    # 计算，你属于哪一种人格
    character = ""
    for i in range(0, 8, 2):
        if context['score'][i] < context['score'][i + 1]:
            character += positions[i]['name']
        else:
            character += positions[i + 1]['name']

    context['result'] = result[character]
    print(character)

    return render(request, 'result.html', context)
