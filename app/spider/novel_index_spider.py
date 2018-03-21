# _*_ coding:utf-8 _*_

"""
基本目标是自动获取首页更新的novels，信息还是那些信息
获取小说的信息后，为避免重复和实时的更新，爬取小说后，名字数据库比对
"""

import requests
from bs4 import BeautifulSoup
from app import db
from app.models import Novel
import time


class IndexSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
        }
        self.url = 'https://www.zwda.com'

    def get_book_data(self, chapter_html):
        data = {}  # 书的信息字典
        soup = BeautifulSoup(chapter_html, 'lxml')

        data['chapter_url'] = soup.select('[property="og:novel:read_url"]')[0]['content'].strip()
        data['image_src'] = soup.select('[property="og:image"]')[0]['content'].strip()
        data['name'] = soup.select('[property="og:novel:book_name"]')[0]['content'].strip()
        data['desc'] = soup.select('[property="og:description"]')[0]['content'].strip()
        data['author'] = soup.select('[property="og:novel:author"]')[0]['content'].strip()
        data['novel_type'] = soup.select('[property="og:novel:category"]')[0]['content'].strip()
        data['refresh_time'] = soup.select('[property="og:novel:update_time"]')[0]['content'].strip()
        data['latest'] = soup.select('[property="og:novel:latest_chapter_name"]')[0]['content'].strip()

        return data

    def get_latest_novel(self):
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'gbk'
        html = response.text

        soup = BeautifulSoup(html, 'lxml')
        all_chapter_urls = soup.select('#newscontent .l .s2 a')
        search_word = str(time.time())  # 获取一个唯一字符串，用来作为这十本书的共同标记

        # 首页展示十部最新更新的小说。如果需要这边可以改。最多可以改到chapter_urls的长度
        for i in range(0, 12):
            # 获取这本小说网站目录页面的 html.从这个页面中抓取各小说的详细信息。而另一个实在搜索结果页面抓取的，不一样
            chapter_url = self.url + all_chapter_urls[i]['href'].strip()
            chapter_response = requests.get(chapter_url, headers=self.headers)
            chapter_response.encoding = 'gbk'
            chapter_html = chapter_response.text
            data = self.get_book_data(chapter_html)
            data['search_word'] = search_word
            # print(data)
            novel = Novel(
                name=data['name'],
                image_src=data['image_src'],
                chapter_url=data['chapter_url'],
                desc=data['desc'],
                author=data['author'],
                novel_type=data['novel_type'],
                refresh_time=data['refresh_time'],
                latest=data['latest'],
                search_word=data['search_word']
            )
            if Novel.query.filter_by(name=data['name']).first() is None:  # 如果这本书不存在
                db.session.add(novel)  # 把这十本书存入novel数据库，这样就能跟前面的爬虫对上了
            else:
                # 如果这本书已经存在了，就把更新时间，最新章节，十本书的共同标记更新一下
                novel = Novel.query.filter_by(name=data['name']).first()
                novel.refresh_time = data['refresh_time']
                novel.latest = data['latest']
                novel.search_word = data['search_word']
                db.session.add(novel)
        # 数据库中检索按照之前给的这十本书的共同标记来选
        novels = Novel.query.filter_by(search_word=search_word).all()
        # print('novels数据爬虫已经返回')
        return novels


def main():
    index_spider = IndexSpider()
    index_spider.get_latest_novel()


if __name__ == "__main__":
    main()
