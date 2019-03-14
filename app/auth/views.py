# @Time     : 2019/3/14 10:07
# @Author   : sonny.zhang
# @FileName : views.py
# @github   : @sonny-zhang
from flask.views import MethodView
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from app import db
from app.models import User
from .forms import LoginForm, RegistrationForm


class Login(MethodView):
    def get(self):
        form = LoginForm()
        return render_template('auth/login.html', form=form)

    def post(self):
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
        logout_user()
        flash('您已经退出登录')
        return redirect(url_for('main.index'))


class Password_Reset_Request(MethodView):
    def get(self):
        pass


class Register(MethodView):
    def get(self):
        form = RegistrationForm()
        return render_template('auth/register.html', form=form)

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            flash('注册成功！')
            return redirect(url_for('auth.login'))
        return render_template('auth/register.html', form=form)
