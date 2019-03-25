# @Time     : 2019/3/14 10:07
# @Author   : sonny.zhang
# @FileName : views.py
# @github   : @sonny-zhang
from flask.views import MethodView
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from . import auth
from app.email import send_email
from app.models import User
from .forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ChangePasswordForm, \
    ChangeEmailForm, PasswordResetForm


@auth.before_app_request
def before_request():
    """拦截app请求: 登录了但是没有认证(更新访问时间)->Unconfirmed"""
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


class Unconfirmed(MethodView):
    @login_required
    def get(self):
        """限制普通没有认证的用户访问页面:普通用户is_anonymous返回False"""
        if current_user.is_anonymous or current_user.confirmed:
            #: 普通用户或已经认证用户->index页面
            return redirect(url_for('main.index'))
        return render_template('auth/unconfirmed.html')


class ResendConfirmation(MethodView):
    @login_required
    def get(self):
        """重新发送账户验证邮件"""
        token = current_user.generate_confirmation_token()
        send_email(current_user.email, '认证您的账户', 'auth/email/confirm', user=current_user, token=token)
        flash('一封新的认证邮件已经发到您的邮箱，请及时认证！')
        return redirect(url_for('main.index'))


class Confirm(MethodView):
    @login_required
    def get(self, token):
        """认证注册用户
        :param token: 根据用户的id生成的token
        :return: index.html
        """
        if current_user.confirmed:
            #: 用户已经认证
            return redirect(url_for('main.index'))
        if current_user.confirm(token):
            #: 认证通过,在model里修改User.confirmed为True，这里提交到数据库
            db.session.commit()
            flash('您已经认证通过，谢谢！')
        else:
            flash('认证链接无效或者已经过期！')
        return redirect(url_for('main.index'))


class Register(MethodView):
    def get(self):
        form = RegistrationForm()
        return render_template('auth/register.html', form=form)

    def post(self):
        """注册"""
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, '认证您的账户', 'auth/email/confirm', user=user, token=token)
            flash('注册成功！认证邮件已经发到您的邮箱。')
            return redirect(url_for('main.index'))
        return render_template('auth/register.html', form=form)


class Login(MethodView):
    def get(self):
        form = LoginForm()
        return render_template('auth/login.html', form=form)

    def post(self):
        """登录"""
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.verify_password(form.password.data):
                #: login_user在用户会话中把用户标记为已登录;
                #: remember为False关闭浏览器下次就要重新登录;
                #: remember为True,会在浏览器写入一个长期有效的cookie,使用cookie复现用户会话
                login_user(user, form.remember_me.data)
                #: args里的next参数保存着上一个用户访问的url地址
                #: 如果用户第一次进来就是登录页面，next是为None，登录后定位到主页
                #: 如果用户是从限制需要登录的页面A跳转到登录页B，登录后返回的是页面A
                return redirect(request.args.get('next') or url_for('main.index'))
            flash('无效的用户或密码')
            #: email不存在且密码不正确，重新带着表单数据渲染登录页
        return render_template('auth/login.html', form=form)


class Logout(MethodView):
    @login_required
    def get(self):
        """登出"""
        logout_user()
        flash('您已经退出登录')
        return redirect(url_for('main.index'))


class Change_Password(MethodView):
    @login_required
    def get(self):
        form = ChangePasswordForm()
        return render_template('auth/change_password.html', form=form)

    @login_required
    def post(self):
        """修改密码"""
        form = ChangePasswordForm()
        if form.validate_on_submit():
            if current_user.verify_password(form.old_password.data):
                current_user.password = form.password.data
                db.session.add(current_user)
                db.session.commit()
                flash('您的密码已经修改成功！')
                return redirect(url_for('main.index'))
            else:
                flash('原密码无效！')
        return render_template('auth/change_password.html', form=form)


class Password_Reset_Request(MethodView):
    def get(self):
        form = PasswordResetRequestForm()
        return render_template('auth/reset_password.html', form=form)

    def post(self):
        """重置密码：需要通过邮件里的链接去重置"""
        form = PasswordResetRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                token = user.generate_reset_token()
                send_email(user.email, '验证您的账户', 'auth/email/reset_password',
                           user=user, token=token)
                flash('请到你的邮箱确认要进行重置密码操作！')
                return redirect(url_for('auth.login'))
            flash('邮箱无效！')
        return render_template('auth/reset_password.html', form=form)


class Password_Reset(MethodView):
    def get(self, token):
        if not current_user.is_anonymous:
            return redirect(url_for('main.index'))
        form = PasswordResetForm()
        return render_template('auth/reset_password.html', form=form)

    def post(self, token):
        if not current_user.is_anonymous:
            return redirect(url_for('main.index'))
        form = PasswordResetForm()
        if form.validate_on_submit():
            if User.reset_password(token, form.password.data):
                db.session.commit()
                flash('您的密码已经修改完成，请登录！')
                return redirect(url_for('auth.login'))
            else:
                flash('认证链接无效或者已经过期！请重新获取认证')
                return redirect(url_for('auth.password_reset_request'))
        return render_template('auth/reset_password.html', form=form)


class Change_Email_Request(MethodView):
    @login_required
    def get(self):
        form = ChangeEmailForm()
        return render_template('auth/change_email.html', form=form)

    @login_required
    def post(self):
        form = ChangeEmailForm()
        if form.validate_on_submit():
            if current_user.verify_password(form.password.data):
                new_email = form.email.data
                token = current_user.generate_email_change_token(new_email)
                send_email(new_email, '验证您的邮箱地址', 'auth/email/change_email',
                           user=current_user, token=token)
                flash('验证邮件已经发到您的邮箱里！')
                return redirect(url_for('main.index'))
            else:
                flash('无效的邮箱或密码！')
        return render_template('auth/change_email.html', form=form)


class Change_Email(MethodView):
    def get(self, token):
        if current_user.change_email(token):
            db.session.commit()
            flash('您的邮箱地址已经修改成功了！')
        else:
            flash('无效的请求！')
        return redirect(url_for('main.index'))




