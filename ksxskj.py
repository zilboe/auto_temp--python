import requests
from lxml import etree
import ddddocr
import random

"""
来自孙和雷的科师空间脚本
使用https://github.com/sml2h3/ddddocr进行验证码识别
"""


def login(username, password):
    login1 = "https://ksxskj.hevttc.edu.cn/"
    login2 = "https://ksxskj.hevttc.edu.cn/getcheckimg/"
    login3 = "https://ksxskj.hevttc.edu.cn/login/?next=/"
    session = requests.session()
    csrf = session.get(login1)
    png = session.get(login2)
    xpaths = etree.HTML(csrf.text)
    csrfmiddlewaretoken = xpaths.xpath('///form[@id="login-form"]/input/@value')
    html = requests.utils.dict_from_cookiejar(session.cookies)
    headers = {
        "Content-Length": "150",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"97\"",
        "ec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Android",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://ksxskj.hevttc.edu.cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://ksxskj.hevttc.edu.cn/login/?next=/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close",
    }

    # 识别验证码
    ocr = ddddocr.DdddOcr()
    captcha = ocr.classification(png.content)
    cookies = {
        "csrftoken": html['csrftoken'],
        "sessionid": html['sessionid'],
    }
    # 封装数据
    data = {
        "csrfmiddlewaretoken": csrfmiddlewaretoken[0],
        "username": username,
        "password": password,
        "check_code": str(captcha).replace(" ", ""),
        "next": "%2F"
    }
    session.post(url=login3, data=data, headers=headers, cookies=cookies)
    login_cookies = requests.utils.dict_from_cookiejar(session.cookies)
    return login_cookies


def tem_xg(csrftoken, sessionid, local):
    url = "https://ksxskj.hevttc.edu.cn/NCIR/user_data/add/"

    cookies = {
        "csrftoken": csrftoken,
        "sessionid": sessionid
    }

    # 随机生成体温

    lst = ['36.3', '36.4', '36.5', '36.6']
    number_tw = random.choice(lst)

    # 配置请求头
    headers = {
        "Content-Length": "179",
        "Cache-Control": "max-age=0",
        "Host": "ksxskj.hevttc.edu.cn",
        "Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://ksxskj.hevttc.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://ksxskj.hevttc.edu.cn/NCIR/user_data/add/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }

    # 获取csrfmiddlewaretoken
    def get_csrfmiddlewaretoken():
        url_cookies = "https://ksxskj.hevttc.edu.cn/NCIR/user_data/add/pmbt/"
        get_csrfmiddlewaretoken = requests.get(url=url_cookies, cookies=cookies)
        xpaths = etree.HTML(get_csrfmiddlewaretoken.text)
        csrfmiddlewaretoken = xpaths.xpath('//div[@id="content-main"]/form/input/@value')
        return csrfmiddlewaretoken[0]

    # 配置发送数据
    data = {
        "csrfmiddlewaretoken": get_csrfmiddlewaretoken(),
        # 体温
        "tw": number_tw,
        # 乏力
        "fl": "False",
        # 干咳
        "gk": "False",
        # 呼吸？或许是鼻塞
        "hx": "False",
        # 其他
        "qt": "False",
        # ？？未知 或许是流涕
        "jc": "False",
        # 腹泻
        "fx": "False",
        # 未知
        # "jqjc":"",
        # 位置 。。不需要编码
        "lc": local,
        "actionName": "actionValue",
    }
    xg_tw = requests.post(url, data=data, cookies=cookies, headers=headers)
    print("体温修改状态为" + xg_tw.text)


if __name__ == "__main__":
    # 账号密码输入处
    data = (["账号", "密码", "某某省 某某市 某某县"], ["123123", "456456", "789789"])
    for under in range(0, len(data)):
        cookie = login(data[under][0], data[under][1])
        tem_xg(cookie['csrftoken'], cookie['sessionid'], data[under][2])
