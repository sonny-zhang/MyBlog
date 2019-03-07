# @Time     : 2019/3/6 23:17
# @Author   : sonny-zhang
# @FileName : urls.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from . import main
from .views import *

main.add_url_rule('/', view_func=Index.as_view('index'))
