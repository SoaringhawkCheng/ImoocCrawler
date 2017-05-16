# -*- encoding=utf-8 -*-

import requests
import cookielib
import re

session = requests.Session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print "Load Cookies Faild"
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
header = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
    'User-Agent':agent
}



def get_xsrf():
    # response = requests.get("https://www.zhihu.com",headers=header)
    # print response.text
    text = '<input type="hidden" name="_xsrf" value="8081a1a8e85682afd666e79b0be774aa"/>'
    match_obj = re.match('.*name="_xsrf" value="(.*?)"',text)
    print match_obj.group(1)
    return match_obj.group(1)


def zhihu_login(account,password):
    #知乎登陆
    if re.match("^1\d{10}",account):
        print "手机号码登录"
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "xsrf": "",
            "phone_num":account,
            "password":password
        }
        response_text = session.post(post_url,data=post_data,headers=header)
        response_text.cookies.save()
get_xsrf()