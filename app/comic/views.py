# _*_ coding:utf-8 _*_
from . import comic
from .forms import SearchForm
from flask import render_template


@comic.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        pass
    return render_template('/comic/index.html', form=form)
