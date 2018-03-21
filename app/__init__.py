# _*_ coding:utf-8 _*_


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:rong@localhost/manyuewan?charset=utf8"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'wtforms csrf'
app.config['CHAPTER_PER_PAGE'] = 30

db = SQLAlchemy(app)

from app.novel import novel as novel_blueprint
from app.comic import comic as comic_blueprint

app.register_blueprint(novel_blueprint)
app.register_blueprint(comic_blueprint, url_prefix='/comic')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('novel/404.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('novel/500.html'), 500


if __name__ == '__main__':
    app.run()
