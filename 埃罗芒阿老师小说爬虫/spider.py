'''
页面主体在 <div id="contentmain"> 标签内
标题为 <div id="title">
正文为 <div id="content">
下一页 <a href="54900.htm">下一页</a>
'''

import requests
from bs4 import BeautifulSoup
import re

header = {'Host': 'www.xxx.net',
          'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br',
          'Connection': 'keep-alive'}
UrlRoot ="https://www.xxx.net/novel/1/1538/"
NextUrl = "51563.htm"
numberOfimages = 1


def get_page(url,f):
    global numberOfimages
    r = requests.get(UrlRoot+url,headers=header)
    r.encoding='gbk'
    soup = BeautifulSoup(r.text,'html.parser')
    images = soup.find_all("img",class_='imagecontent')
    if len(images) > 0:
        for i in images:
            print(i['src'])
            image = requests.get(i['src'])
            if image.content :
                with open("%d.jpg"%numberOfimages,'wb') as imageFile:
                    imageFile.write(image.content)
                numberOfimages = numberOfimages+1

    title = soup.find(id="title").get_text()
    f.write(title)
    content = soup.find(id="content").get_text()
    f.write(content)
    next_page = soup.find("a",string="下一页")
    try:
        next_url = re.findall(r"^<a href=\"(\d+.htm)", str(next_page))[0]
    except:
        next_url = None
    return next_url

if __name__=='__main__':
    with open('text','a') as f:
        NextUrl = get_page(NextUrl, f)
        while(1):
            if NextUrl:
                NextUrl = get_page(NextUrl, f)
                print(NextUrl)
            else:
                break



