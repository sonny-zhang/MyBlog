# @Time     : 2019/3/6 21:30
# @Author   : sonny-zhang
# @FileName : _init__.py
# @Blog     : http://www.cnblogs.com/1fengchen1/

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config

bootstrap = Bootstrap()
# db = SQLAlchemy()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    #: 获得环境的classobj
    environment = config[config_name]
    app.config.from_object(environment)
    #: 对环境初始化
    environment.init_app(app)

    bootstrap.init_app(app)
    # db.init_app(app)
    moment.init_app(app)

    #: 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
