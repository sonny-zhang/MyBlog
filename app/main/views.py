# @Time     : 2019/3/6 21:31
# @Author   : sonny-zhang
# @FileName : views.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from datetime import datetime
from flask import render_template
from flask.views import MethodView


class Index(MethodView):
    def get(self):
        return render_template('index.html', current_time=datetime.utcnow())

    def post(self):
        pass
