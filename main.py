import requests
from lxml import etree
import ddddocr
import time
import random
ocr = ddddocr.DdddOcr()
HTMLPAGE = "https://ksxskj.hevttc.edu.cn/"
LOGIN = "login/?next=/"
CHECKCODE = "getcheckimg/"
checkcodee = "checkcode.jpg"
class denglu:
    def __init__(self,username,password):
        self.username = username        #账号
        self.password = password        #密码
        self.session = requests.session()       #同一个请求
        self.checkcode = ""        #验证码
        self.csrftoken = self.getcsrftoken()        #setcookie文件
        self.sessionid = self.getsessionid()
        self.csrfmiddlewaretoken = self.get_csrfmiddlewaretoken()
    def getcsrftoken(self):
        self.session.get(HTMLPAGE + LOGIN)
        html = requests.utils.dict_from_cookiejar(self.session.cookies)
        print("csrftoken = " + html['csrftoken'])
        return html['csrftoken']
    def getsessionid(self):
        cookies = {
            "csrftoken": self.csrftoken,
        }
        code = self.session.get(url=HTMLPAGE + CHECKCODE, cookies=cookies)
        img_code = code.content
        with open(checkcodee, 'wb') as f:
            f.write(img_code)
        imgcode = open(checkcodee,'rb').read()#验证码
        self.checkcode = ocr.classification(imgcode)
        html = requests.utils.dict_from_cookiejar(self.session.cookies)
        print("sessionid = " + html['sessionid'])
        return html['sessionid']
    def get_csrfmiddlewaretoken(self):
        cookies = {
            "csrftoken": self.csrftoken,
            "sessionid": self.sessionid,
        }
        data = ""
        get_crsftoken = requests.get(url=HTMLPAGE, data=data, cookies=cookies)
        xpaths = etree.HTML(get_crsftoken.text)
        csrfmiddlewaretoken = xpaths.xpath('//div[@class="login-main"]/form[@id="login-form"]/input/@value')
        #print("csrfmiddlewaretoken = " + csrfmiddlewaretoken[0])
        return csrfmiddlewaretoken[0]
    def get_cookie_login(self):
        headers = {
            "Content-Length":"150",
            "Cache-Control":"max-age=0",
            "Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"97\"",
            "ec-Ch-Ua-Mobile":"?0",
            "Sec-Ch-Ua-Platform":"Android",
            "Upgrade-Insecure-Requests":"1",
            "Origin":"https://ksxskj.hevttc.edu.cn",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site":"same-origin",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-User":"?1",
            "Sec-Fetch-Dest":"document",
            "Referer":"https://ksxskj.hevttc.edu.cn/login/?next=/",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"close",
        }
        data = {
            "csrfmiddlewaretoken":self.csrfmiddlewaretoken,
            "username":self.username,
            "password":self.password,
            "check_code":self.checkcode,
            "next":"%2F",
        }
        cookies = {
            "csrftoken":self.csrftoken,
            "sessionid":self.sessionid,
        }
        self.session.post(url=HTMLPAGE+LOGIN,data=data,headers=headers,cookies=cookies)
        getcookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        if getcookies['csrftoken'] == self.csrftoken:
            print("验证码错误")
            getcookies= None
        else:
            print(getcookies)
        return getcookies
class TW:
    def __init__(self,csrftoken,sessionid):
        self.add_tw = "https://ksxskj.hevttc.edu.cn/NCIR/user_data/add/"
        self.csrftoken = csrftoken
        self.sessionid = sessionid
        self.csrfmiddlewaretoken = self.get_csrfmiddlewaretoken()
    def get_csrfmiddlewaretoken(self):
        cookies_1 = {
            "sessionid": self.sessionid,
            "csrftoken": self.csrftoken,
        }
        data1 = ""
        get_crsftoken = requests.get(url=self.add_tw, data=data1, cookies=cookies_1)
        text = get_crsftoken.text
        xpaths = etree.HTML(text)
        csrfmiddlewaretoken = xpaths.xpath('//div[@id="content-main"]/form/input/@value')
        return csrfmiddlewaretoken[0]
    def tw_add(self):
        lst = ['36.1', '36.2', '36.3', '36.4']
        number = random.choice(lst)
        headers = {
            "Host": "ksxskj.hevttc.edu.cn",
            "Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"99\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Origin": "https://ksxskj.hevttc.edu.cn",
            "Referer": "https://ksxskj.hevttc.edu.cn/NCIR/user_data/add/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive"
        }
        cookies = {
            "sessionid": self.sessionid,
            "csrftoken": self.csrftoken,
        }
        data = {
            "csrfmiddlewaretoken":self.csrfmiddlewaretoken,
            'tw':number,#体温
            "fl": "False",#乏力
            "gk": "False",#干咳
            "hx": "False",#呼吸
            "qt": "False",#其他
            "jc": "False",#？？
            "fx": "False",#腹泻
            "lc": " ",#位置，中文输入就可以例如：北京市 丰台区
            "actionName": "actionValue",
        }
        response = requests.post(url=self.add_tw,headers=headers,cookies=cookies,data=data)
        if response.status_code == 200:
            print("保存体温为{}度".format(number))
        else:
            print("保存失败")
if __name__ == "__main__":
    starttime = time.perf_counter()
    ass = denglu('username','password')#账号，密码
    cookie = ass.get_cookie_login()
    csrftoken = cookie['csrftoken']
    sessionid = cookie['sessionid']
    ss = TW(csrftoken=csrftoken,sessionid=sessionid)
    ss.tw_add()
    endtime = time.perf_counter()
    print('本次运行时间{.2f}秒'.format(endtime - starttime))




