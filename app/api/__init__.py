# @Time     : 2019/4/2 14:46
# @Author   : sonny.zhang
# @FileName : __init__.py.py
# @github   : @sonny-zhang
from flask import Blueprint

api = Blueprint('api', __name__)

from . import articles, authentication, comments, errors, users