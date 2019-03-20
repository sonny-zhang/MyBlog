# @Time     : 2019/3/12 17:32
# @Author   : sonny-zhang
# @FileName : email.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    """多线程发送邮件
    :param to: 接收人
    :param subject: 邮件主题
    :param template: 邮件模板
    :param kwargs: 其他dictionary参数
    :return: 发送事件
    """
    app = current_app._get_current_object()
    msg = Message(current_app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
