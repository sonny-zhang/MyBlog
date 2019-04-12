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
    FLASK_MAIL_SUBJECT_PREFIX = '[Blog]'
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

    JSON_AS_ASCII = False   # 返回json格式，中文显示

    #: 启用记录查询统计数字功能；缓慢查询的阈值设为0.5秒
    SQLALCHEMY_RECORD_QUERIES = True
    FLASK_SLOW_DB_QUERY_TIME = 0.5

    #: init_app()方法，参数是application实例。
    #: 功能：可以执行当前环境配置的初始化
    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('MyBlog_DEV_DATABASE_URL') or 'sqlite:///' +\
                              os.path.join(basedir, 'data-dev.sqlite')
    # 自动提交数据变更


class Testing(Config):
    TESTING = True  # 用来测试开启测试环境
    #: '?check_same_thread=False' 设置该项，就可以允许一个线程创建并访问的sqlite的数据库，另外一个线程也可以进行访问
    SQLALCHEMY_DATABASE_URI = (os.environ.get('MyBlog_TEST_DATABASE_URL') or 'sqlite:///' +
                              os.path.join(basedir, 'data-test.sqlite')) + '?check_same_thread=False'
    WTF_CSRF_ENABLED = False


class Product(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('MyBlog_DATABASE_URL') or 'sqlite:///' + \
                              os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_SSL', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASK_MAIL_SENDER,
            toaddrs=[cls.FLASK_ADMIN],
            subject=cls.FLASK_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': Development,
    'testing': Testing,
    'product': Product,

    'default': Development
}
