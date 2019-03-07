# @Time     : 2019/3/6 21:31
# @Author   : sonny-zhang
# @FileName : __init__.py
# @Blog     : http://www.cnblogs.com/1fengchen1/

from flask import Blueprint
#: 创建蓝图
main = Blueprint('main', __name__)

#: 加载路由，异常处理。(urls里导入了views，所以不用加载了)
from . import urls, errors
