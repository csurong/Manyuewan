# _*_ coding:utf-8 _*_
from . import novel  # 主要是为漫画做准备
from app import db, app
from flask import render_template, url_for, redirect, request, abort, flash
from .forms import SearchForm
from ..models import Novel, Chapter, Content
from ..spider.novel_spider import Spider
from ..spider.novel_index_spider import IndexSpider


@novel.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    # post情况
    if form.validate_on_submit():
        search_name = form.data['search_name']
        return redirect(url_for('novel.search_result', search_name=search_name))
    # get情况
    index_spider = IndexSpider()
    # print('请求已经发出')
    novels = index_spider.get_latest_novel()
    # print('views已经收到爬虫返回的数据，准备渲染')
    return render_template("novel/index.html", form=form, novels=novels)


@novel.route('/novel/<search_name>/')
def search_result(search_name):
    spider = Spider()

    for data in spider.get_search_book_data(search_name):
        name = data['name']
        if Novel.query.filter_by(name=name).count() == 0:
            novel = Novel(
                name=data['name'],
                image_src=data['image_src'],
                chapter_url=data['chapter_url'],
                desc=data['desc'],
                author=data['author'],
                novel_type=data['novel_type'],
                refresh_time=data['refresh_time'],
                latest=data['latest'],
                search_word=search_name
            )
            db.session.add(novel)
    novels = Novel.query.filter_by(search_word=search_name)
    if novels.count() == 0:
        abort(404)
    novels = novels.all()
    return render_template('novel/result.html', search_name=search_name, novels=novels)


@novel.route('/novel/<int:novel_id>')  # 删除参数 <novel_name>
def show_chapters(novel_id):  # 删除参数 novel_name
    #
    page = request.args.get('page', 1, type=int)
    # 如果章节对应的书的 id 已经存在了，就说明这本书的章节都已经存过了。毕竟要么不存，要存就全部存起来的
    if Chapter.query.filter_by(novel_id=novel_id).first() is None:
        spider = Spider()
        novel = Novel.query.filter_by(id=novel_id).first_or_404()
        for data in spider.get_chapter_data(novel.chapter_url):
            chapter = Chapter(
                chapter_name=data['chapter_name'],
                content_url=data['content_url'],
                novel_id=novel_id
            )
            db.session.add(chapter)
    #
    pagination = Chapter.query.filter_by(novel_id=novel_id).paginate(
        page, per_page=app.config['CHAPTER_PER_PAGE'],
        error_out=False
    )
    chapters = pagination.items
    novel = Novel.query.filter_by(id=novel_id).first()
    #
    # chapters = Chapter.query.filter_by(novel_id=novel_id).all()
    return render_template('novel/chapters.html', chapters=chapters, pagination=pagination, novel=novel)


@novel.route('/novel/<int:chapter_id>/')
def content(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()

    spider = Spider()
    text = spider.get_chapter_text(chapter.content_url)
    content = Content(
        content_text=text,
        chapter_id=chapter_id
    )
    db.session.add(content)
    return render_template('novel/content.html', content=content, chapter=chapter)


# 下一章
@novel.route('/novel/next/<int:chapter_id>')
def next(chapter_id):
    novel_id = Chapter.query.filter_by(id=chapter_id).first().novel_id
    next_chapter_id = chapter_id + 1
    next_novel_id = Chapter.query.filter_by(id=next_chapter_id).first_or_404().novel_id

    if novel_id == next_novel_id:
        return redirect(url_for('novel.content', chapter_id=next_chapter_id))
    else:
        flash('已经是最新的一章')
        return redirect(url_for('novel.content', chapter_id=chapter_id))


# 上一章
@novel.route('/novel/prev/<int:chapter_id>')
def prev(chapter_id):
    novel_id = Chapter.query.filter_by(id=chapter_id).first().novel_id
    prev_chapter_id = chapter_id - 1
    if prev_chapter_id < 1:
        abort(500)
    prev_novel_id = Chapter.query.filter_by(id=prev_chapter_id).first_or_404().novel_id

    if novel_id == prev_novel_id:
        return redirect(url_for('novel.content', chapter_id=prev_chapter_id))
    else:
        flash('么有上一章了...')
        return redirect(url_for('novel.content', chapter_id=chapter_id))
