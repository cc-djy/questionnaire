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
            'question_type_id':question_type.question_type_id,
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
                    'option_num_id':option_id,
                    'option_description': option.option_description
                })  # 将选项放进问题字典
                option_id += 1

            # 将问题方法进问题字典
            question_type_dict['questions'].append(question_dict)
            question_id += 1

        # 将问题类型字典放进context
        context['question_types'].append(question_type_dict)

    return render(request, 'index.html', context)
