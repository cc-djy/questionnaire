import requests
import urllib.request, urllib.parse, urllib.error
from django.test import TestCase

# Create your tests here.

def get_response():
    # details = repr(data).encode("utf-8")
    details = urllib.parse.urlencode(data).encode("utf-8")
    url = urllib.request.Request("https://cas.dgut.edu.cn/ssoapi/v2/checkToken", details)
    responseData = urllib.request.urlopen(url).read().decode('utf-8')

    print(responseData)

data = {
    "appid": "wjxt",  # 设置应用系统的AppID，每个应用都不同，你要先去申请注册
    "appsecret": "57a97405ac28",  # 设置应用系统的appSecret，每个应用都不同，你要先去申请注册
    'userip': "219.222.189.72",
    'token': "wjxt-z-d3ac27dcd5d3db4e6ae22cee445d5934"
}

# headers = {'content-type': 'application/json'}
# result = requests.post("https://cas.dgut.edu.cn/ssoapi/v2/checkToken", data=data, headers=headers)
#
# print(result.text)

get_response()


'''
{'appid': 'wjxt', 'appsecret': '57a97405ac28', 'token': 'wjxt-z-8aacfd6a426af47540e1e2db0139152f', 'userip': '172.28.7.29'} 
your IP Address : 172.28.7.29 
{"error":0,"message":"success","openid":"7b605e82f73655a15bf7bfd60f245a1f","access_token":"f34f9e47989ec10bc1c87ecaeeca82af"}
'''