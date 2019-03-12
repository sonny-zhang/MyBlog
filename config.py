# @Time     : 2019/3/6 21:30
# @Author   : sonny-zhang
# @FileName : manage.py
# @Blog     : http://www.cnblogs.com/1fengchen1/

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'https://github.com/sonny-zhang'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', '465')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in ['true', 'on', 1]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_MAIL_SUBJECT_PREFIX = '[Sonny]'
    FLASK_MAIL_SENDER = 'Sonny <sonny.zhang@foxmail.com>'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #: init_app()方法，参数是application实例。
    #: 功能：可以执行当前环境配置的初始化
    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # 自动提交数据变更
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class Testing(Config):
    pass


class Product(Config):
    pass


config = {
    'development': Development,
    'testing': Testing,
    'product': Product,

    'default': Development
}
