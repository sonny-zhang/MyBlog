# @Time     : 2019/3/14 11:29
# @Author   : sonny.zhang
# @FileName : forms.py
# @github   : @sonny-zhang
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    """登录表单"""
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email(message='无效的邮箱地址.')])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    """注册表单"""
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email(message='无效的邮箱地址.')])
    username = StringField('用户名', validators=[DataRequired(), Length(4, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                    '只允许字母、数字、下划线、英文句点.')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('重复密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        """表单类里有validate_开头且跟着字段名的方法，这个方法和常规的验证函数一起调用.
        验证注册的email不在数据库中
        """
        if User.query.filter_by(email=field.data).first():
            #: ValidationError抛出异常，参数是错误信息
            raise ValidationError('邮箱已经被注册！')

    def validate_username(self, field):
        """验证注册的用户名不在数据库中"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户民已经被注册！')
