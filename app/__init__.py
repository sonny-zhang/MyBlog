# @Time     : 2019/3/6 21:30
# @Author   : sonny-zhang
# @FileName : _init__.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
mail = Mail()
pagedown = PageDown()
#: 初始化login用户认证的等级，设置登录函数的路径
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录才能进入该页面'


def create_app(config_name):
    app = Flask(__name__)
    #: 获得环境的classobj
    environment = config[config_name]
    app.config.from_object(environment)
    #: 对环境初始化
    environment.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    #: 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
