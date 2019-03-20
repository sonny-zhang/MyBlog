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
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 18)])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    """注册表单"""
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email(message='无效的邮箱地址.')])
    username = StringField('用户名', validators=[DataRequired(), Length(4, 64), Regexp('[\u4e00-\u9fa5A-Za-z0-9_.]*$', 0,
                                                                                    '只允许中英文、数字、下划线、句点.')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 18), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('重复密码', validators=[DataRequired(), Length(6, 18)])
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


class ChangePasswordForm(FlaskForm):
    """修改密码表单"""
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), Length(6, 18), EqualTo('password2',
                                                                                 message='Passwords must match.')])
    password2 = PasswordField('Confirm New Password', validators=[DataRequired(), Length(6, 18)])
    submit = SubmitField('Submit')


class PasswordResetRequestForm(FlaskForm):
    """重置秘密表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Submit')


class ChangeEmailForm(FlaskForm):
    """修改邮箱地址"""
    pass

