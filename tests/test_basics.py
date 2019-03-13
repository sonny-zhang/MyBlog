# @Time     : 2019/3/13 16:40
# @Author   : sonny.zhang
# @FileName : test_basics.py
# @github   : @sonny-zhang
import unittest
from flask import current_app
from app import create_app, db


class BasicsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # 激活程序上下文
        self.app_context = self.app.app_context()
        self.app_context.push()
        # 创建表结构(如果没有)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        # 删除数据，表结构依然存在
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """测试APP实例创建成功; 为False代表成功"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """测试APP在运行在测试环境"""
        self.assertTrue(current_app.config['TESTING'])
