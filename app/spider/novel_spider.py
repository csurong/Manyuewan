import requests
from bs4 import BeautifulSoup
import re

"""
Splider类
初始化无需参数
get_search_book_data(name) 返回书的信息，字典，yield
get_chapter_data(chapter_url) 返回章节地址和名称，字典，yield。chapter_url在书的信息中
get_chapter_text(content_url) 返回改章节的内容，已插入 <br> 排版。content_url 是章节的地址，上面有

bug：还有名称没有输完整会出现多页的情况，之后可以做进一步的修改
"""


class Spider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
        }

    def get_search_result_html(self, name):
        url = 'https://www.zwda.com/search.php?keyword=' + name
        requests.urllib3.disable_warnings()
        response = requests.get(url=url, headers=self.headers, verify=False)
        return response.text

    def get_search_book_data(self, name):
        """

        :return: dict -> book_data
        """
        html = self.get_search_result_html(name)
        soup = BeautifulSoup(html, 'lxml')

        num = len(soup.find_all(attrs={'class': 'result-item'}))
        book_data = {}  # 书的信息字典

        chapter_urls = soup.select(".result-game-item-title-link")
        images = soup.select(".result-game-item-pic-link-img")
        names = soup.select(".result-game-item-detail a span")
        descs = soup.select(".result-game-item-desc")
        authors = re.findall(r'<span.*?作者.*?<span>(.*?)</span>', html, re.S)
        novel_types = re.findall(r'<span.*?类型.*?-title">(.*?)</span>', html, re.S)
        refresh_times = re.findall(r'<span.*?时间.*?-title">(.*?)</span>', html, re.S)
        latests = re.findall(r'<a cpos=.*?ank">(.*?)</a>', html, re.S)

        for i in range(0, num):
            # 目录地址
            chapter_url = chapter_urls[i]['href'].strip()
            book_data['chapter_url'] = chapter_url
            # 封面
            image_src = images[i]['src'].strip()
            if image_src == '':
                images[i]['src'] = 'https://www.zwda.com/images/nocover.jpg'
            book_data['image_src'] = image_src
            # 书名
            name = names[i].get_text().strip()
            book_data['name'] = name
            # 简介
            desc = descs[i].get_text().strip()
            book_data['desc'] = desc
            # 作者
            author = authors[i].strip()
            book_data['author'] = author
            # 类型
            novel_type = novel_types[i].strip()
            book_data['novel_type'] = novel_type
            # 时间
            refresh_time = refresh_times[i].strip()
            book_data['refresh_time'] = refresh_time
            # 最新章节
            latest = latests[i].strip()
            book_data['latest'] = latest

            yield book_data

    def get_chapter_data(self, chapter_url):
        # 爬取每个章节的名字和链接，跟上面一样，字典返回
        chapter_html = requests.get(chapter_url, headers=self.headers)
        # 由于章节的页面头部并没有指定指点编码方式，默认是按照ISO-8859-1解码,会有乱码，下面需指定
        chapter_html.encoding = 'gbk'
        chapter_html = chapter_html.text

        soup = BeautifulSoup(chapter_html, 'lxml')
        num = len(soup.select("#list dl dd"))

        chapters_urls = soup.select("#list dd a")

        for i in range(0, num):
            data = {
                'content_url': "https://www.zwda.com" + chapters_urls[i]['href'].strip(),
                'chapter_name': chapters_urls[i].get_text().strip()
            }
            yield data

    def get_chapter_text(self, content_url):
        chapter_content = requests.get(content_url, headers=self.headers)
        chapter_content.encoding = 'gbk'
        content_html = chapter_content.text

        soup = BeautifulSoup(content_html, 'lxml')
        content = soup.find(attrs={'id': 'content'}).get_text()
        # 排版稍作调整。br直接作为字符存进去，之后渲染时直接传过去
        re_str = '\s+'
        content = re.sub(re_str, '<br><br>', content)
        return content
