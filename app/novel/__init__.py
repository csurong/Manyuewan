# _*_ coding:utf-8 _*_

from flask import Blueprint

novel = Blueprint('novel', '__name__')

import app.novel.views