# @Time     : 2019/3/6 21:31
# @Author   : sonny-zhang
# @FileName : views.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask_login import login_required, current_user
from flask.views import MethodView
from sqlalchemy import desc
from app.models import User, Role, Permission, Article
from app import db
from app.decorators import admin_required
from .forms import EditProfileAdminForm, EditProfileForm, ArticleForm


class Index(MethodView):
    def get(self):
        form = ArticleForm()
        page = request.args.get('page', 1, type=int)
        pagination = Article.query.order_by(desc(Article.timestamp)).paginate(
            page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        return render_template('index.html', form=form, articles=articles,
                               pagination=pagination)

    def post(self):
        """写文章"""
        form = ArticleForm()
        if current_user.can(Permission.WRITE) and form.validate_on_submit():
            article = Article(body=form.body.data,
                        author=current_user._get_current_object())
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('main.index'))
        page = request.args.get('page', 1, type=int)
        pagination = Article.query.order_by(desc(Article.timestamp)).paginate(
            page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        return render_template('index.html', form=form, articles=articles,
                               pagination=pagination)


class Users(MethodView):
    def get(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        articles = user.articles.order_by(Article.timestamp.desc()).all()
        return render_template('user.html', user=user, articles=articles)


class EditProfile(MethodView):
    @login_required
    def get(self):
        """访问个人资料页"""
        form = EditProfileForm()
        form.name.data = current_user.name
        form.location.data = current_user.location
        form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', form=form)

    @login_required
    def post(self):
        """编辑非admin角色个人资料"""
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
        """访问admin角色个人资料页"""
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

    @login_required
    @admin_required
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


class ArticleView(MethodView):
    @login_required
    def get(self, id):
        """文章详情页"""
        article = Article.query.get_or_404(id)
        return render_template('article.html', articles=[article])


class ArticleEdit(MethodView):
    def get(self, id):
        article = Article.query.get_or_404(id)
        form = ArticleForm()
        form.body.data = article.body
        return render_template('edit_article.html', form=form)

    @login_required
    def post(self, id):
        """编辑文章"""
        article = Article.query.get_or_404(id)
        if current_user != article.author and \
                not current_user.can(Permission.ADMIN):
            abort(403)
        form = ArticleForm()
        if form.validate_on_submit():
            article.body = form.body.data
            db.session.add(article)
            db.session.commit()
            flash('文章已经更新.')
            return redirect(url_for('.post', id=article.id))
        form.body.data = article.body
        return render_template('edit_post.html', form=form)
