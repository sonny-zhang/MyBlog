# @Time     : 2019/3/11 21:06
# @Author   : sonny-zhang
# @FileName : models.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request
from markdown import markdown
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager, db
import hashlib
import bleach


class Permission:
    FOLLOW = 1  #: 关注他人
    COMMENT = 2  #: 在他人撰写的文章中发布评论
    WRITE = 4  #: 写原创文章
    MODERATE = 8  #: 查处他人发表的不当评论
    ADMIN = 16  #: 管理网站


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        """定义默认角色为匿名角色"""
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        """创建角色: 运行
        python manage.py shell
        Role.insert_roles()
        Role.query.all()·
        """
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Admin': [Permission.FOLLOW, Permission.COMMENT,
                      Permission.WRITE, Permission.MODERATE,
                      Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                #: 写死的roles字典里没有找到，就回去创建角色name
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        """添加权限
        :param perm: 权限位
        :return: None
        """
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        """删除权限
        :param perm:权限位
        :return: None
        """
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        """重置角色权限位0匿名角色
        :return: None
        """
        self.permissions = 0

    def has_permission(self, perm):
        """判断是否有权限
        :param perm: 权限位
        :return: True/False
        """
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Follow(db.Model):
    """关注功能的关联表"""
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


#: 支持用户登录需要继承UserMixin，实现了用户已经登录/允许用户登录/普通用户/用户唯一标识
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    #: 关注了谁
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    #: 被谁关注了
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        """构造函数赋予用户角色"""
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

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
        """生成认证注册账户的token: 使用User.id生成token
        :param expiration: 生效时长，秒
        :return: token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        #: 指定用户的id为加密数据，因为id只有数据库知道
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """认证注册账户：校验token+设置User.confirmed为True"""
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

    @staticmethod
    def reset_password(token, new_password):
        """检查token和重置新密码
        :param token: url后缀的token
        :param new_password:
        :return: True
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        """生成修改邮箱功能使用的token"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'users_id': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        """修改邮箱：验证token里users_id，修改的邮箱不在数据库"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('users_id') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def can(self, perm):
        """检查用户是否有权限操作：在请求和赋予角色的权限间进行位运算
        :param perm: 权限位
        :return: 角色中包含请求的所有权限位，返回True; 否则False
        """
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        """检查是否有管理员权限，因为经常使用所以分离从上个方法分离出来
        :return: True/False
        """
        return self.can(Permission.ADMIN)

    def ping(self):
        """更新最后一次访问时间"""
        self.last_seen = datetime.utcnow()
        self.add = db.session.add(self)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        """生成个人全球统一头像url"""
        url = 'https://www.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        u = '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
        return u

    def follow(self, user):
        """关注用户功能"""
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        """取消关注"""
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        """【关注user】查询self是否关注了user
        :param user: 要查询的user
        :return: True/False
        """
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        """【被user关注】查询self是否被user关注了
        :param user: 要查询的user
        :return: True/False
        """
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """flask_login要求实现的回调函数，指定用户标识符的回调函数
    找到用户的id返回用户对象，否则返回None
    """
    return User.query.get(int(user_id))


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Article.body, 'set', Article.on_changed_body)
