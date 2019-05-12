import json
import random
import urllib.request, urllib.parse, urllib.error
from user_agents import parse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .global_var import result_type, getter as get_var, setter as set_var, getter_ques as get_ques, \
    setter_ques as set_ques, get_app_secret, get_app_id
from .tools import get_json, clac_score, get_result, get_questions, get_client_ip


def test(request):
    if get_ques() is None:
        set_ques(get_questions())
        print("hello")
    context = get_ques()

    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    print(user_agent.is_mobile)

    return render(request, 'index.html', context)

    # return render(request, 'index.html', context)


def mbti(request):
    context = {}
    # 上线时，这里要解封
    if login(request) is False:
        ua_string = request.META['HTTP_USER_AGENT']
        user_agent = parse(ua_string)

        if user_agent.is_mobile:
            return HttpResponseRedirect('https://cas.dgut.edu.cn/Wechat?state=wjxt_*_STATE')  # 这里是微信登录用的
        else:
            return HttpResponseRedirect('https://cas.dgut.edu.cn?appid=wjxt&state=STATE')

    ######

    return render(request, 'mbti.html', context)


def login(request):
    data = {
        "appid": get_app_id(),  # 设置应用系统的AppID，每个应用都不同，你要先去申请注册
        "appsecret": get_app_secret(),  # 设置应用系统的appSecret，每个应用都不同，你要先去申请注册
        'token': request.GET.get('token'),  # 获取token
        'userip': get_client_ip(request),  # 获取用户ip
    }

    # 判断是否已登录
    if request.session.get('username', False) is False:
        # 判断是否有token
        if request.GET.get('token', False):
            # 利用token、appid，appsecret 去获取access_token，openid
            details = urllib.parse.urlencode(data).encode("utf-8")
            url = urllib.request.Request("https://cas.dgut.edu.cn/ssoapi/v2/checkToken", details)
            responseData = urllib.request.urlopen(url).read().decode('utf-8')

            # 通过access_token和openid获取个人信息
            responseData = json.loads(responseData)
            details = urllib.parse.urlencode(responseData).encode("utf-8")
            url = urllib.request.Request("https://cas.dgut.edu.cn/oauth/getUserInfo", details)
            user_info = urllib.request.urlopen(url).read().decode('utf-8')

            user_info = json.loads(user_info)

            # 将用户信息保存到 session
            request.session['username'] = user_info['username']
            request.session['name'] = user_info['name']
            request.session['wx_openid'] = user_info['wx_openid']
            request.session['group'] = user_info['group']
            request.session['openid'] = user_info['openid']
        else:
            return False
    return True


def index(request):
    """关于index页面的视图"""
    if get_ques() is None:
        set_ques(get_questions())
    context = get_ques()

    # return render(request, 'index.html', context)

    response = JsonResponse(context)
    return HttpResponse(response, content_type='application/json')


def result(request):
    """计算结果的视图"""
    from .models import CommitRecord, SelectRecord
    if request.method != "POST":
        return None
    try:
        commit_record = CommitRecord(

            user_openid=request.session.get('wx_openid'),
            user_id=request.session.get('username'),

            client_time=timezone.now(),
            server_time=timezone.now(),
        )
    except Exception as e:
        commit_record = CommitRecord(
            user_openid='a28c64d4b9cf' + str(random.randint(1000000, 9999999)) + '504b9584510',
            user_id="2013" + str(random.randint(1000000, 9999999)),
            client_time=timezone.now(),
            server_time=timezone.now(),
        )

    commit_record.save()
    print(commit_record.commit_id)

    remark_list = []
    if get_var() is None:
        set_var(get_json())
    remark_dict = get_var()

    select_record_list = []
    for i in range(1, 93 + 1):
        select = ord(request.POST["option{}".format(i)]) - 64
        remark_list.append(remark_dict[i][1][select][1])
        select_record = SelectRecord(
            commit_id=commit_record.commit_id,
            question_id=remark_dict[i][0],
            option_id=remark_dict[i][1][select][0],
        )
        select_record_list.append(select_record)

    SelectRecord.objects.bulk_create(select_record_list)

    character = result_type[get_result(clac_score(remark_list))]

    return render(request, 'result.html', character)
