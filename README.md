## 项目介绍

![漫阅湾.png](https://upload-images.jianshu.io/upload_images/6434703-71a32de3e7835d80.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用 Gunicorn 和 Nginx 部署在 111.231.85.221（买的国内服务器，实在是不想备案，太麻烦，能用就行）

漫阅湾，一个支持小说和漫画在线搜索和阅读的网站，后端使用 Flask 框架，前端响应式布局，小说与漫画由爬虫实时抓取

2018.03.21 完成小说功能

2018.03.23 项目上线部署 

2018.03.26 有朋友说服务器一直报错，我检查了一下，是爬的网站服务崩了，所以我的也跟着崩了，今晚我花时间重写一个，最近有点忙，见谅

后期计划完成 漫画功能、注册登录功能、收藏功能、管理员后台管理功能...欢迎提出你的建议

## 项目结构

```
app
├── comic
│   ├── forms.py
│   ├── __init__.py  
│   └── views.py
|
├── __init__.py
|
├── models.py
|
├── novel
│   ├── forms.py
│   ├── __init__.py
│   └── views.py
|
├── spider
│   ├── comic_splider.py
│   ├── novel_index_spider.py
│   ├── novel_spider.py
|
├── static
│   ├── css
│   ├── fonts
│   ├── images
│   ├── js
│   └── sass
|── templates
|   ├── comic
|   │   └── index.html
|   ├── novel
|   │   ├── 404.html
|   │   ├── 500.html
|   │   ├── base.html
|   │   ├── chapters.html
|   │   ├── content.html
|   │   ├── index.html
|   │   └── result.html
|   └── tmp
manage.py
```

## 爬虫部分：
	+ 主页爬虫
	+ 搜索结果页爬虫

主页爬虫: 每次访问主页时自动抓取最新更新的小说，此处考虑到前端使用的 Bootstrap 布局，因此只抓取十二本

搜索结果页爬虫: 根据用户的搜索关键字抓取数据。爬虫默认只抓取第一页的搜索结果，如有需要，此处可拓展，给与用户操作功能，继续爬取后页的数据（暂不考虑此功能）

## Flask 部分

常规的 MVC 结构。在项目结构设计时，为后期功能预留了操作空间，之后无需再对已有功能修改，新增功能可单独开发，直接在 app.__init__.py 中注册蓝图即可

## 必要说明

clone 本项目本地测试时，请根据需要，自行修改 `app.config['SQLALCHEMY_DATABASE_URI']` 数据库的配置。

为了开发时候的方便，已将应用配置全写在了 `app.__init__.py` 文件中，从 `manage.py` 中启动调试

