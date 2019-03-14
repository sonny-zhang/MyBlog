# @Time     : 2019/3/13 18:00
# @Author   : sonny.zhang
# @FileName : tests_user_model.py
# @github   : @sonny-zhang
import unittest
from app.models import User
from app import db
import time


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        """测试密码转换哈希值值成功"""
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        """测试密码不可访问"""
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verfication(self):
        """测试密码校验器"""
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        """测试相同的密码的哈希值是不同的，真正起到保护作用"""
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        """【被加密数据相同】将数据加密生成的token来验证本人用户"""
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        """【被加密数据不同】将数据加密生成的token来验证非本人用户"""
        u1 = User(password='cat')
        u2 = User(password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        """验证token过期"""
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

