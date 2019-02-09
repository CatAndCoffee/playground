# _*_ coding = utf-8 _*_
import requests
import re
import os
import time
from urllib.parse import quote

urlImageBase = 'http://n2.1whour.com/'
contentsURL = "http://m.kukudm.com/comiclist/527/"

contentsModel = re.compile("<a href=\'([\S|\w|\d]+.htm)\'>([\S]+)</a></li>")
reModel = re.compile(b"document.write\(\"<a\shref=\'([\S]*?.htm)\'><IMG\sSRC=\'\"[\S]*?\+\"([\S|\s]*?)\'></a>")
reErrorModel = re.compile(b"<!DOCTYPE html>")
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
}

response = requests.get(url=contentsURL, headers=header)
if response.status_code == 200:
    with open("tmpFile", 'wb') as tmp:
        tmp.write(response.content)
    with open('tmpFile', 'r', encoding='gbk') as f:
        text = f.readline()
    contents = contentsModel.findall(text)
    with open('content.txt', 'w', encoding='utf-8') as fw:
        length = len(contents)
        i = length - 1
        num = 1
        while i >= 0:
            fw.write("%d,%s,http://m.kukudm.com%s\n" % (num, contents[i][1], contents[i][0]))
            num = num + 1
            i = i - 1
    os.remove("./tmpFile")
else:
    print("Get content Error")
    exit(1)
with open('./content.txt', 'r', encoding='utf-8') as f:
    urlList = f.readlines()
i = 0  # i is the number of urlList
length = len(urlList)
while i < length:
    doc = urlList[i].split(',')
    dirName = doc[0] + doc[1]
    baseUrl = doc[2][:-6]
    os.mkdir("./" + str(dirName))
    dirName = dirName + '/'
    j = 1  # j is the number of imagePage
    while True:
        imagePage = baseUrl + str(j) + '.htm'
        response = requests.get(url=imagePage, headers=header)
        if response.status_code == 200:
            reFind = reModel.findall(response.content)
            if b"exit" in reFind[0][0]:
                urlImage = urlImageBase + quote(reFind[0][1])
                imageResponse = requests.get(url=urlImage, headers=header)
                while reErrorModel.match(imageResponse.content):
                    time.sleep(1)
                    imageResponse = requests.get(url=urlImage, headers=header)
                with open(str(dirName) + str(j) + str(reFind[0][1][-4:])[2:-1], 'wb') as f:
                    f.write(imageResponse.content)
                break
            urlImage = urlImageBase + quote(reFind[0][1])
            imageResponse = requests.get(url=urlImage, headers=header)
            while reErrorModel.match(imageResponse.content):
                time.sleep(1)
                imageResponse = requests.get(url=urlImage, headers=header)
            with open(str(dirName) + str(j) + str(reFind[0][1][-4:])[2:-1], 'wb') as f:
                f.write(imageResponse.content)
            j = j + 1
    i = i + 1
