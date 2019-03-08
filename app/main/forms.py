# @Time     : 2019/3/6 23:21
# @Author   : sonny-zhang
# @FileName : forms.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class NameForm(Form):
    name = StringField('用户名', validators=[InputRequired()])
    submit = SubmitField('提交')
