import json
import urllib.request, urllib.parse, urllib.error

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .global_var import result_type, getter as get_var, setter as set_var, getter_ques as get_ques, \
    setter_ques as set_ques
from .tools import get_json, clac_score, get_result, get_questions


def get_client_ip(request):
    '''获取用户ip'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    '''关于index页面的视图'''

    data = {
        "appid": "wjxt",  # 设置应用系统的AppID，每个应用都不同，你要先去申请注册
        "appsecret": "57a97405ac28",  # 设置应用系统的appSecret，每个应用都不同，你要先去申请注册
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
            return HttpResponseRedirect('https://cas.dgut.edu.cn?appid=wjxt&state=STATE')
            # return HttpResponseRedirect('https://cas.dgut.edu.cn/Wechat?state=wjxt_*_STATE') #这里是微信登录用的

    # return HttpResponse(
    #     "Login success!\n your IP Address : {} {}".format(get_client_ip(request), request.session.get('username')))

    if get_ques() is None:
        set_ques(get_questions())
    context = get_ques()

    return render(request, 'index.html', context)
    # json_context = json.dumps(context, ensure_ascii=False)
    # return HttpResponse(json_context)


def result(request):
    """计算结果的视图"""
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
