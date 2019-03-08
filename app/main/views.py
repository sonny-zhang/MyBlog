# @Time     : 2019/3/6 21:31
# @Author   : sonny-zhang
# @FileName : views.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from datetime import datetime
from flask import render_template
from flask.views import MethodView
from .forms import *


class Index(MethodView):
    def get(self):
        return render_template('index.html', current_time=datetime.utcnow())

    def post(self):
        name = None
        form = NameForm()
        if form.validate_on_submit():
            #: 所有数据通过验证函数
            name = form.name.data
            # form.name.data = ''
        return render_template('index.html', current_time=datetime.utcnow(),
                               form=form, name=name)
