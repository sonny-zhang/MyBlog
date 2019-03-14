# @Time     : 2019/3/14 9:55
# @Author   : sonny.zhang
# @FileName : __init__.py.py
# @github   : @sonny-zhang
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import urls