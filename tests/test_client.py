# @Time     : 2019/4/4 9:21
# @Author   : sonny.zhang
# @FileName : test_client.py
# @github   : @sonny-zhang
import re
import unittest
from app import create_app, db
from app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """访问首页"""
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('游客' in data)

    def test_register_and_login(self):
        """申请一个新账户并登录"""
        #: 申请
        response = self.client.post('/auth/register', data={
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat123',
            'password2': 'cat123',
        })
        self.assertEqual(response.status_code, 302)

        #: 登录
        response = self.client.post('/auth/login', data={
            'email': 'john@example.com',
            'password': 'cat123'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search(r'您好,\s+john!', data))
        self.assertTrue('您还没有认证您的邮箱' in data)

        #: 发送确认令牌
        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        #: 认证账户需要带入登录态
        response = self.client.get('/auth/confirm/{}'.format(token),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('您已经认证通过，谢谢！' in data)

        #: 登出
        response = self.client.get('/auth/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('您已经成功退出' in data)
