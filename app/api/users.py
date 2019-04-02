# @Time     : 2019/4/2 17:00
# @Author   : sonny.zhang
# @FileName : users.py
# @github   : @sonny-zhang
from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Article


@api.route('/users/<int:id>')
def get_user(id):
    """获取用户数据"""
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/articles/')
def get_user_articles(id):
    """获取用户的所有文章"""
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.articles.order_by(Article.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_ARTICLES_PER_PAGE'],
        error_out=False)
    articles = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_articles', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_articles', id=id, page=page+1)
    return jsonify({
        'articles': [article.to_json() for article in articles],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:id>/timeline/')
def get_user_followed_articles(id):
    """关注的人文章"""
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_articles.order_by(Article.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_ARTICLES_PER_PAGE'],
        error_out=False)
    articles = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_articles', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_articles', id=id, page=page+1)
    return jsonify({
        'articles': [article.to_json() for article in articles],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
