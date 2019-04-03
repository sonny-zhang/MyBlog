# @Time     : 2019/4/2 17:49
# @Author   : sonny.zhang
# @FileName : comments.py
# @github   : @sonny-zhang
from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Article, Permission, Comment
from . import api
from .decorators import permission_required


@api.route('/comments/')
def get_comments():
    """获取所有评论资源"""
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_comments', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_comments', page=page+1)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/comments/<int:id>')
def get_comment(id):
    """获取1个评论资源"""
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/articles/<int:id>/comments/')
def get_article_comments(id):
    """获取1篇文章所有评论资源"""
    article = Article.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = article.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASK_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_article_comments', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_article_comments', id=id, page=page+1)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/articles/<int:id>/comments/', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_article_comment(id):
    """创建1篇文章评论"""
    article = Article.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.article = article
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, \
        {'Location': url_for('api.get_comment', id=comment.id)}
