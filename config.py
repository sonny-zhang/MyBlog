# @Time     : 2019/3/6 21:30
# @Author   : sonny-zhang
# @FileName : manage.py
# @Blog     : http://www.cnblogs.com/1fengchen1/

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guss string'

    #: init_app()方法，参数是application实例。
    #: 功能：可以执行当前环境配置的初始化
    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    pass


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
