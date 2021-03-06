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
auth.add_url_rule('/change_password', view_func=Change_Password.as_view('change_password'))
auth.add_url_rule('/password_reset', view_func=Password_Reset_Request.as_view('password_reset_request'))
auth.add_url_rule('/password_reset/<token>', view_func=Password_Reset.as_view('password_reset'))
auth.add_url_rule('/change_email', view_func=Change_Email_Request.as_view('change_email_request'))
auth.add_url_rule('/change_email/<token>', view_func=Change_Email.as_view('change_email'))

