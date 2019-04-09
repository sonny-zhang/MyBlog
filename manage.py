# @Time     : 2019/3/6 21:30
# @Author   : sonny-zhang
# @FileName : manage.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

import sys
from app import create_app, db
from app.models import Role, User, Permission, Article, Follow, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade

app = create_app(os.getenv('MyBlog_CONFIG') or 'default')
manager = Manager(app)
#: 使用Migrate必须有app, db参数
migrate = Migrate(app, db)


#: 集成到Python Shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Follow=Follow,
                Permission=Permission, Article=Article, Comment=Comment)


#: Shell命令注册了make_context回调函数，函数里的对象能直接导入shell
manager.add_command("shell", Shell(make_context=make_shell_context))
#: flask_migrate提供的MigrateCommand可以加入manager的对象，就可以用数据库迁移命令了
manager.add_command('db', MigrateCommand)


@manager.option('-c', '--coverage', dest='coverage', default=False, help='在代码覆盖下运行测试')
def test(coverage):
    """运行单元测试"""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        #: 重新启动测试
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(['python'] + sys.argv))  #: Windows下要加上['python']，因为dll是32位

    import unittest
    tests = unittest.defaultTestLoader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('代码覆盖率概要：')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML版本：file://%s/index.html' % covdir)
        COV.erase()


@manager.option('-l', '--length', dest='length', default=25, help='要包含在分析器报告中的函数数')
@manager.option('-p', '--profile-dir', dest='profile_dir', default=None, help='分析器数据保存的文件夹')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """运行部署任务"""
    # 迁移最后一个数据库版本
    upgrade()

    # 创建或者更新Role表
    Role.insert_roles()

    # 所有的用户关注自己
    User.add_self_follows()


if __name__ == "__main__":
    manager.run()
    #: 创建角色
    Role.insert_roles()
    Role.query.all()
    #: 创建假测试数据
    from app.fake import users, articles

    users()
    articles()
