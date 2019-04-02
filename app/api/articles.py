# @Time     : 2019/4/2 17:05
# @Author   : sonny.zhang
# @FileName : articles.py
# @github   : @sonny-zhang
from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Article, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/articles/')
def get_articles():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.paginate(
        page, per_page=current_app.config['FLASK_ArticleS_PER_PAGE'],
        error_out=False)
    articles = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_articles', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_articles', page=page+1)
    return jsonify({
        'articles': [article.to_json() for article in articles],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/articles/<int:id>')
def get_article(id):
    article = Article.query.get_or_404(id)
    return jsonify(article.to_json())


@api.route('/articles/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_article():
    article = Article.from_json(request.json)
    article.author = g.current_user
    db.session.add(article)
    db.session.commit()
    return jsonify(article.to_json()), 201, \
        {'Location': url_for('api.get_article', id=article.id)}


@api.route('/articles/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_article(id):
    article = Article.query.get_or_404(id)
    if g.current_user != article.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    article.body = request.json.get('body', article.body)
    db.session.add(article)
    db.session.commit()
    return jsonify(article.to_json())
