# @Time     : 2019/3/14 10:06
# @Author   : sonny.zhang
# @FileName : urls.py
# @github   : @sonny-zhang
from .views import *
from . import auth

auth.add_url_rule('/login', view_func=Login.as_view('login'))
auth.add_url_rule('/logout', view_func=Logout.as_view('logout'))
auth.add_url_rule('/register', view_func=Register.as_view('register'))
auth.add_url_rule('/unconfirmed', view_func=Unconfirmed.as_view('unconfirmed'))
auth.add_url_rule('/confirm/<token>', view_func=Confirm.as_view('confirm'))
auth.add_url_rule('/resend_confirmation', view_func=ResendConfirmation.as_view('resend_confirmation'))

