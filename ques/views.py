import json

from django.http import HttpResponse
from django.shortcuts import render
from .global_var import result_type, getter as get_var, setter as set_var, getter_ques as get_ques, setter_ques as set_ques
from .tools import get_json, clac_score, get_result, get_questions


# @cache_page(60 * 15)  # 不使用缓存了
def index(request):
    """
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
    """
    if get_ques() is None:
        set_ques(get_questions())
    context = get_ques()

    # json_context = json.dumps(context, ensure_ascii=False)
    return render(request, 'index.html', context)
    # return HttpResponse(json_context)


def result(request):
    """
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
    """
    if request.method != "POST":
        return None

    remark_list = []
    if get_var() is None:
        set_var(get_json())
    remark_dict = get_var()

    for i in range(1, 93 + 1):
        select = ord(request.POST["option{}".format(i)]) - 64
        remark_list.append(remark_dict[i][1][select][1])

    character = result_type[get_result(clac_score(remark_list))]

    return render(request, 'result.html', character)
