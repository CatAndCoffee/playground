#!/usr/bin/python3
# -*- conding: utf-8 -*-
""" A script to get descriptions of files in Nirsoft.
There are too many useful tools in Nirsoft(https://www.nirsoft.net/)...
算了，我还是写中文吧，这个宝藏网站上边很多牛逼的工具，但是描述是英文的，因此想把里面的英文描述通过翻译API转换成中文。
一个小作坊式脚本，完成了网页中信息的提取，利用百度API翻译成中文，并以{id, 文件名, 详情页面url, 英文描述, 中文翻译} 的格式存入Mongodb数据库。

需要修改如下内容：
- MongoClient地址
- 网页来源
- 百度APIappid
- 百度API密钥

每一个文件在页面中的格式如下：
<tr class="filesrow"><td>
<a class="filetitle" href="web_browser_password.html">WebBrowserPassView v1.94</a><img src="../update.gif"><br>
WebBrowserPassView is a password recovery tool that reveals the passwords stored by the following Web browsers: Internet Explorer (Version 4.0 - 8.0), Mozilla Firefox (All Versions), Google Chrome, and Opera. This tool can be used to recover your lost/forgotten password of any Website, including popular Web sites, like Facebook, Yahoo, Google, and GMail, as long as the password is stored by your Web Browser.
After retrieving your lost passwords, you can save them into text/html/csv/xml file, by using the 'Save Selected Items' option (Ctrl+S).

"""

import re
import requests
import random
import hashlib
import json
import pymongo
import time
from bs4 import BeautifulSoup


MyClient = pymongo.MongoClient("mongodb://x.x.x.x:27017/") # MongoClient地址
MyDB = MyClient["Toolkit"]
MyCol = MyDB["FileList"]
Files = {}
pattern = re.compile(r'<a class="filetitle" href="([\s\S]*?)">([\S\s]*?)<\/a>[\s\S]*?<br/>([\S\s]*?)<(tr|/td|span)',
                     re.M)
MainUrl = "https://www.nirsoft.net/utils/"
number = 1


def translate(english):
    appid = ''  # 填写你的appid
    secretKey = ''  # 填写你的密钥
    apiUrl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    salt = random.randint(32768, 65536)
    sign = appid + english + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    PostData = {"q": english,
                "from": "en",
                "to": "zh",
                "appid": appid,
                "salt": salt,
                "sign": sign}
    req = requests.post(apiUrl, data=PostData, headers=headers)
    if req.status_code == 200:
        result = json.loads(req.content)
        try:
            transResult = result["trans_result"][0]["dst"] #提取翻译内容
            return transResult
        except:
            print("============ERROR==============\n") # 如果出错的话将错误信息打印至控制台
            print(req.content)
            return "Connect Error" # 在数据库中提示是因为百度API造成失败

    else:
        return "ERROE" # 记录其他错误


if __name__ == "__main__":
    soup = BeautifulSoup(open("nirsoft.html"), 'html.parser') # 网页来源
    allTables = soup.find_all('table', class_="filestable")
    # 这里class是python的关键字，所以需要在后边接一个下划线
    print(len(allTables))
    for Tables in allTables:
        Re_Result = pattern.findall(str(Tables))
        for item in Re_Result:
            Raw_description = item[2]
            Description = Raw_description.replace('\n', ' ') # 处理一些影响观感的字符
            Description = Description.replace('<p>', ' ')
            Description = Description.replace('<br/>', ' ')
            Description = Description.replace('&gt;', '>')
            Description = Description.replace('&lt;', '<')
            Description = Description.replace('</a>', '')
            DelExtraBlank = re.compile(r'\s{2,}')
            Description = DelExtraBlank.sub(' ', Description) # 删除多余的空格
            ahref2Help = re.compile(r'<a href="[\s\S]*?">')
            Description = ahref2Help.sub('[help]', Description) # 处理描述中的超级链接
            zh_cnDescription = translate(Description) # 调用翻译
            mydict = {"id": number, "FileName": item[1], "Url": MainUrl + item[0], "Description": Description,
                    "zh_Description": zh_cnDescription}
            x = MyCol.insert_one(mydict)
            number += 1 # 计数器
            print("id:{}  File:{}".format(number, item[1])) # 在终端显示进度
            time.sleep(random.randint(2, 5)) # 百度接口调用不能太快



"""
学到的一些东西：
1. BeautifulSoup中直接用标签名获得标签对象的方法，只能获得所有该标签的第一内容
2. 使用find_all才能获取到所有标签的对象，获取时与python关键字冲突的名称需要在后面加"_"
3. 如何获取标签对象中的字符串？直接str() 就可以
"""
