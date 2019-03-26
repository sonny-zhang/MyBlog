# @Time     : 2019/3/6 23:21
# @Author   : sonny-zhang
# @FileName : forms.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from app.models import Role, User


class NameForm(FlaskForm):
    name = StringField('用户名', validators=[InputRequired()])
    submit = SubmitField('提交')

class EditProfileForm(FlaskForm):
    """编辑个人资料"""
    name = StringField('真实姓名', validators=[Length(0, 16)])
    location = StringField('所在地', validators=[Length(0, 64)])
    about_me = TextAreaField('简介')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email(message='无效的邮箱地址.')])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('[\u4e00-\u9fa5A-Za-z0-9_.]*$', 0,
               '只允许中英文、数字、下划线、句点.')])
    confirmed = BooleanField('认证')
    role = SelectField('角色', coerce=int)
    name = StringField('真实名字', validators=[Length(0, 64)])
    location = StringField('所在地', validators=[Length(0, 64)])
    about_me = TextAreaField('简介')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮件已经被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')