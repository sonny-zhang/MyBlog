# @Time     : 2019/3/6 21:31
# @Author   : sonny-zhang
# @FileName : views.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from datetime import datetime
from flask import render_template, abort, current_app, redirect, url_for, flash
from flask_login import login_required, current_user
from flask.views import MethodView
from app.models import User, Role
from app import db
from app.decorators import admin_required
from .forms import EditProfileAdminForm, EditProfileForm


class Index(MethodView):
    def get(self):
        return render_template('index.html', current_time=datetime.utcnow())


class Users(MethodView):
    def get(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('user.html', user=user)


class EditProfile(MethodView):
    @login_required
    def get(self):
        form = EditProfileForm()
        form.name.data = current_user.name
        form.location.data = current_user.location
        form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', form=form)

    @login_required
    def post(self):
        """编辑非admin个人资料"""
        form = EditProfileForm()
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.location = form.location.data
            current_user.about_me = form.about_me.data
            # db.session.add(current_user._get_current_object())
            db.session.add(current_user)
            db.session.commit()
            flash('您的资料已经跟新.')
            return redirect(url_for('main.user', username=current_user.username))
        form.name.data = current_user.name
        form.location.data = current_user.location
        form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', form=form)


class EditProfileAdmin(MethodView):
    @login_required
    @admin_required
    def get(self, id):
        user = User.query.get_or_404(id)
        form = EditProfileAdminForm(user=user)
        form.email.data = user.email
        form.username.data = user.username
        form.confirmed.data = user.confirmed
        form.role.data = user.role_id
        form.name.data = user.name
        form.location.data = user.location
        form.about_me.data = user.about_me
        return render_template('edit_profile.html', form=form, user=user)

    def post(self, id):
        """编辑admin用户资料"""
        user = User.query.get_or_404(id)
        form = EditProfileAdminForm(user=user)
        if form.validate_on_submit():
            user.email = form.email.data
            user.username = form.username.data
            user.confirmed = form.confirmed.data
            user.role = Role.query.get(form.role.data)
            user.name = form.name.data
            user.location = form.location.data
            user.about_me = form.about_me.data
            db.session.add(user)
            db.session.commit()
            flash('个人资料已经更新.')
            return redirect(url_for('main.user', username=user.username))
        form.email.data = user.email
        form.username.data = user.username
        form.confirmed.data = user.confirmed
        form.role.data = user.role_id
        form.name.data = user.name
        form.location.data = user.location
        form.about_me.data = user.about_me
        return render_template('edit_profile.html', form=form, user=user)
