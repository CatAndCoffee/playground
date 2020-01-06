前段时间接触了一下BeautifulSoup，用来练习一下使用方法。
爬取站点为“XX文库”，选择理由比较简单：一是因为正在看这个动漫想看看原著，但是手机端广告覆盖太严重；另外页面内文章默认为简体中文，因此不需要处理其中的js代码。
小说内容页面构成非常规范 *（比超炮那个网站强太多了）* ：
  - 章节标题标签：`<div id="title">`
  - 正文内容标签为：`<div id="content">`
  - 下一页导航标签为：`<a href="54900.htm">下一页</a>`
  - 小说插图标签为：`< img src="xxxxxx" border="0" class="imagecontent">`

对应的提取方法为：
  - 提取标题：`soup.find(id="title").get_text()`
  - 提取正文：`soup.find(id="content").get_text()`
  - 提取下一页url：
    ```python
    next_page = soup.find("a",string="下一页")
    try:
        next_url = re.findall(r"^<a href=\"(\d+.htm)", str(next_page))[0]
    except:
        next_url = None
    return next_url
    ```
  - 提取图片地址：
    ```python
    images = soup.find_all("img",class_='imagecontent')
    if len(images) > 0:
        for i in images:
            imgURL = i['src']
    ```
