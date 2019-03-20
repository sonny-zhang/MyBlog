# @Time     : 2019/3/11 21:06
# @Author   : sonny-zhang
# @FileName : models.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from . import login_manager, db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


#: 支持用户登录需要继承UserMixin，实现了用户已经登录/允许用户登录/普通用户/用户唯一标识
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        """密码生成哈希值就无法还原"""
        raise AttributeError('密码没有可读的属性')

    @password.setter
    def password(self, password):
        """将密码转化成密码哈希值"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证用户的密码和数据库中的密码哈希值"""
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """验证账户的token: 使用User.id生成token
        :param expiration: 生效时长，秒
        :return: token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        #: 指定用户的id为加密数据，因为id只有数据库知道
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            #: 验证加密方式符合服务器设置的SECRET_KEY、expiration
            data = s.loads(token)
        except:
            return False
        #: 验证解密的数据是正确的
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        """重置账户密码的token: 使用User.id生成token
        :param expiration: 生效时长，秒
        :return: token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        #: 指定用户的id为加密数据，因为id只有数据库知道
        return s.dumps({'reset': self.id})


@login_manager.user_loader
def load_user(user_id):
    """指定用户标识符的回调函数
    找到用户的id返回用户对象，否则返回None
    """
    return User.query.get(int(user_id))
