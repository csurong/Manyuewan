# _*_ coding:utf-8 _*_

from flask import Blueprint

comic = Blueprint('comic', '__name__')

import app.comic.views