import requests
import re
import os
import sys

UrlRoot = "https://upload.cnblogs.com/imageuploader/processupload?host=www.cnblogs.com&qqfile="
# Proxy = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
Proxy = {}
Header = {'Host': 'upload.cnblogs.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
          'Accept': '*/*', 'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3', 'Accept-Encoding': 'gzip, deflate',
          'X-Requested-With': 'XMLHttpRequest',
          'Cache-Control': 'no-cache', 'Content-Type': 'application/octet-stream',
          'Origin': 'https://upload.cnblogs.com', 'Connection': 'close',
          'Referer': 'https://upload.cnblogs.com/imageuploader/upload?host=www.cnblogs.com&editor=4'}
Cookie = {}


# 'X-Mime-Type': 'image/png'
# 'X-File-Name': '%E4%BA%94%E5%8D%81%E9%9F%B3.png',

def upload(filepath, filename):
    repattern = re.compile(r"\"message\":\"(\S*)\"")
    # mime_type = magic.from_file(filename,mime=True)
    url = UrlRoot + filename
    if filename[-3:] == 'jpg':
        Header['X-Mime-Type'] = 'image/' + 'jpeg'
    elif filename[-3:] == 'png':
        Header['X-Mime-Type'] = 'image/' + 'png'
    else:
        MimeType = input("Plz set type of %s" % filename)
        Header['X-Mime-Type'] = 'image/' + MimeType
    Header['X-File-Name'] = filename
    # print(Header)
    # print("URL:{}\nHeader:{}\nFilepath:{}\n".format(url,Header,filepath))
    # return '12321'
    with open(filepath, 'rb') as f:
        try:
            r = requests.post(url, headers=Header, cookies=Cookie, data=f, proxies=Proxy, verify=False)
            return repattern.findall(r.text)[0]
        except:
            print("Get Error")
            return None


def getPic(mdfile):
    # ![1538469977801](初音.assets/1538469977801.png)
    reText = re.compile(r"\!\[\S*\]\((\S*)\)")
    with open(mdfile, 'r', encoding='utf-8') as f:
        with open('upload_' + mdfile, 'w', encoding='utf-8') as fw:
            for line in f.readlines():
                picture = reText.findall(line)
                if len(picture):
                    workpath = os.getcwd()
                    picpath = workpath + "\\" + picture[0].replace('/', '\\')
                    # ![image-20191219125001416](AppWeb.assets/image-20191219125001416.png)
                    filename = picture[0].split('/')[1]
                    cnpath = upload(picpath, filename)
                    if cnpath:
                        outpath = re.sub(r"\((\S*)\)", "(%s)" % cnpath, line)
                        fw.write(outpath + '\n')
                else:
                    fw.write(line)


def modifyCookie(text):
    global Cookie
    deletHeader = text[8:]
    for item in deletHeader.split('; '):
        index = item.find('=')
        Cookie[item[:index]] = item[index + 1:]


if __name__ == "__main__":
    """
    getPic输入文件名，生成"upload_文件名.md"
    """
    rawCookie ="" # 博客园的cookie
    modifyCookie(rawCookie)
    os.chdir("") # markdown文件和图片文件夹的位置
    getPic("") #markdown文档名
