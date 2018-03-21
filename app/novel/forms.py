# _*_ coding:utf-8 _*_

from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_name = StringField(
        label='搜索框',
        validators=[
            DataRequired('请输入小说名称'),
        ],
        description='搜索框',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入网络小说名称',
            'id': 'search_name'
        }
    )

    submit = SubmitField(
        label='搜索',
        render_kw={
            'class': 'button white',
            'id': 'subscribe-submit',
            'value': 'search'
        }
    )