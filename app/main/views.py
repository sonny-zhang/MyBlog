# @Time     : 2019/3/6 21:31
# @Author   : sonny-zhang
# @FileName : views.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from datetime import datetime
from flask import render_template, session, flash
from flask.views import MethodView
from app.forms import *


class Index(MethodView):
    def get(self):
        form = NameForm()
        return render_template('index.html', current_time=datetime.utcnow(), form=form)

    def post(self):
        form = NameForm()
        if form.validate_on_submit():
            #: 所有数据通过验证函数
            old_name = session.get('name')
            if old_name is not None and old_name != form.name.data:
                flash('您的名字已经被修改！')
            session['name'] = form.name.data
            # return redirect(url_for('main.index'))
        return render_template('index.html', current_time=datetime.utcnow(),
                               form=form, name=session.get('name'))
