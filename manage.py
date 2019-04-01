# @Time     : 2019/3/6 21:30
# @Author   : sonny-zhang
# @FileName : manage.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
import os
from app import create_app, db
from app.models import Role, User, Permission, Article, Follow
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('MyBlog_CONFIG') or 'default')
manager = Manager(app)
#: 使用Migrate必须有app, db参数
migrate = Migrate(app, db)


#: 集成到Python Shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Follow=Follow,
                Permission=Permission, Article=Article)


#: Shell命令注册了make_context回调函数，函数里的对象能直接导入shell
manager.add_command("shell", Shell(make_context=make_shell_context))
#: flask_migrate提供的MigrateCommand可以加入manager的对象，就可以用数据库迁移命令了
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """运行单元测试"""
    import unittest
    tests = unittest.defaultTestLoader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
    #: 创建角色
    Role.insert_roles()
    Role.query.all()
    #: 创建假测试数据
    from app.fake import users, articles
    users()
    articles()
