import requests
import random
from lxml import etree
sessionid = "1o2rmek0x0mi6mbb1dtu9r9z7m5fsi29"
csrftoken = "Jl2OEGaSpJAHAXg8PLt4gtfSwLpFKpkkTJFYJqiVtrTPccX9ByOC2zpWvmK4Phcb"
def get_csrfmiddlewaretoken():
    url_cookies = "https://ksxskj.hevttc.edu.cn/NCIR/user_data/add/pmbt/"
    cookies_1 = {
            "sessionid":sessionid,
            "csrftoken":csrftoken,
        }
    data1 = ""
    get_crsftoken = requests.get(url=url_cookies,data=data1,cookies=cookies_1)
    text = get_crsftoken.text
    xpaths = etree.HTML(text)
    csrfmiddlewaretoken = xpaths.xpath('//div[@id="content-main"]/form/input/@value')
    return csrfmiddlewaretoken[0]
csrfmiddlewaretoken = get_csrfmiddlewaretoken()

#随机生成体温
lst = ['36.1','36.2','36.3','36.4']
number_chen = random.choice(lst)
#主url
url = "https://ksxskj.hevttc.edu.cn/NCIR/user_data/add/"
#晨午体温路径-需要修改，请自行抓包获取（晚上的修改时候的数据包有路径）
#配置请求头
headers = {
    "Host":"ksxskj.hevttc.edu.cn",
    "Sec-Ch-Ua":"\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"99\"",
    "Sec-Ch-Ua-Mobile":"?0",
    "Sec-Ch-Ua-Platform":"Windows",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site":"none",
    "Sec-Fetch-Mode":"navigate",
    "Sec-Fetch-User":"?1",
    "Sec-Fetch-Dest":"document",
    "Origin": "https://ksxskj.hevttc.edu.cn",
    "Referer":"https://ksxskj.hevttc.edu.cn/NCIR/user_data/add/",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive"
}

#配置cookie-需要修改，请自行抓包获取
cookies = {
    "sessionid":sessionid,
    "csrftoken":csrftoken,
    }

#配置发送数据 其中csrfmiddlewaretoken为必须，请自行抓包获取
data_chen = {
    "csrfmiddlewaretoken":csrfmiddlewaretoken,
    #体温
    "tw":number_chen,
    #乏力
    "fl":"False",
    #干咳
    "gk":"False",
    #呼吸？或许是鼻塞
    "hx":"False",
    #其他
    "qt":"False",
    #？？未知 或许是流涕
    "jc":"False",
    #腹泻
    "fx":"False",
    ###？？？未知
    #"jqjc"="",
    'lc':"河北省 石家庄市 栾城区",
    "actionName":"actionValue",
    }

xg_chentw = requests.post(url,data = data_chen,cookies=cookies,headers=headers)
if xg_chentw.status_code == 200:
    print(xg_chentw.text)
    print("保存体温为{}度".format(number_chen))
else:
    print("{}".format("失败"))