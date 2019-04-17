# @Time     : 2019/3/6 21:31
# @Author   : sonny-zhang
# @FileName : views.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
from flask_sqlalchemy import get_debug_queries
from flask_login import login_required, current_user
from flask.views import MethodView
from sqlalchemy import desc
from app.models import User, Role, Permission, Article, Comment
from . import main
from app import db
from app.decorators import admin_required, permission_required
from .forms import EditProfileAdminForm, EditProfileForm, ArticleForm, CommentForm


@main.after_app_request
def after_request(response):
    """将查询SQL慢于5秒的记录到日志"""
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASK_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'SQL语句查询慢: %s\n参数: %s\n时长: %fs\n上下文: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


class Index(MethodView):
    def get(self):
        form = ArticleForm()
        page = request.args.get('page', 1, type=int)
        show_followed = False
        if current_user.is_authenticated:
            show_followed = bool(request.cookies.get('show_followed', ''))
        if show_followed:
            query = current_user.followed_articles
        else:
            query = Article.query
        pagination = query.order_by(desc(Article.timestamp)).paginate(
            page, per_page=current_app.config['FLASK_ARTICLES_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        return render_template('index.html', form=form, articles=articles, show_followed=show_followed,
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
        show_followed = False
        if current_user.is_authenticated:
            show_followed = bool(request.cookies.get('show_followed', ''))
        if show_followed:
            query = current_user.followed_articles
        else:
            query = Article.query
        pagination = query.order_by(desc(Article.timestamp)).paginate(
            page, per_page=current_app.config['FLASK_ARTICLES_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        return render_template('index.html', form=form, articles=articles, show_followed=show_followed,
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
        form = CommentForm()
        page = request.args.get('page', 1, type=int)
        if page == -1:
            page = (article.comments.count() - 1) // \
                   current_app.config['FLASK_COMMENTS_PER_PAGE'] + 1
        pagination = article.comments.order_by(Comment.timestamp).paginate(
            page, per_page=current_app.config['FLASK_COMMENTS_PER_PAGE'],
            error_out=False)
        comments = pagination.items
        return render_template('article.html', articles=[article], form=form,
                               comments=comments, pagination=pagination)

    @login_required
    def post(self, id):
        """评论"""
        article = Article.query.get_or_404(id)
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data,
                              article=article,
                              author=current_user._get_current_object())
            db.session.add(comment)
            db.session.commit()
            flash('您的评论已经发布！')
            return redirect(url_for('.article', id=article.id, page=-1))
        page = request.args.get('page', 1, type=int)
        if page == -1:
            page = (article.comments.count() - 1) // \
                   current_app.config['FLASK_COMMENTS_PER_PAGE'] + 1
        pagination = article.comments.order_by(Comment.timestamp).paginate(
            page, per_page=current_app.config['FLASK_COMMENTS_PER_PAGE'],
            error_out=False)
        comments = pagination.items
        return render_template('article.html', articles=[article], form=form,
                               comments=comments, pagination=pagination)


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
            return redirect(url_for('.article', id=article.id))
        form.body.data = article.body
        return render_template('edit_post.html', form=form)


class Follow(MethodView):
    @login_required
    @permission_required(Permission.FOLLOW)
    def get(self, username):
        """关注用户username"""
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('无效的用户.')
            return redirect(url_for('.index'))
        if current_user.is_following(user):
            flash('您已经关注了该用户，不用再次关注.')
            return redirect(url_for('.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('您关注了用户%s.' % username)
        return redirect(url_for('.user', username=username))


class UnFollow(MethodView):
    @login_required
    @permission_required(Permission.FOLLOW)
    def get(self, username):
        """取消关注用户username"""
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('无效的用户.')
            return redirect(url_for('.index'))
        if not current_user.is_following(user):
            flash('您还没有关注该用户.')
            return redirect(url_for('.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('您不再关注%s.' % username)
        return redirect(url_for('.user', username=username))


class Followers(MethodView):
    def get(self, username):
        """展示username的粉丝们"""
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('无效的用户.')
            return redirect(url_for('.index'))
        page = request.args.get('page', 1, type=int)
        pagination = user.followers.paginate(
            page, per_page=current_app.config['FLASK_FOLLOWERS_PER_PAGE'],
            error_out=False)
        follows = [{'user': item.follower, 'timestamp': item.timestamp}
                   for item in pagination.items]
        return render_template('followers.html', user=user, title="粉丝",
                               endpoint='.followers', pagination=pagination,
                               follows=follows)


class FollowedBy(MethodView):
    def get(self, username):
        """展示username所关注者们"""
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('无效的用户.')
            return redirect(url_for('.index'))
        page = request.args.get('page', 1, type=int)
        pagination = user.followed.paginate(
            page, per_page=current_app.config['FLASK_FOLLOWERS_PER_PAGE'],
            error_out=False)
        follows = [{'user': item.followed, 'timestamp': item.timestamp}
                   for item in pagination.items]
        return render_template('followers.html', user=user, title="关注",
                               endpoint='.followed_by', pagination=pagination,
                               follows=follows)


class ShowAll(MethodView):
    @login_required
    def get(self):
        """所有文章"""
        resp = make_response(redirect(url_for('.index')))
        #: 设置response的cookie值
        resp.set_cookie('show_followed', '', max_age=30*24*60*60)
        return resp


class ShowFollowed(MethodView):
    @login_required
    def get(self):
        """关注者的文章"""
        resp = make_response(redirect(url_for('.index')))
        resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
        return resp


class Moderate(MethodView):
    @login_required
    @permission_required(Permission.MODERATE)
    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = Comment.query.order_by(Comment.timestamp).paginate(
            page, per_page=current_app.config['FLASK_COMMENTS_PER_PAGE'],
            error_out=False)
        comments = pagination.items
        return render_template('moderate.html', comments=comments,
                               pagination=pagination, page=page)


class ModerateEnable(MethodView):
    @login_required
    @permission_required(Permission.MODERATE)
    def get(self, id):
        comment = Comment.query.get_or_404(id)
        comment.disabled = False
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.moderate',
                                page=request.args.get('page', 1, type=int)))


class ModerateDisable(MethodView):
    @login_required
    @permission_required(Permission.MODERATE)
    def get(self, id):
        comment = Comment.query.get_or_404(id)
        comment.disabled = True
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.moderate',
                                page=request.args.get('page', 1, type=int)))
