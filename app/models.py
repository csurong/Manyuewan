# _*_ coding:utf-8 _*_

from datetime import datetime
from app import db


# 书的数据模型
class Novel(db.Model):
    __tablename__ = 'novel'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100))  # 书名
    image_src = db.Column(db.String(233))  # 图片地址
    chapter_url = db.Column(db.String(233))  # 目录地址
    desc = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(100), nullable=True)
    novel_type = db.Column(db.String(100), nullable=True)
    refresh_time = db.Column(db.String(100), nullable=True)
    latest = db.Column(db.String(100), nullable=True)
    search_word = db.Column(db.String(100), nullable=True, index=True)
    spider_time = db.Column(db.DateTime, default=datetime.now())

    chapters = db.relationship('Chapter', backref='novel')

    def __repr__(self):
        return "<novel {}>".format(self.name)


# 章节的数据模型
class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True)
    chapter_name = db.Column(db.String(233), default='点击阅读')
    content_url = db.Column(db.String(233))

    novel_id = db.Column(db.Integer(), db.ForeignKey('novel.id'))
    contents = db.relationship('Content', backref='chapter')

    def __repr__(self):
        return "<chapter {}>".format(self.chapter_name)


# 文本内容的数据模型
class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    content_text = db.Column(db.Text)

    chapter_id = db.Column(db.Integer(), db.ForeignKey('chapter.id'))
