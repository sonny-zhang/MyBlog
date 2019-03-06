# @Time     : 2019/3/6 21:39
# @Author   : sonny-zhang
# @FileName : errors.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def page_server_error(e):
    return render_template('500.html'), 500
