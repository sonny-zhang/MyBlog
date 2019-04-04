# @Time     : 2019/3/6 21:30
# @Author   : sonny-zhang
# @FileName : manage.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'https://github.com/sonny-zhang'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_MAIL_SUBJECT_PREFIX = '[Sonny]'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or ''
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', '465')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in ['true', 'on', 1]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    FLASK_ARTICLES_PER_PAGE = 20    # 文章列表数据每页显示的条数
    FLASK_FOLLOWERS_PER_PAGE = 50   # 关注用户列表数据每页显示的条数
    FLASK_COMMENTS_PER_PAGE = 30    # 评论列表数据每页显示的条数

    #: init_app()方法，参数是application实例。
    #: 功能：可以执行当前环境配置的初始化
    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' +\
                              os.path.join(basedir, 'data-dev.sqlite')
    # 自动提交数据变更


class Testing(Config):
    TESTING = True  # 用来测试开启测试环境
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + \
                              os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class Product(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + \
                              os.path.join(basedir, 'data.sqlite')


config = {
    'development': Development,
    'testing': Testing,
    'product': Product,

    'default': Development
}
