import requests
import re
from lxml import etree
import ddddocr
import time
import logging
import random
import os
from configparser import RawConfigParser

#日志初始化
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='my.log',level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT)

#当前目录获取
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep

#获取账号参数
try:
    configinfo = RawConfigParser()
    try:
        configinfo.read(pwd + 'id.ini',encoding='UTF-8')
    except Exception as e:
        with open(pwd + 'id.ini','r',encoding='UTF-8') as config:
            getconfig = config.read().encode('utf-8').decode('utf-8-sig')
        with open(pwd + 'id.ini','w',encoding='UTF-8') as config:
            config.write(getconfig)
        try:
            configinfo.read(pwd + "id.ini", encoding="UTF-8")
        except:
            configinfo.read(pwd + "id.ini", encoding="gbk")
    user = configinfo.get('main','user')
except Exception as e:
    OpenCardConfigLabel = 1
    print("参数配置有误，请检查id.ini\nError:", e)
    
#地址
ocr = ddddocr.DdddOcr()
HTMLPAGE = "https://ksxskj.hevttc.edu.cn/"
LOGIN = "login/?next=/"
add_tw = "https://ksxskj.hevttc.edu.cn/NCIR/user_data/add/"
CHECKCODE = "getcheckimg/"
checkcodee = "checkcode.jpg"
#cookie获取
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
            #print("验证码错误")
            return None
        else:
            ck_jar = requests.utils.cookiejar_from_dict(getcookies)
            return ck_jar
#读取配置信息
def isuser():
    usernamelists = []
    passwordlists = []
    locationlists = []
    if 'username=' in user and 'password=' in user and 'location=' in user:
        u = re.compile(r'username=(.*?);',re.M | re.S | re.I)
        p = re.compile(r"password=(.*?);",re.M | re.S | re.I)
        l = re.compile(r'location=(.*?);',re.M | re.S | re.I)
        result_u = u.findall(user)
        result_p = p.findall(user)
        result_l = l.findall(user)
        if len(result_u) >= 1:
            print('已配置{}个账号'.format(len(result_u)))
            for x in result_u:
                usernamelists.append(x)
            for y in result_p:
                passwordlists.append(y)
            for z in result_l:
                locationlists.append(z)
        return usernamelists,passwordlists,locationlists

#填体温
def addtw():
    headers = {
        "Host": "ksxskj.hevttc.edu.cn",
        "Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Android",
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
        "Connection": "close"
    }
    usernames,passwords,locations = isuser()
    for us,pw,lc in zip(usernames,passwords,locations):
        start = time.perf_counter()
        ass = denglu(us,pw)
        cookies = ass.get_cookie_login()
        if cookies != None:
            data1 = ""
            get_crsftoken = requests.get(url=add_tw, data=data1, cookies=cookies)
            text = get_crsftoken.text
            xpaths = etree.HTML(text)
            csrfmiddlewaretoken = xpaths.xpath('//div[@id="content-main"]/form/input/@value')
            if len(csrfmiddlewaretoken) != False:
                try:
                    csmt = csrfmiddlewaretoken[0]
                    lst = ['36.1', '36.2', '36.3', '36.4']
                    number = random.choice(lst)
                    data = {
                        "csrfmiddlewaretoken": csmt,
                        'tw': number,  # 体温
                        "fl": "False",  # 乏力
                        "gk": "False",  # 干咳
                        "hx": "False",  # 呼吸
                        "qt": "False",  # 其他
                        "jc": "False",  # ？？
                        "fx": "False",  # 腹泻
                        "lc": lc,  # 地点，配置文件中
                        "actionName": "actionValue",
                    }
                    response = requests.post(url=add_tw, headers=headers, cookies=cookies, data=data)
                    if response.status_code == 200:
                        print("账号{}保存体温{}°成功".format(us, number))
                        logging.info("账号{}保存体温{}°成功".format(us, number))
                except:
                    print("账号{}已经保存过体温".format(us))
                    logging.info("账号{}已经保存过体温".format(us))
            else:
                print("账号{}已经保存过体温".format(us))
                logging.info("账号{}已经保存过体温".format(us))
        else:
            print("账号{}登陆失败".format(us))
            logging.info("账号{}登陆失败".format(us))
        endtime = time.perf_counter()
        print('账号{}运行时间{}秒'.format(us,endtime-start))
        logging.info("账号{}运行时间{}秒".format(us,endtime-start))
        
if __name__ == "__main__":
    addtw()
#结束
